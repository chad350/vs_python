# 모듈
from pathlib import Path

print(Path.cwd())  # 작업 디렉토리 [절대경로]
print(Path.home()) # 홈 디렉토리 [절대경로]


p1 = Path()
p2 = Path("chapter4")
p3 = Path("chapter5")
p4 = Path("chapter6")

print(p1)
print(p1.resolve())  # 절대 경로로 바꾸기

print(p2)
print(p2.resolve())  # 절대 경로로 바꾸기

file = p1 / "log.txt"
print(file)

# file_2 = p3 / "0904" / "_01_dictionary.py"
# file_2 = p1 / "chapter5/0904/_01_dictionary.py"
file_2 = p1 / "chapter5" / "0904" / "_01_dictionary.py"

print(file_2)        # chapter5/0904/_01_dictionary.py
print(file_2.name)   # _01_dictionary.py
print(file_2.stem)   # _01_dictionary  V
print(file_2.suffix) # .py  V

print(file_2.parent) # chapter5/0904 V
print(file_2.parts)  # ('chapter5', '0904', '_01_dictionary.py')


# 파일이 존재하는지 확인 
print(Path("chapter5").exists())
print(Path("chapter6").exists())  

# 폴더인지 확인
print(Path("chapter5/0904").is_dir()) 
print(Path("chapter5/0904/_02_file.py").is_dir())

# 파일인지 확인
print(Path("chapter5/0904").is_file())
print(Path("chapter5/0904/_02_file.py").is_file())

p4 = Path("chapter5/0904")
for f in p4.iterdir():
    print(f)

# walk
# listdir

# mkdir - 디렉토리를 만드는 기능
# parents
#    T - 중간에 빠진 경로가 있어도 처리 (없는 폴더까지 만들어 준다)
#    F - 준간에 빠진 경로가 있으면 에러
# exist_ok
#    T - 이미 해당 폴더가 존재해도 통과
#    F - 이미 해당 폴더가 존재하면 에러
Path("chapter5/0904/folder/test_newfolder").mkdir(parents=True, exist_ok=True)

Path("test.txt").touch() # 빈 파일 만들기

# 지우는 것
Path("test_log.txt").unlink() # 파일 지우기
Path("chapter5/0904/qa_practice").rmdir() # 폴더 지우기 - 빈 폴더만 지울수 있다.

Path("items.csv").replace("item_test.csv") # 이름 바꾸기 - 같은 경로에서 진행
Path("item_test.csv").replace("test/item_test.csv") # 파일 옮기기 - 다른 경로를 지정

import shutil

shutil.copytree("chapter5/0904/qa_practice","chapter5/0904" , dirs_exist_ok= True) # 폴더를 전부 옮기기 
shutil.rmtree("chapter5/0904/qa_practice") # 폴더를 전부 삭제