import json
import os
import zipfile
from bs4 import BeautifulSoup
from fastapi import Depends
import openai
from pydantic import BaseModel
from app.api.deps import get_cursor
from app.core.image import image
from app.db.base import DBCursor
from app.plugin.interface import AbstractPlugin
from . import config

class CreateTask(BaseModel):
    content: str | None
    form_data: str
    task_data: dict|None
    is_final: bool

class Plugin(AbstractPlugin):
    router_path='/ai-task'
    feature_docs='알고리즘 문제 생성 시, AI를 통해 생성해주는 AI'
    base='ChatGPT 3.5-turbo'

    class TableModel(AbstractPlugin.AbstractTable):
        __key__='id'
        __tablename__='problem_generation'
        id: int

    @staticmethod
    def test():
        return 1
        
    @staticmethod
    def endpoint_main(info: CreateTask, db_cursor:DBCursor=Depends(get_cursor)):
        Plugin.enable_onoff(db_cursor)
        if info.is_final == False:
            prompt = '''
%s

        ''' % (info.content)

            # 문제 내용 JSON 변환
            result = ask_ai(prompt, task_template)
            print(result)
            start, end = 0, len(result)-1
            for i in range(len(result)):
                if result[i] == '{':
                    start = i
                    break
            for i in range(len(result)-1, -1, -1):
                if result[i] == '}':
                    end = i
                    break
                    
            result = result[start:end+1]
            result = json.loads(result, strict=False)
            print('task', result)
            
            return {'data': True, 'result': result}
        else:   
            # 문제 메인 설명
            description = BeautifulSoup(info.form_data, "lxml").text
            input_desc = info.task_data["inputDescription"]
            output_desc = info.task_data["outputDescription"]
            prompt = '''

위 문제의 설명은 다음과 같습니다
: %s

위 문제의 입력 설명은 다음과 같습니다
: %s

위 문제의 출력 설명은 다음과 같습니다
: %s

다음 정보를 고려해서 위 문제에 대한 파이썬 테스트 케이스를 만들어 주세요
단, 입력이 0 이거나 없는 경우는 빼고 만들어 주세요
''' % (description, input_desc, output_desc)
            print(prompt)
            result = ask_ai(prompt, tc_template)

            start, end = 0, len(result)-1
            for i in range(len(result)):
                if result[i] == '{':
                    start = i
                    break
            for i in range(len(result)-1, -1, -1):
                if result[i] == '}':
                    end = i
                    break

            result = result[start:end+1]
            result = json.loads(result, strict=False)
            print('testcase', result)
            testcase = result['testcase']   # TC
            task = info.task_data # 문제 정보

            sample={'input':[task['inputEx1'],task['inputEx2']],'output':[task['outputEx1'],task['outputEx2']]}
            sample_str=json.dumps(sample)
            # #time_limit, diff는 한자리 숫자 task 테이블에 문제 먼저 삽입해서 id추출
            sql="INSERT INTO `coco`.`task` ( `title`, `sample`,`mem_limit`, `time_limit`, `diff` ) VALUES ( %s, %s, %s, %s, %s);"
            data=(task['title'], sample_str,task['memLimit'],task['timeLimit'],task['diff'])
            task_id=db_cursor.insert_last_id(sql,data)

            for i in map(lambda a:a.strip(),task['category'].split(",")):
                sql="INSERT INTO `coco`.`task_ids` (`task_id`, `category`) VALUES (%s, %s);"
                data=(task_id,i)
                db_cursor.execute_sql(sql,data)

            #desc에서 임시 이미지 삭제 및 실제 이미지 저장
            maindesc=image.save_update_image(os.path.join(os.getenv("TASK_PATH"),"temp"),os.path.join(os.getenv("TASK_PATH"),str(task_id)),description,task_id,"s")

            #desc 저장
            sql="insert into coco.descriptions values (%s,%s,%s,%s);"
            data=(task_id,maindesc,task['inputDescription'],task['outputDescription'])
            db_cursor.execute_sql(sql,data)

            # 플러그인 task에 생성된 문제 아이디 저장
            task_result = Plugin.TableModel(id=task_id)
            Plugin.create(db_cursor, task_result)

            #테스트케이스 json 결과
            input_case, output_case = [], []
            for case in testcase:
                input_case.append(case['input'])
                output_case.append(case['output'])

            # TC 파일 경로 - AI가 생성한 문제는 ai_{task_id}
            testcase_file_path = os.path.join(os.getenv("TASK_PATH"), str(task_id))
            # os.makedirs(testcase_file_path)

            # 입력 TC 파일
            input_file_path = os.path.join(testcase_file_path,'input')
            os.mkdir(input_file_path)
            for i in range(len(input_case)):
                file = open(input_file_path+"/"+str(i+1)+".txt",'w',encoding = 'utf-8') #텍스트파일 생성
                file.write(input_case[i])					#생성한 텍스트파일에 글자를 입력합니다.
                file.close()	

            # 출력 TC 파일
            output_file_path = os.path.join(testcase_file_path,'output')
            os.mkdir(output_file_path)
            for i in range(len(output_case)):
                file = open(output_file_path+"/"+str(i+1)+".txt",'w',encoding = 'utf-8') #텍스트파일 생성
                file.write(output_case[i])					#생성한 텍스트파일에 글자를 입력합니다.
                file.close()	

            # TC 파일 압축해서 저장
            zip_file = zipfile.ZipFile(os.getenv("TASK_PATH") + f"/{str(task_id)}/testcase{str(task_id)}.zip", "w")
            for (path, dir, files) in os.walk(f"{os.getenv('TASK_PATH')}{str(task_id)}/input/"):
                for file in files:
                    if file.endswith('.txt'):
                        zip_file.write(os.path.join(path, file),os.path.join('input', file), compress_type=zipfile.ZIP_DEFLATED)
            for (path, dir, files) in os.walk(f"{os.getenv('TASK_PATH')}{str(task_id)}/output/"):
                for file in files:
                    if file.endswith('.txt'):
                        zip_file.write(os.path.join(path, file),os.path.join('output', file), compress_type=zipfile.ZIP_DEFLATED)
            zip_file.close()
            return {'code': 1}
 
