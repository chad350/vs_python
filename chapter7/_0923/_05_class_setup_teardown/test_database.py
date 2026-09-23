import unittest


class FakeDatabase:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n🔧 setUpClass: 데이터베이스 연결")
        cls.db = FakeDatabase()
        cls.db.connect()

    @classmethod
    def tearDownClass(cls):
        cls.db.disconnect()
        print("🔧 tearDownClass: 데이터베이스 연결 해제")

    def setUp(self):
        print("  📝 setUp: 트랜잭션 시작")
        self.rows = []

    def tearDown(self):
        self.rows = []
        print("  📝 tearDown: 트랜잭션 롤백")

    def test_insert(self):
        print("   테스트: INSERT")
        self.rows.append("user1")
        self.assertEqual(len(self.rows), 1)

    def test_select(self):
        print("   테스트: SELECT")
        self.assertTrue(self.db.connected)

    def test_update(self):
        print("   테스트: UPDATE")
        self.rows.append("user1")
        self.rows[0] = "user2"
        self.assertEqual(self.rows[0], "user2")


if __name__ == '__main__':
    unittest.main()