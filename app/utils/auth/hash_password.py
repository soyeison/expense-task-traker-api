import bcrypt


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_passsword: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_passsword.encode("utf-8"), hashed_password.encode("utf-8")
    )
