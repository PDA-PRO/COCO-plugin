
# COCO-plugin

COCO : Coding Coach - Plugin  
COCO에 추가할 수 있는 플러그인 목록  

## 적용하기
### COCO 설치
https://github.com/PDA-PRO/COCO-deploy
참고하여 설치

### COCO 백엔드 설치 환경이 우분투일 경우
#### 플러그인 목록 다운
```bash
git clone https://github.com/PDA-PRO/COCO-plugin.git
cd COCO-plugin
```

#### 원하는 플러그인을 백엔드 플러그인 폴더로 이동
```bash
cp <플러그인폴더> <coco백엔드플러그인경로>/<플러그인폴더>
```

#### 컨테이너 재시작
```bash
docker compose restart
```

### COCO 백엔드 설치 환경이 윈도우일 경우
#### 플러그인 목록 다운
```bash
git clone https://github.com/PDA-PRO/COCO-plugin.git
cd COCO-plugin
```

#### 원하는 플러그인을 백엔드 플러그인 폴더로 이동


#### 컨테이너 재시작
```powershell
docker compose restart
```

## 사용하기
#### 관리자 페이지의 AI PLUGINS
![manage](https://github.com/PDA-PRO/COCO-plugin/assets/80380576/cc8fcf7a-d4c8-4152-a206-107817fcf003)

* 백엔드와 프론트엔드의 플러그인 상태를 확인 가능
* 플러그인의 엔드포인트 On/Off 가능
