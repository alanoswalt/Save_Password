import logging as log
import os
from cryptography.fernet import Fernet

class encode_decode:
    def __init__(self, name_of_key, base_dir="data/keys", key_path=None) -> None:
        """Create an encoder using a key stored at an explicit or default path.

        ``key_path`` is useful for tests, while the application can continue to
        use the default ``data/keys`` directory.
        """
        self.file_path = key_path or os.path.join(base_dir, f"{name_of_key}.txt")
        self.key = ""
        self.check_or_create_key()

    def encode(self, field):
        fernet = Fernet(self.key)
        encrypted_field = fernet.encrypt(field.encode())
        print(f"Password saved: {encrypted_field}")
        return encrypted_field

    def decode(self, encrypted_field):
        fernet = Fernet(self.key)
        decrypted_field = fernet.decrypt(encrypted_field).decode()    
        return decrypted_field

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return None

    #Escribir la llave en texto, no en binario
    def write_key(self, file_path, data):
        log.info(f"File '{file_path}' does not exist. Creating it...")
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(data.decode())
        log.info(f"File '{file_path}' created with initial data:\n{self.key}") #La imprime en binario

    #Crea la llave en binario
    def create_new_key(self):
        log.info("Creating key")
        key = Fernet.generate_key()
        return key

    def check_or_create_key(self):
         # Check if the file exists
        if os.path.exists(self.file_path):
            self.key = self.read_file(self.file_path).encode()
            if self.key:
                log.info(f"File '{self.file_path}' exists and contains:\n{self.key}")
            else:
                log.warning(f"File '{self.file_path}' exists but is empty.")
        else:
            self.key = self.create_new_key()
            self.write_key(self.file_path, self.key)
