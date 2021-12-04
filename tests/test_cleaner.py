# import os
# import sys
#
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.anki.Cleaner import Cleaner
import pytest



@pytest.fixture
def cleaner():
    return Cleaner('name')


def test_clean_line(cleaner):
    assert 'nine rings' == cleaner.clean_line_regexp('...nine rings...')
