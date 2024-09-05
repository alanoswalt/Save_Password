import main
import pytest
import os

# Fixture to initialize the main.encode_decode class instance
# Fixture here and not un conftest because of clarity
#Scope class because we want the sabe instance for all test in the class
@pytest.fixture(scope='class')
def encode_decode_instance():
    test_file_key = "test/test_file_key"
    instance = main.encode_decode(test_file_key)
    return instance

@pytest.mark.encode_decode
class encode_decode_Tests:

    def test_check_or_create_key(self, encode_decode_instance):
        expected_file_key = "test/test_file_key.txt"
        assert os.path.exists(expected_file_key), f"File does not exist: {expected_file_key}"

    def test_encode_decode(self, encode_decode_instance):
        
        expected_return_text = "Hello"

        text = "Hello"
        #Esto lo puedo hacer un fixture?
        encode_return_text = encode_decode_instance.encode(text)
        decode_return_text = encode_decode_instance.decode(encode_return_text)

        
        assert (expected_return_text == decode_return_text), f"Encode incorrect, expected {expected_return_text}, real return: {decode_return_text}"
