# COCO-plugin

한국어|[English](https://github.com/PDA-PRO/COCO-plugin/blob/main/README.eng.md)  
AI 문제 생성, AI 답변 생성 등 AI를 활용한 다양한 확장 기능을 플러그인으로 간편하게 적용해보세요  
새로운 플러그인을 개발하고 싶다면 https://github.com/PDA-PRO/COCO-plugin/blob/main/README.develop.md 를 참고해주세요

## COCO에 추가할 수 있는 플러그인 목록

- [AI 답변 생성](https://github.com/PDA-PRO/COCO-plugin/tree/main/answer_generation)
- [코드 클러스터](https://github.com/PDA-PRO/COCO-plugin/tree/main/code_cluster)
- [AI 코드 개선](https://github.com/PDA-PRO/COCO-plugin/tree/main/code_improvement)
- [AI 문제 생성](https://github.com/PDA-PRO/COCO-plugin/tree/main/problem_generation)
- [Wong Part of Code](https://github.com/PDA-PRO/COCO-plugin/tree/main/wpc) **적용을 위해 추가 설정이 필요합니다. 링크를 방문하여 추가설정을 해주세요**

## 전제 조건

### COCO 설치

https://github.com/PDA-PRO/COCO-deploy
참고하여 설치  
기본적으로 `plugin` 폴더는 `docker up`이 실행된 경로에 존재합니다.

## 플러그인 적용하기

### Linux

- System: Ubuntu 20.04.6 LTS

#### 플러그인 목록 다운

```bash
git clone https://github.com/PDA-PRO/COCO-plugin.git
cd COCO-plugin
```

#### 원하는 플러그인 폴더를 `plugin` 폴더로 이동

```bash
cp -r <플러그인폴더> <plugin 폴더 경로>/<플러그인폴더>
```

#### 백엔드 컨테이너 재시작

```bash
docker container restart coco_backend
```

### Windows

- System: Windows 10

#### 플러그인 목록 다운

```bash
git clone https://github.com/PDA-PRO/COCO-plugin.git
cd COCO-plugin
```

#### 원하는 플러그인 폴더를 `plugin` 폴더로 이동

#### 백엔드 컨테이너 재시작

```bash
docker container restart coco_backend
```

## 사용하기

#### 관리자 페이지의 AI PLUGINS 메뉴

![manage](https://github.com/PDA-PRO/COCO-plugin/assets/80380576/cc8fcf7a-d4c8-4152-a206-107817fcf003)

- 적용된 플러그인의 백엔드와 프론트엔드의 상태를 확인 가능
- 플러그인의 엔드포인트 On/Off 가능

## FAQ

### 올바르지 않는 플러그인 추가

`new_plugin_temp` 템플릿을 플러그인으로 추가할 경우 오류가 발생합니다.

### 해결 방법

`new_plugin_temp` 템플릿을 플러그인 폴더에서 제거합니다.

------------
### 플러그인 종속 패키지 설치 오류

플러그인의 상태가 모두 `enable`이지만 패키지가 없다는 오류가 발생할 경우

### 해결 방법

`plugin` 폴더의 각 플러그인에서 `.cache` 파일을 삭제합니다  
이후 백엔드를 재시작합니다.
```bash
docker container restart coco_backend
```
## 라이선스

[Apache2.0](https://www.apache.org/licenses/LICENSE-2.0)