def ask_ai(prompt, template):
    openai.api_key = config.CHATGPT_KEY
    # completion = openai.Completion.create(
    # engine='text-davinci-003'  # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
    # , prompt=prompt
    # , temperature=0.5
    # , max_tokens=1024
    # , top_p=1
    # , frequency_penalty=0
    # , presence_penalty=0)
    # return completion['choices'][0]['text']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": template
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


task_template = '''
    당신은 알고리즘 문제 생성가입니다.
    당신은 알고리즘 문제를 만들고, 알고리즘에 관한 정보를 다음과 같은 형식으로 제공합니다.
    {
        "problem": {
            "title": "<문제 제목>",
            "description": "<문제 설명>",
            "input": {
                "description": "<입력 설명>"
            },
            "output": {
                "description": "<출력 설명>"
            },
            "examples": [
                {
                    "input": "<공백으로 구분된 입력 예시>",
                    "output": "<출력 예시>"
                },
                {
                    "input": "<공백으로 구분된 입력 예시>",
                    "output": "<출력 예시>"
                }
            ]
        },
        "constraints": {
            "memory": "<메모리 제약 조건>",
            "time": "<시간 제약 조건>"
        },
        "code" : {
            "code": "<줄바꿈으로 구분된 파이썬 정답 코드>"
        }
    }
    '''
tc_template = '''
    당신은 알고리즘 문제 테스트 케이스 생성가입니다.
    당신은 알고리즘 문제에 대한 설명을 읽고, 
    그에 해당하는 테스트 케이스를 다음과 형식으로 20개 제공합니다.

    {
        "testcase": [ 
            { 
                "input": "<공백으로 구분된 입력 예시>",
                "output": "<입력에 대한 출력>"
            }
        ]
    }   
'''

