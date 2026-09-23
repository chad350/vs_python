import os
import tempfile
import unittest


class TestFileProcessor(unittest.TestCase):

    def setUp(self):
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
        temp.close()
        self.file_path = temp.name
        print(f"\n📁 setUp: 임시 파일 생성 - {self.file_path}")

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        print(f"🗑️ tearDown: 임시 파일 삭제 - {self.file_path}")

    def test_write_and_read(self):
        """파일 쓰기/읽기 테스트"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("레벨 10 달성")
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "레벨 10 달성")

    def test_append(self):
        """파일 추가 쓰기 테스트"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("첫째 기록\n")
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write("둘째 기록\n")
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 2)


if __name__ == '__main__':
    unittest.main()