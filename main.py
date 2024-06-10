from txt2excel import *

start_time = time.time()

# 저장된 디렉토리를 불러오기
dir_path = '/Users/dataly/Desktop/E'
save_path = '/Users/dataly/Desktop/E'
new_file = []

# 텍스트파일 리스트 불러오기
txt_file = [f for f in os.listdir(dir_path) if f.endswith('.txt')]
txt_file.sort()
# g_txt_file = [glob(dir_path, recursive=False)]

# 최종 dictionary
result_dict = pd.DataFrame()

# 불러온 텍스트파일 리스트를 통해 file 단위로 순회
for file in txt_file:
    read_txt = os.path.join(dir_path, file)
    df = pd.read_csv(read_txt, delimiter='\t', header=None)

    filename = os.path.splitext(file)[0]
    new_dict = pd.DataFrame(make_dict(df, filename))

    # 파일입출력을 줄이기 위해 result_dict에 데이터를 쌓고
    result_dict = pd.concat([result_dict, new_dict], ignore_index=True)

    # 일정 크기마다 입력
    if (len(result_dict) > 10000):
        write_excel(result_dict, 'result_excel.xlsx', save_path)
        result_dict = pd.DataFrame()
# 남은 버퍼 비우기
if not result_dict.empty:
    write_excel(result_dict, 'result_excel.xlsx', save_path)

end_time = time.time()
print(end_time - start_time)