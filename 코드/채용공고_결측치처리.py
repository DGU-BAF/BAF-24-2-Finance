import pandas as pd
import re

data = pd.read_csv('WANTED_EDA/원티드_채용공고_merge.csv')
data = data.drop(['마감일','면접리뷰'], axis=1)
print(data.columns)

print(data[data['회사위치'].isnull()]['회사명'])

# 결측치 회사 위치 회사명에 대해 회사 위치를 업데이트
data.loc[data['회사명'] == "이노케어플러스", '회사위치'] = "서울 서초구"
data.loc[data['회사명'] == "카탈로닉스", '회사위치'] = "서울 서초구"
data.loc[data['회사명'] == "마켓위즈", '회사위치'] = "서울 마포구"
data.loc[data['회사명'] == "에이머슬리", '회사위치'] = "서울 강남구"
data.loc[data['회사명'] == "화승엔지니어링", '회사위치'] = "서울 구로구"
data.loc[data['회사명'] == "넥스트서베이", '회사위치'] = "서울 영등포구"
data.loc[data['회사명'] == "픽셀트라이브", '회사위치'] = "경기 성남시"
data.loc[data['회사명'] == "아이디씨아시아", '회사위치'] = "서울 영등포구"
data.loc[data['회사명'] == "그래비티벤처스", '회사위치'] = "서울 영등포구"
data.loc[data['회사명'] == "컴포즈커피", '회사위치'] = "서울 송파구"
data.loc[data['회사명'] == "이지백", '회사위치'] = "서울 마포구"
data.loc[data['회사명'] == "한국바리스타자격검정협회", '회사위치'] = "서울 마포구"
data.loc[data['회사명'] == "리원컨설팅그룹", '회사위치'] = "서울 강남구"
data.loc[data['회사명'] == "지엘커뮤니케이션즈", '회사위치'] = "서울 강남구"
data.loc[data['회사명'] == "하이마루포토", '회사위치'] = "서울 마포구"
data.loc[data['회사명'] == "오픈드림컴퍼니", '회사위치'] = "서울 종로구"
data.loc[data['회사명'] == "레미유코스메틱", '회사위치'] = "서울 성동구"
data.loc[data['회사명'] == "법률사무소 사유", '회사위치'] = "서울 서초구"
data.loc[data['회사명'] == "도이그로코리아", '회사위치'] = "서울 중구"
data.loc[data['회사명'] == "제이피케어즈", '회사위치'] = "경기 성남시"

# 결측치 확인
print(data.isnull().sum())

# 한국어가 포함된 행만 유지
data = data[data['포지션 상세'].apply(lambda x: bool(re.search(r'[가-힣]', str(x))))]

# 결측치 확인
print(data.isnull().sum())

data['혜택 및 복지'] = data['혜택 및 복지'].fillna(data['우대사항'])
data['채용 전형'] = data['채용 전형'].fillna(data['혜택 및 복지'])

# 결측치 확인
print(data.isnull().sum())

# '태그' 열이 결측치인 행만 제거
data = data.dropna(subset=['태그'])

# 결측치 확인
print(data.isnull().sum())
print(data.info())
print(data)

data.to_csv('WANTED_EDA/원티드_채용공고_merge_2.csv', index=False, encoding='utf-8-sig')
