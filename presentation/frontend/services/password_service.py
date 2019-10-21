
def validate_pwd(password):
    for token in password:
        if token.isupper() or token.isdigit():
            return True
    return len(password) >= 8