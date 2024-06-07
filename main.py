from txt2excel import *

start_time = time.time()

# 저장된 디렉토리를 불러오기
dir_path = '/Users/dataly/Desktop/E'
save_path = '/Users/dataly/Desktop/E'
new_file = []

# 텍스트파일 리스트 불러오기
txt_file = [f for f in os.listdir(dir_path) if f.endswith('.txt')]
# g_txt_file = [glob(dir_path, recursive=False)]
# print(type(g_txt_file))
# print(g_txt_file)
print(txt_file)

# 불러온 텍스트파일 리스트를 통해 file 단위로 순회
for file in txt_file:
    read_txt = os.path.join(dir_path, file)
    df = pd.read_csv(read_txt, delimiter='\t', header=None)

    filename = os.path.splitext(file)[0]
    new_dict = make_dict(df, filename)
    # write_excel(new_dict, 'result_excel.xlsx', save_path)

end_time = time.time()
print(end_time - start_time)