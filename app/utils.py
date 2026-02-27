from passlib.context import CryptContext
# password security
pwd_context= CryptContext(schemes=["argon2","bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)