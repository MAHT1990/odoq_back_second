# odoq_back_second
odoq second backend

## odoq second backend 초기 세팅
### 가상환경 세팅
### CLI 세팅
```bash
# 라이브러리 설치
pip install -r requirements.txt

# 로컬 DB 설정
python manage.py makemigrations
python manage.py migrate

# 로컬 서버 열기
python manage.py runserver
```

## 초기 세팅 이후, 로컬 서버 열기
```bash
python manage.py runserver 
```
