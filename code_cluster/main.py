from fastapi import Depends
import requests
from app.api.deps import get_cursor
from app.db.base import DBCursor
from app.plugin.interface import AbstractPlugin
from transformers import (RobertaTokenizer)
import faiss
import numpy

tokenizer = RobertaTokenizer.from_pretrained("microsoft/graphcodebert-base")
max_token_len=512
clustering_k=10
class Plugin(AbstractPlugin):
    router_path='/code-cluster'
    feature_docs='문제 풀이가 맞은 코드에 대해, 해당 코드와 유사한 로직의 다른 코드들을 만들어 주는 AI'
    base='FAISS from facebook'

    @staticmethod
    def test():
        return 1
        
    @staticmethod
    def endpoint_main(task_id:int,sub_id:int,db_cursor:DBCursor=Depends(get_cursor)):
        result=[]
        sql='SELECT sub.code FROM coco.sub_ids as ids, coco.submissions as sub where ids.task_id=%s and sub.id=ids.sub_id and sub.status=3;'
        result=db_cursor.select_sql(sql,[task_id])
        my_code_sql='SELECT sub.code FROM coco.sub_ids as ids, coco.submissions as sub where ids.task_id=%s and sub.id=%s'
        my_code_result=db_cursor.select_sql(my_code_sql,[task_id,sub_id])[0]
        code_list=[my_code_result['code']]
        for i in result:
            code_list.append(i['code'])

        #0 패딩
        code_ids_list=[]
        for i in code_list:
            tokenized_code=tokenizer.convert_tokens_to_ids(tokenizer.tokenize(i))
            if len(tokenized_code)>=max_token_len:
                continue
            else:
                tokenized_code=tokenized_code+(max_token_len-len(tokenized_code))*[0]
                code_ids_list.append(tokenized_code)

        #numpy로 변환 및 0-1정규화
        code_ids_list=numpy.asarray(code_ids_list, dtype='float32')
        min_v=numpy.min(code_ids_list)
        max_v=numpy.max(code_ids_list)
        for i in range(len(code_ids_list)):
            for j in range(max_token_len):
                code_ids_list[i][j]=(code_ids_list[i][j]-min_v)/(max_v-min_v)

        #인덱스 생성
        kmeans = faiss.Kmeans(max_token_len,clustering_k)
        kmeans.train(code_ids_list)

        index = faiss.IndexFlatL2(max_token_len)
        index.add(code_ids_list)
        D, I = index.search(kmeans.centroids, 1) 
        return_list=[]
        for i in zip(I,D):
            return_list.append({'code':code_list[i[0][0]],'distance':float(i[1][0])})

        return return_list