from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Function to hash passwords and verify"""
def password_hash(password: str):
    return pwd_context.hash(password)

def password_verify(plain_password: str, password: str):
    return pwd_context.verify(plain_password, password)

