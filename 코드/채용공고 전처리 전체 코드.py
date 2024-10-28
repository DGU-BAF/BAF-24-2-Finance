import pandas as pd
import re

data = pd.read_csv('WANTED_EDA/원티드_채용공고_결측치처리.csv')
print(data.head())

# 채용 전형 전처리
# 채용 전형에서 추출할 단어 리스트 정의
selection_steps = [
    '서류 전형', '화상 인터뷰', '실무 인터뷰', '컬쳐핏 인터뷰', '최종 합격', '서류심사', '대면 인터뷰',
    '실무인터뷰', '1차 인터뷰', '2차 인터뷰', '3차 인터뷰', '직무 인터뷰', '최종 인터뷰', '처우 협의',
    '1차 면접', '2차 면접', '레퍼런스 체크', '서류심사', '온라인역량(인성)검사', '합격자발표', '처우 협의',
    '대면 면접', '최종 결과 안내', '지원서 접수', '직무적합성 인터뷰', '문화적합성 인터뷰', '전화 인터뷰',
    '실무진면접', '종합 인터뷰', '입사', '출근일자협의', '심층 면접', '합격', '조직장 면접', '경영진 면접', '상시채용',
    '온라인 면접', '팀리더 면접', '대표이사 면접', '과제전형', '인적성 전형', '시용', '평판 조회', '이력서', '서류전형',"출근일자", "급여"
]


# 채용 전형에서 단어 추출 및 결측치 처리 함수 정의
def extract_steps(text):
    extracted_steps = []
    for step in selection_steps:
        # 띄어쓰기를 무시하고 단어를 찾기 위해 정규 표현식을 사용
        if re.search(step.replace(" ", ""), text.replace(" ", "")):
            extracted_steps.append(step)

    # 단어가 하나도 추출되지 않았을 때 '개별 문의' 반환
    return ', '.join(extracted_steps) if extracted_steps else '개별 문의'


# 채용 전형 열에서 단어 추출 및 결측치 처리
data['채용 전형'] = data['채용 전형'].apply(extract_steps)

# 결과 확인
print(data)


# 혜택 및 복지
from summa.summarizer import summarize


# 혜택 및 복지 요약 함수 정의
def summarize_benefits(text, ratio=0.5):
    if isinstance(text, str):
        # 채용 전형 크롤링된 거 삭제
        for step in selection_steps:
            text = re.sub(r'[^.]*?' + re.escape(step) + r'[^.]*\.', '', text)

        # 링크 삭제
        text = re.sub(r'http[s]?://\S+', '', text)

        # []와 <> 안의 텍스트 삭제
        text = re.sub(r'\[.*?\]', '', text)  # [] 안의 텍스트 삭제
        text = re.sub(r'<.*?>', '', text)  # <> 안의 텍스트 삭제
        text = re.sub(r'".*?"', '', text)  # "" 안의 텍스트 삭제

        # 공백으로 시작하거나 끝나는 경우 제거
        text = text.strip()

        if text:  # 요약할 내용이 있을 경우
            summary = summarize(text, ratio=ratio)  # ratio를 사용하여 요약
            if summary:  # 요약이 비어있지 않은 경우
                summary = summary.strip()
                summary = re.sub(r'(입니다|합니다|해드립니다|해 주세요|할 수 있어요|해요|!|해 드려요|해 드립니다)', '', summary)  # 불필요한 표현 제거
                summary = summary.strip()  # 여백 제거
                summary = summary.replace('습니다', '음')
                summary = summary.replace('있어요', '있음')
                summary = summary.replace('만듭니다', '만듦')
                summary = summary.replace('할 수 있습니다', '할 수 있음')
                summary = summary.replace('.', '')
                summary = summary.replace('=', '')
                summary = summary.replace('▷', '•')
                summary = summary.replace('-', '•')
                summary = summary.replace('*', '•')
                summary = summary.replace('o', '•')
                summary = summary.replace('5)', '•')
                summary = summary.replace('7)', '•')
                summary = summary.replace('••', '')
                summary = re.sub(r'<.*?>', '', summary)

                # 문장이 여러 개일 경우 각각 앞에 • 추가
                sentences = summary.split('•')  # 기존의 •로 나누기
                formatted_summary = []

                for sentence in sentences:
                    sentence = sentence.strip()  # 문장 앞뒤 공백 제거
                    if sentence:  # 비어 있지 않은 경우
                        # 문장이 •로 시작하지 않으면 • 추가
                        if not sentence.startswith('•'):
                            formatted_summary.append('• ' + sentence)
                        else:
                            formatted_summary.append(sentence)

                return ' '.join(formatted_summary)  # 문장들을 공백으로 연결하여 반환

        return '명시되어 있지 않음'  # 요약할 내용이 없으면 반환
    return '명시되어 있지 않음'  # 결측치가 있을 경우 처리

