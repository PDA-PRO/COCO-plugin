import json
import os
from fastapi import Depends
import openai
from pydantic import BaseModel
from app.api.deps import get_cursor
from app.core import security
from app.db.base import DBCursor
from app.plugin.interface import AbstractPlugin
from . import config


class AiCode(BaseModel):
    code: str
    task_id: int
    sub_id: int
    
class Plugin(AbstractPlugin):
    router_path='/ai-code'
    feature_docs='문제 풀이가 맞은 코드에 대해 판별하고, 더 좋은 효율의 코드를 만들어주는 AI'
    base='ChatGPT 3.5-turbo'

    class TableModel(AbstractPlugin.AbstractTable):
        __key__='sub_id'
        __tablename__='code_improvement'
        task_id: int
        sub_id: int
        code: str
        desc: str
        lang: int

    @staticmethod
    def test():
        return 1

    @staticmethod
    def endpoint_main(info: AiCode, token: dict = Depends(security.check_token), db_cursor:DBCursor=Depends(get_cursor)):  
        Plugin.enable_onoff(db_cursor)
         # 해당 코드에 대한 ai 코드가 있는지 확인
        ai_code:Plugin.TableModel=Plugin.read(db_cursor,sub_id=info.sub_id)

        if ai_code: #ai 개선 코드가 있다면
            return {
                'data': True,
                'code': ai_code.code,
                'desc': ai_code.desc
            }

        efficient_prompt = '''
%s
          
        ''' % (info.code)



        #  ai 답변 결과를 dict 형태로 변경
        efficient_result = ask_ai(efficient_prompt)
        start_idx, end_idx = 0, 0
        for i in range(len(efficient_result)):
            if efficient_result[i] == '{':
                start_idx = i
                break
        for i in range(len(efficient_result)-1, -1, -1):
            if efficient_result[i] == '}':
                end_idx = i
                break

        efficient_result = efficient_result[start_idx: end_idx+1]
        print('code', efficient_result)
        efficient_result = json.loads(efficient_result, strict=False)

        code = efficient_result['code']
        desc = efficient_result['desc']

        new_tuple=Plugin.TableModel(task_id=info.task_id,sub_id=info.sub_id,code=code,desc=desc)
        Plugin.create(db_cursor,new_tuple)
        return {
            'data': True,
            'code': code,
            'desc': desc
        }
    

def ask_ai(prompt):
    openai.api_key = config.CHATGPT_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": '''
당신은 프로그래밍 전문가입니다.
당신은 주어진 프로그램 코드를 분석하고 주어진 코드보다 효율적으로 개선된 코드를 다음과 같은 형식으로 제시합니다.

{
    "code": "<수정된 코드>",
    "desc": "<수정된 코드에 대한 두 줄 이상의 자세한 설명>"
}

'''
            },
            {
            "role": "user",
            "content":prompt
            },
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]["message"]['content']
    # completion = openai.Completion.create(
    # engine='text-davinci-003'  # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
    # , prompt=prompt
    # , temperature=0.5
    # , max_tokens=1024
    # , top_p=1
    # , frequency_penalty=0
    # , presence_penalty=0)
    # return completion['choices'][0]['text']
