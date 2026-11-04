import pytest

@pytest.fixture
def admin():
    print("admin - set up")   # 1번
    
    yield "admin data"

    print("admin - tear down")  # 4번   <-   픽스처 사용이 끝나고 실행



def test_one( admin ):
    print("test_one")    # 2번
    print(admin)      # 2번


