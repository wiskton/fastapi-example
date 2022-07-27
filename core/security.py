from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(password: str, hash_password: str) -> bool:
    """
    function checks if the password is correct
    """
    return CRIPTO.verify(password, hash_password)


def generate_hash_password(password: str) -> str:
    """
    generate new hash password
    """
    return CRIPTO.hash(password)