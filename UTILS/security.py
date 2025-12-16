import hashlib

class Security:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_password(stored_hash, password):
        return stored_hash == Security.hash_password(password)