import main
import pytest
import os
import sqlite3

# Fixture to initialize the main.encode_decode class instance
@pytest.fixture
def user_database_instance():
    test_name_database = "test/test_database"
    instance = main.user_database(test_name_database)
    return instance

class encode_decode_Tests:

    def test_check_database_file(self, user_database_instance):
        expected_file_key = "test/test_database.db"
        assert os.path.exists(expected_file_key), f"File does not exist: {expected_file_key}"

    def test_submit(self, user_database_instance):
        
        test_database = "test/test_database.db"
        test_table = "password_table"
        test_account = "test_account"
        test_username = "test_username"
        test_password = "test_username"

        query = "SELECT 1 FROM password_table WHERE account = ? LIMIT 1"

        user_database_instance.submit(test_account, test_username, test_password)

        conn = sqlite3.connect(test_database)
        cursor = conn.cursor()

        cursor.execute(query, (test_account,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        assert(result)
