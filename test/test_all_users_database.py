import main
import pytest
import os
import sqlite3


# Fixture to initialize the main.encode_decode class instance
@pytest.fixture(scope='class')
def users_database_instance():
    test_name_database = "test/all_user_database_test"
    instance = main.all_users_database(test_name_database)
    return instance


@pytest.mark.users_database
class user_DB_Tests:

    def test_check_database_files(self, users_database_instance):
        expected_file_key = "test/all_user_database_test.txt"
        expected_file_db = "test/all_user_database_test.db"
        assert os.path.exists(expected_file_key), f"File does not exist: {expected_file_key}"
        assert os.path.exists(expected_file_db), f"File does not exist: {expected_file_db}"
        
    def test_add_user(self, users_database_instance):
        
        test_database = "test/all_user_database_test.db"
        user_email = "test_username"
        test_user_password = "test_password"

        query = "SELECT 1 FROM all_user WHERE user_email = ? LIMIT 1"

        users_database_instance.add_new_user(user_email, test_user_password)

        conn = sqlite3.connect(test_database)
        cursor = conn.cursor()

        cursor.execute(query, (user_email,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        assert(result)

    def test_look_for_user(self, users_database_instance):
        
        user_email = "test_username"
        incorrect_user_name =  "incorrect_user_name"
        result_positive = users_database_instance.look_for_user(user_email)

        result_negative = users_database_instance.look_for_user(incorrect_user_name)

        if result_positive and not result_negative:
            assert(True)
        else:
            assert(False)

    def test_compare_password(self, users_database_instance):
        
        test_user_email = "test_username"
        test_user_password = "test_password"

        result_positive = users_database_instance.compare_password(test_user_email, test_user_password)

        assert(result_positive)
