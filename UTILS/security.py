import hashlib

class Security:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_password(stored_hash, input_password):
        return stored_hash == hashlib.sha256(input_password.encode('utf-8')).hexdigest()