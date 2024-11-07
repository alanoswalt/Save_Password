import main
import pytest
import os
import sqlite3


# Fixture to initialize the main.encode_decode class instance
@pytest.fixture(scope='class')
def users_database_instance():
    test_name_database = "test/all_user_test"
    instance = main.user_database(test_name_database)
    return instance


@pytest.mark.users_database
class user_DB_Tests:

    def test_check_database_files(self, users_database_instance):
        expected_file_key = "test/all_user_test.txt"
        expected_file_db = "test/all_user_test.db"
        assert os.path.exists(expected_file_key), f"File does not exist: {expected_file_key}"
        assert os.path.exists(expected_file_db), f"File does not exist: {expected_file_db}"
        