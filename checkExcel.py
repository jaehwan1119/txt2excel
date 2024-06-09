from txt2excel import *
import numpy as np

# def matching:

def checkIntegrity(txtDF: pd.DataFrame, excelDF: pd.DataFrame) -> list:
    dict_type = ['id', 'type', 'output', 'modify', 'diff_1', 'diff_2']
    dir_path = '/Users/Dataly/Desktop/E/'
    excel_name = 'result_excel.xlsx'

    start_idx = 0
    end_idx = 7

    # excel파일의 DataFrame
    excel_df = pd.read_excel(dir_path + excel_name, dtype=str)

    # excel에서 데이터를 읽어올 때 빈 칸의 nan을 ''로 교체
    excel_df = excel_df.replace(np.nan, '', regex=True)
    new_excel_dict = excel_df.to_dict(orient='dict')

    for i in range(len(excel_df)):
        # idx initialize
        # start_idx(default=0)와 end_idx(default=7)일 때의 id값을 비교해서 같을때(텍스트 파일에 expression이 여러개 있음 -> 길이가 길어져야함)
        if excel_df['id'][start_idx] == excel_df['id'][end_idx]:
            print('[if]')
            print(end_idx)
            end_idx += 6
        # start_idx(default=0)와 end_idx(default=7)일 때의 id값을 비교해서 같지않을때(텍스트 파일에 expression이 여러개 있음 -> 길이가 길어져야함)
        else:
            txt_path = dir_path + excel_df['id'][start_idx] + '.txt'
            txt_file = open(txt_path, 'r')
            txt_df = pd.read_csv(txt_file, delimiter='\t', header=None)
            new_txt_dict = make_dict(txt_df, excel_df['id'][start_idx])

            print('[Excel_dict]')
            print(new_excel_dict)
            print('[txt_dict]')
            print(new_txt_dict)

            # 순회하며 txt와 excel의 데이터가 일치하는지 매칭
            for i in range(start_idx, end_idx):
                for key in dict_type:
                    if new_txt_dict[key][i] != new_excel_dict[key][i]:

                        print('='*50)
                        print('[Error Detail]')
                        print(new_txt_dict[key][i])
                        print(new_excel_dict[key][i])
                        print('=' * 50)


    # excel의 DataFrame에서 id순서대로 txt 파일을 매칭
    txt_file = [f for f in os.listdir(dir_path) if f.endswith('.txt')]

    # 불러온 텍스트파일 리스트를 통해 file 단위로 순회
    for file in txt_file:
        read_txt = os.path.join(dir_path, file)
        txt_df = pd.read_csv(read_txt, delimiter='\t', header=None)
        # print(txt_df)

        filename = os.path.splitext(file)[0]
        new_txt_dict = make_dict(txt_df, filename)
        # print(new_txt_dict)

    return None
a = checkIntegrity(None, None)
