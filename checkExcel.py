from txt2excel import *
import numpy as np


def checkIntegrity(new_txt_dict: dict, new_excel_dict: dict) -> None:
    global idx
    for i in range(len(new_txt_dict['id'])):
        for type in dict_type:
            # 만약 txt와 excel의 내용이 맞지 안는 경우 위치와 내용 표시
            if new_txt_dict[type][i] != new_excel_dict[type][idx]:
                print('='*50)
                print(f"[Error Loaction: {new_txt_dict['id'][0]}")
                print('[Error Detail: new_txt_dict]')
                print(new_txt_dict[type][i])
                print('[Error Detail: new_excel_dict]')
                print(new_excel_dict[type][idx])
                print('=' * 50)
                print()
        idx += 1
    return None

dict_type = ['id', 'type', 'output', 'modify', 'diff_1', 'diff_2']
dir_path = '/Users/Dataly/Desktop/E/'
excel_name = 'result_excel.xlsx'

# new_excel 순회를 위한 전역변수
idx=0

# excel파일의 DataFrame
excel_df = pd.read_excel(dir_path + excel_name, dtype=str)

# excel에서 데이터를 읽어올 때 빈 칸의 nan을 ''로 교체
excel_df = excel_df.replace(np.nan, '', regex=True)
new_excel_dict = excel_df.to_dict(orient='dict')

# 텍스트파일 리스트 불러오기
txt_file = [f for f in os.listdir(dir_path) if f.endswith('.txt')]
txt_file.sort()

for file in txt_file:
    read_txt = os.path.join(dir_path, file)
    df = pd.read_csv(read_txt, delimiter='\t', header=None)

    filename = os.path.splitext(file)[0]
    new_txt_dict = make_dict(df, filename)

    checkIntegrity(new_txt_dict, new_excel_dict)
