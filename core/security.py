from passlib.context import CryptContext

#Sistema de criptografia usado para as senhas
CRYPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return CRYPTO.verify(plain_password, hashed_password)

def generate_password_hash(password: str) -> str:
    return CRYPTO.hash(password)