# 혜택 및 복지 열에서 요약 수행
data['혜택 및 복지'] = data['혜택 및 복지'].apply(lambda x: summarize_benefits(x, ratio=0.5))


# 우대사항 전처리 함수 정의
def summarize_benefits(text, ratio=1):
    # 텍스트가 문자열이 아니거나 결측치일 경우 '명시되어 있지 않음' 반환
    if not isinstance(text, str) or pd.isna(text):
        return '명시되어 있지 않음'

    # '지원' 또는 '제공'이 포함된 경우 결측치 처리
    if '지원' in text or '제공' in text:
        return '명시되어 있지 않음'

    # 링크 삭제
    text = re.sub(r'http[s]?://\S+', '', text)

    # []와 <> 안의 텍스트 삭제
    text = re.sub(r'\[.*?\]', '', text)  # [] 안의 텍스트 삭제
    text = re.sub(r'<.*?>', '', text)  # <> 안의 텍스트 삭제
    text = re.sub(r'".*?"', '', text)  # "" 안의 텍스트 삭제
    text = re.sub(r'#.*?', '', text)  # #으로 시작하는 텍스트 삭제

    # 숫자 목록 형식 대체
    text = re.sub(r'\d+\.', '•', text)  # 숫자. 형식
    text = re.sub(r'\d+\)', '•', text)  # 숫자) 형식

    # 공백으로 시작하거나 끝나는 경우 제거
    text = text.strip()

    if text:  # 요약할 내용이 있을 경우
        summary = summarize(text, ratio=ratio)  # ratio를 사용하여 요약
        if summary:  # 요약이 비어있지 않은 경우
            summary = summary.strip()
            summary = re.sub(r'(입니다|합니다|해드립니다|해 주세요|할 수 있어요|해요|!|해 드려요|해 드립니다|이런 분이면 더 좋아요|이런 분이라면 더 좋아요)', '', summary)  # 불필요한 표현 제거
            summary = summary.strip()  # 여백 제거
            summary = summary.replace('습니다', '음')
            summary = summary.replace('있어요', '있음')
            summary = summary.replace('만듭니다', '만듦')
            summary = summary.replace('할 수 있습니다', '할 수 있음')
            summary = summary.replace('*', '•')
            summary = summary.replace('.', '')
            summary = summary.replace('■', '•')
            summary = summary.replace('=', '')
            summary = summary.replace('-', '•')
            summary = summary.replace('·', '•')

            # 문장이 여러 개일 경우 각각 앞에 • 추가
            sentences = summary.split('•')  # 기존의 •로 나누기
            formatted_summary = []

            for sentence in sentences:
                sentence = sentence.strip()  # 문장 앞뒤 공백 제거
                if sentence:  # 비어 있지 않은 경우
                    # 문장이 •로 시작하지 않으면 • 추가
                    if not sentence.startswith('•'):
                        formatted_summary.append('• ' + sentence)
                    else:
                        formatted_summary.append(sentence)

            return ' '.join(formatted_summary)  # 문장들을 공백으로 연결하여 반환

        return '명시되어 있지 않음'  # 요약할 내용이 없으면 반환
    return '명시되어 있지 않음'  # 결측치가 있을 경우 처리


# 우대사항 열에서 요약 수행
data['우대사항'] = data['우대사항'].apply(lambda x: summarize_benefits(x, ratio=1))

# 결과 확인
print(data['우대사항'])


