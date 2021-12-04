from src.anki.cleaner import Cleaner
import pytest



@pytest.fixture
def cleaner():
    return Cleaner('name')


def test_clean_line(cleaner):
    assert 'nine rings' == cleaner.clean_line_regexp('...nine rings...')
