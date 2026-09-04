from pathlib import Path
# 1. 지금 작업 폴더를 절대경로로 표현
print(Path.cwd())
# 2. 홈 디렉토리를 절대경로로 표현
print(Path.home())

# 3. config 폴더 안에 setting.json - Path 객체로 만들어 출력
setting_path = Path() / "chater" / "0904" / "qa_practice" / "config" / "setting.json"


# 4. testdata/android/build_1.2.0/log.txt - Path 객체로 만들기
log_path = Path() / "chater" / "0904" / "qa_practice" / "testdata" / "android" / "build_1.2.0" / "log.txt"

# 5. log 경로를 기반으로 아래처럼 문구 출력

print(f"파일을 찾았습니다! : {log_path.name}")
print(f"저장된 폴더 : {log_path.parent.name}")
print(f"파일 이름은 : {log_path.stem}")
print(f"확장자 : {log_path.suffix}")

# 파일을 찾았습니다! : log.txt
# 저장된 폴더 : build_1.2.0
# 파일 이름은 : log
# 확장자 : .txt