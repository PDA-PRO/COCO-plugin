# COCO 플러그인 개발

한국어|English  
현재 `v1.0.0` 버전에서는 제한적으로만 플러그인을 개발할 수 있습니다.

## 환경 세팅

### 백엔드

[백엔드](https://github.com/PDA-PRO/COCO_Back_End)를 참고하여 자신의 환경에 맞는 백엔드를 설치해주세요

### 프론트엔드

#### 프론트엔드 저장소 복제

```
git clone https://github.com/PDA-PRO/COCO_Front_End.git
cd COCO_Front_End/coco
```

#### 프론트엔드 시작

```
npm install
npm start
```

## 개발하기

### 백엔드 API 개발

#### 백엔드 인터페이스 구현

백엔드 설치시 생성된 `plugin` 폴더의 `interfase.py`를 구현하여 플러그인을 개발합니다.

1. 원하는 이름의 플러그인 폴더를 `plugin`폴더에 생성해주세요

```bash
mkdir ./new_plugin
```

2. 새롭게 생성된 플러그인 폴더에 `new_plugin_templat`폴더에 있는 모든 파일을 옮겨주세요

- `config.py` : 플러그인의 설정값을 관리합니다.
- `requirements.txt` : 플러그인의 종속패키지를 관리합니다.
- `main.py` : 플러그인의 동작, db, 엔드포인드를 관리합니다.
- `README.md` : 플러그인의 간략한 소개문입니다.

3. `main.py` 를 구현합니다.

   1. 플러그인 db 조작

      1. Plugin.read_all(cls,db_cursor:DBCursor)->list

      ```
      ai 플러그인 db 저장소에서 모든 튜플 조회

      params
      - db_cursor : db 조작을 위한 curosor
      ```

      사용예시

      ```python
      - Plugin.read_all(db_cursor)
      ```

      2. Plugin.read(cls,db_cursor:DBCursor,\*\*key):

      ```
      ai 플러그인 db 저장소에서 특정 튜플 조회

      params
      - db_cursor : db 조작을 위한 curosor
      - key : 조회할 튜플의 모든 키값, 만약 키가 2개라면 2개의 키의 값 필요
      ```

      사용예시

      ```python
      - Plugin.read(db_cursor,sub_id=2)#키네임이 sub_id이고 찾는 튜플의 키값이 2인경우
      - Plugin.read(db_cursor,status=2,id=2)#키네임이 sub_id,id이고 찾는 튜플의 키값이 2,2인경우
      ```

      3. Plugin.create(cls,db_cursor:DBCursor,tableModel_obj):

      ```
      ai 플러그인 db 저장소에서 튜플 생성

      params
      - db_cursor : db 조작을 위한 curosor
      - tuple :  Plugin.TableModel 객체
      ```

      사용예시

      ```python
      new_tuple=Plugin.TableModel(sub_id=sub_id,status=4)
      Plugin.create(db_cursor,new_wpc)
      ```

   2. 기존 coco db 조작
      1. https://github.com/PDA-PRO/COCO_Back_End/tree/develop/app/crud 를 참고하여 활용바랍니다.
   3. endpoint 추가  
       아래와 같이 `endpoint`접두사를 가진 새로운 `static`함수를 클래스 내부에 만들경우 `router_path`/`method`의 엔드포인트가 생성됩니다.

      ```python
       @staticmethod
       def endpoint_method():
           pass
      ```

### 프론트엔드 GUI 개발

React JS를 활용하여 컴포넌트를 개발하고 백엔드 API와 연동합니다.