# 자격요건 전처리 함수 정의
def summarize_benefits(text, ratio=1):
    # 링크 삭제
    text = re.sub(r'http[s]?://\S+', '', text)

    # []와 <> 안의 텍스트 삭제
    text = re.sub(r'\[.*?\]', '', text)  # [] 안의 텍스트 삭제
    text = re.sub(r'<.*?>', '', text)  # <> 안의 텍스트 삭제
    text = re.sub(r'".*?"', '', text)  # "" 안의 텍스트 삭제
    text = re.sub(r'#.*?', '', text)  # #으로 시작하는 텍스트 삭제

    # 숫자 목록 형식 대체
    text = re.sub(r'\d+\.', '•', text)  # 숫자. 형식
    text = re.sub(r'\d+\)', '•', text)  # 숫자) 형식

    # 공백으로 시작하거나 끝나는 경우 제거
    text = text.strip()

    if text:  # 요약할 내용이 있을 경우
        summary = summarize(text, ratio=ratio)  # ratio를 사용하여 요약
        if summary:  # 요약이 비어있지 않은 경우
            summary = summary.strip()
            summary = re.sub(r'(입니다|합니다|해드립니다|해 주세요|할 수 있어요|해요|!|해 드려요|해 드립니다|이런 분이면 더 좋아요|이런 분과 함께하고 싶어요|이런 분을 찾고 있어요)', '', summary)  # 불필요한 표현 제거
            summary = summary.strip()  # 여백 제거
            summary = summary.replace('습니다', '음')
            summary = summary.replace('있어요', '있음')
            summary = summary.replace('만듭니다', '만듦')
            summary = summary.replace('할 수 있습니다', '할 수 있음')
            summary = summary.replace('*', '•')
            summary = summary.replace('.', '')
            summary = summary.replace('=', '')
            summary = summary.replace('■', '•')
            summary = summary.replace('-', '•')
            summary = summary.replace('·', '•')

            # 문장이 여러 개일 경우 각각 앞에 • 추가
            sentences = summary.split('•')  # 기존의 •로 나누기
            formatted_summary = []

            for sentence in sentences:
                sentence = sentence.strip()  # 문장 앞뒤 공백 제거
                if sentence:  # 비어 있지 않은 경우
                    # 문장이 •로 시작하지 않으면 • 추가
                    if not sentence.startswith('•'):
                        formatted_summary.append('• ' + sentence)
                    else:
                        formatted_summary.append(sentence)

            return ' '.join(formatted_summary)  # 문장들을 공백으로 연결하여 반환

        return '명시되어 있지 않음'  # 요약할 내용이 없으면 반환
    return '명시되어 있지 않음'  # 결측치가 있을 경우 처리


# 자격 요건 열에서 요약 수행
data['자격 요건'] = data['자격 요건'].apply(lambda x: summarize_benefits(x, ratio=1))

# 결과 확인
print(data['자격 요건'])


# 주요 업무 전처리 함수 정의
def summarize_benefits(text, ratio=0.7):
    # 링크 삭제
    text = re.sub(r'http[s]?://\S+', '', text)

    # []와 <> 안의 텍스트 삭제
    text = re.sub(r'\[.*?\]', '', text)  # [] 안의 텍스트 삭제
    text = re.sub(r'<.*?>', '', text)  # <> 안의 텍스트 삭제
    text = re.sub(r'".*?"', '', text)  # "" 안의 텍스트 삭제
    text = re.sub(r'#.*?', '', text)  # #으로 시작하는 텍스트 삭제

    # 숫자 목록 형식 대체
    text = re.sub(r'\d+\.', '•', text)  # 숫자. 형식
    text = re.sub(r'\d+\)', '•', text)  # 숫자) 형식

    # 공백으로 시작하거나 끝나는 경우 제거
    text = text.strip()

    if text:  # 요약할 내용이 있을 경우
        summary = summarize(text, ratio=ratio)  # ratio를 사용하여 요약
        if summary:  # 요약이 비어있지 않은 경우
            summary = summary.strip()
            summary = re.sub(r'(입니다|합니다|해드립니다|해 주세요|할 수 있어요|해요|!|해 드려요|해 드립니다|합류하시면 이렇게 일해요)', '', summary)  # 불필요한 표현 제거
            summary = summary.strip()  # 여백 제거
            summary = summary.replace('습니다', '음')
            summary = summary.replace('있어요', '있음')
            summary = summary.replace('만듭니다', '만듦')
            summary = summary.replace('할 수 있습니다', '할 수 있음')
            summary = summary.replace('*', '•')
            summary = summary.replace('.', '')
            summary = summary.replace('=', '')
            summary = summary.replace('■', '•')
            summary = summary.replace('▷', '•')
            summary = summary.replace('-', '•')
            summary = summary.replace('·', '•')
            summary = summary.replace('••', '')

            # 문장이 여러 개일 경우 각각 앞에 • 추가
            sentences = summary.split('•')  # 기존의 •로 나누기
            formatted_summary = []

            for sentence in sentences:
                sentence = sentence.strip()  # 문장 앞뒤 공백 제거
                if sentence:  # 비어 있지 않은 경우
                    # 문장이 •로 시작하지 않으면 • 추가
                    if not sentence.startswith('•'):
                        formatted_summary.append('• ' + sentence)
                    else:
                        formatted_summary.append(sentence)

            return ' '.join(formatted_summary)  # 문장들을 공백으로 연결하여 반환

        return '명시되어 있지 않음'  # 요약할 내용이 없으면 반환
    return '명시되어 있지 않음'  # 결측치가 있을 경우 처리


