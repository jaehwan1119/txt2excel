from glob import glob
import openpyxl
import pandas as pd
import os
import re
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 반복을 줄이기 위한 dictionary 추가함수
def append_dict(result_dict:dict, filename:str, key:str, value:str):
    result_dict['id'].append(filename)
    result_dict['type'].append(key)
    result_dict['output'].append(value)
    result_dict['modify'].append('')
    result_dict['diff_1'].append('')
    result_dict['diff_2'].append('')
    return result_dict

# expression 찾기
def find_pattern(text:str, case:int) -> list:
    # 정규 표현식 패턴
    if case == 0:
        regex = r'<(.*?):expression>' # 부정적 발언
    else:
        regex = r'◀([^◀]+)' # type

    # 검색 (type:list)
    matches = re.findall(regex, text)

    return matches

# dataframe으로부터 데이터를 정제하는 함수
def make_dict(df: pd.DataFrame, filename:str) -> pd.DataFrame:

    # 똑같은 형태의 반복이므로 하드코딩
    idx = ['선택 문장', '부적절 발언', '명시성/비명시성', '긍/부정', '강도', '영역']

    queue = []  # 발견한 expression과 expression의 type을 dictionary로 저장할 queue

    # 결과를 저장할 dict
    result_dict = {
        'id': [],
        'type': [],
        'output': [],
        'modify': [],
        'diff_1': [],
        'diff_2': []
    }

    # dataframe을 list로 변환
    data = []
    for index, row in df.iterrows():
        data.append(row.tolist())

    # form output만들기 + expression 검사 ('◀' 기호 발견 시 queue에 저장 후 다음 라인으로 넘어감)
    form = ''
    prev_s = None
    for l in data:
        for s in l:
            if '◀' in s:
                # 만약 '◀' 기호를 발견했다면 이전 라인에 expression이 있다는 뜻 -> 현재 라인과 이전 라인을 저장
                # exp_list -> expression line
                queue.append({'type_line':s, 'exp_line':prev_s})
                break
            form += s + '\n'
            prev_s = s

    result_dict = append_dict(result_dict, filename, 'form', form)

    # '◀' 기호가 없는 경우 -> expression이 없는 경우 -> 모든 속성이 비어야함
    if not queue:
        for key in idx:
            result_dict = append_dict(result_dict, filename, key, '')

    # '◀' 기호가 있는 경우 -> expression 있음 -> 속성 채워넣어야함
    else:
        insert_list = []

        for qpop in queue: # (qpop type:{'type_line', 'exp_line'} )
            # 선택 문장을 저장할 변수 (type:str)
            sentence = qpop['exp_line']
            insert_list.append(sentence)

            # 부적절 발언을 저장할 변수 (type:str)
            exp_list = ', '.join(find_pattern(sentence, 0))
            insert_list.append(exp_list)

            # type을 저장할 변수 (type:list)
            type_list = find_pattern(qpop['type_line'], 1)
            insert_list.extend(type_list)

            for key, value in zip(idx, insert_list):
                result_dict = append_dict(result_dict, filename, key, value)
    df = pd.DataFrame(result_dict)

    return df

# Excel파일 작성
def write_excel(df: pd.DataFrame, filename: str, save_path: str) -> None:
    # 파일명 끝에 확장자 없을 경우
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'

    # 저장 경로가 존재하지 않으면 생성
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 전체 파일 경로
    file_path = os.path.join(save_path, filename)

    # 파일이 이미 존재한다면 기존 파일에 이어서 저장
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(file_path, index=False, engine='openpyxl')
    else:
        # 파일이 존재하지 않으면 새 파일 생성
        df.to_excel(file_path, index=False, engine='openpyxl')


