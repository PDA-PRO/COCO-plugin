# Wong Part of Code

### 적용을 위한 추가 설정

- https://github.com/PDA-PRO/COCO_AI 에서 coco-ai 컨테이너 설치
- 도커 네트워크에 wpc 플러그인 추가를 위해 다음 명령어를 실행

```bash
docker network connect coco_network coco-ai
```

- `config.py` 파일의 `WPC_URL` 수정

```python
WPC_URL="http://coco-ai:8000"
```

---

- TC 판별 중 틀린 코드에 대해, 논리적으로 틀린 부분을 찾아 고쳐주는 AI
- 정해진 알고리즘 문제에 대해서만 작동

![image](https://github.com/PDA-PRO/COCO-plugin/assets/80380576/4b0fd0a5-c207-4e56-84a3-4bed2da2bf96)

#### 설정값

- WPC_URL : WPC url 필요