# 주요 업무 열에서 요약 수행
data['주요 업무'] = data['주요 업무'].apply(lambda x: summarize_benefits(x, ratio=0.7))

# 결과 확인
print(data['주요 업무'])



# 포지션 상세 전처리 함수 정의
def summarize_benefits(text, ratio=0.5):
    # 링크 삭제
    text = re.sub(r'http[s]?://\S+', '', text)

    # []와 <> 안의 텍스트 삭제
    text = re.sub(r'\[.*?\]', '', text)  # [] 안의 텍스트 삭제
    text = re.sub(r'<.*?>', '', text)  # <> 안의 텍스트 삭제
    text = re.sub(r'".*?"', '', text)  # "" 안의 텍스트 삭제
    text = re.sub(r'#.*?', '', text)  # #으로 시작하는 텍스트 삭제
    text = re.sub(r'∞.*?', '', text)
    text = re.sub(r'【.*?】', '', text)

    # 숫자 목록 형식 대체
    text = re.sub(r'\d+\.', '•', text)  # 숫자. 형식
    text = re.sub(r'\d+\)', '•', text)  # 숫자) 형식

    # 공백으로 시작하거나 끝나는 경우 제거
    text = text.strip()

    if text:  # 요약할 내용이 있을 경우
        summary = summarize(text, ratio=ratio)  # ratio를 사용하여 요약
        if summary:  # 요약이 비어있지 않은 경우
            summary = summary.strip()
            summary = re.sub(r'(입니다|합니다|해드립니다|해 주세요|할 수 있어요|해요|!|해 드려요|해 드립니다|회사 소개)', '', summary)  # 불필요한 표현 제거
            summary = summary.strip()  # 여백 제거
            summary = summary.replace('습니다', '음')
            summary = summary.replace('있어요', '있음')
            summary = summary.replace('만듭니다', '만듦')
            summary = summary.replace('할 수 있습니다', '할 수 있음')
            summary = summary.replace('*', '•')
            summary = summary.replace('.', '')
            summary = summary.replace('=', '')
            summary = summary.replace('■', '•')
            summary = summary.replace('▷', '•')
            summary = summary.replace('-', '•')
            summary = summary.replace('·', '•')
            summary = summary.replace('••', '')
            summary = summary.replace('|', '')

            # 문장이 여러 개일 경우 각각 앞에 • 추가
            sentences = summary.split('•')  # 기존의 •로 나누기
            formatted_summary = []

            for sentence in sentences:
                sentence = sentence.strip()  # 문장 앞뒤 공백 제거
                if sentence:  # 비어 있지 않은 경우
                    # 문장이 •로 시작하지 않으면 • 추가
                    if not sentence.startswith('•'):
                        formatted_summary.append('• ' + sentence)
                    else:
                        formatted_summary.append(sentence)

            return ' '.join(formatted_summary)  # 문장들을 공백으로 연결하여 반환

        return '명시되어 있지 않음'  # 요약할 내용이 없으면 반환
    return '명시되어 있지 않음'  # 결측치가 있을 경우 처리


# 포지션 상세 열에서 요약 수행
data['포지션 상세'] = data['포지션 상세'].apply(lambda x: summarize_benefits(x, ratio=0.5))

# 결과 확인
print(data['포지션 상세'])

# 데이터 저장
data.to_csv('WANTED_EDA/채용공고_전처리.csv', index=False, encoding='utf-8-sig')

