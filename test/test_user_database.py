import main
import pytest
import os
import sqlite3


# Fixture to initialize the main.encode_decode class instance
@pytest.fixture(scope='class')
def user_database_instance():
    test_name_database = "test/test_database"
    instance = main.user_database(test_name_database)
    return instance

@pytest.mark.user_database
class encode_decode_Tests:

    def test_check_database_files(self, user_database_instance):
        expected_file_key = "test/test_database.txt"
        expected_file_db = "test/test_database.db"
        assert os.path.exists(expected_file_key), f"File does not exist: {expected_file_key}"
        assert os.path.exists(expected_file_db), f"File does not exist: {expected_file_db}"

    def test_submit(self, user_database_instance):
        
        test_database = "test/test_database.db"
        test_account = "test_account"
        test_username = "test_username"
        test_password = "test_password"

        query = "SELECT 1 FROM password_table WHERE account = ? LIMIT 1"

        user_database_instance.submit(test_account, test_username, test_password)

        conn = sqlite3.connect(test_database)
        cursor = conn.cursor()

        cursor.execute(query, (test_account,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        assert(result)

    def test_update(self, user_database_instance):
        
        test_database = "test/test_database.db"
        test_account_original = "test_account_original"
        test_username_original = "test_username_original"
        test_password_original = "test_password_original"
            
        test_username_update = "test_username_update"
        test_password_update = "test_password_update"


        query = "SELECT 1 FROM password_table WHERE user_email = ? LIMIT 1"

        user_database_instance.submit(test_account_original, test_username_original, test_password_original)
        user_database_instance.update(test_account_original, test_username_update, test_password_update)

        conn = sqlite3.connect(test_database)
        cursor = conn.cursor()

        cursor.execute(query, (test_username_update,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        assert(result)

    def test_delete(self, user_database_instance):
        
        test_database = "test/test_database.db"
        test_account_delete = "test_account_delete"
        test_username_delete = "test_username_delete"
        test_password_delete = "test_password_delete"
            
        query = "SELECT 1 FROM password_table WHERE user_email = ? LIMIT 1"

        user_database_instance.submit(test_account_delete, test_username_delete, test_password_delete)
        user_database_instance.delete(test_account_delete)

        conn = sqlite3.connect(test_database)
        cursor = conn.cursor()

        cursor.execute(query, (test_account_delete,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        assert(not(result))
