from pathlib import Path

# qa_practice/reports - iterdir()
p = Path("qa_practice/reports")
for f in p.iterdir():
    print(f.name)


# android - build_1.2.3 폴더 생성  - mkdir
# Path("qa_practice/testdata/android/build_1.2.3").mkdir(exist_ok=True)
# note.txt 빈 파일 만들기            - touch
# Path("qa_practice/testdata/android/build_1.2.3/note.txt").touch()
# note.txt 지우기                  - unlink
# Path("qa_practice/testdata/android/build_1.2.3/note.txt").unlink()
# build_1.2.3 폴더 지우기           - rmdir
Path("qa_practice/testdata/android/build_1.2.3").rmdir()