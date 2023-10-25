from fastapi import Depends
from app.api.deps import get_cursor
from app.db.base import DBCursor
from app.plugin.interface import AbstractPlugin
from . import config

class Plugin(AbstractPlugin):
    '''
    플러그인 클래스  
    클래스의 이름을 바꾸지 않도록 주의합니다.

    ai 플러그인의 데이터를 저장해야한다면 세부구현이 필요한 내부클래스
    - `TableModel` : `AbstractPlugin.AbstractTable`을 상속하는 클래스로써 ai플러그인 db 저장소 정의

    정의가 필요한 클래스변수
    - `router_path` : ai플러그인 엔드포인트 접두사
    - `feature_docs` : 플러그인의 간략한 설명
    - `base` : ai 플러그인일 경우 모델 정보

    세부구현이 필요한 함수
    - `test` : ai플러그인 테스트
    - `endpoint_main` : ai플러그인 메인동작
    '''
    router_path=''
    feature_docs=''
    base=''
    
    class TableModel(AbstractPlugin.AbstractTable):
        '''
        ai 플러그인의 테이블 스키마 명시
        예시, ::

          #클래스 명과 상속 클래스 고정
          class TableModel(AbstractPlugin.AbstractTable):
              __key__='sub_id' #다중키일 경우 ['sub_id','status'] *필수
              __tablename__='wpc' #테이블이름 *필수
              sub_id:int #속성이름:속성타입 속성타입은 str과 int만 가능
              status:int
              result:str
              ...

        '''
        __key__=''
        __tablename__=''
        
    @staticmethod
    def test():
        '''
        ai 플러그인이 사용가능한지 테스트

        -----------------------------
        returns
        - 사용가능하지 않다면 `False`, 사용가능하다면 `True`
        '''
        return True
        
    @staticmethod
    def endpoint_main(db_cursor:DBCursor=Depends(get_cursor)):
        '''
        ai 플러그인의 메인 동작을 구현
        endpoint 접두사는 꼭 필요합니다.
        Plugin.enable_onoff(db_cursor)를 사용하여 런타임중 엔드포인트를 비활성화 할 수 있습니다.
        -----------------------------
        params
        - db_cursor : db에 조작을 위한 cursor
        '''
        Plugin.enable_onoff(db_cursor)