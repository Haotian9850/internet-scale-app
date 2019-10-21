
def validate_pwd(password):
    if len(password) < 8:
        return False
    containsUppercase = False 
    containsNumber = False
    for token in password:
        if token.isupper():
            containsUppercase = True 
        if token.isdigit():
            containsNumber = True 
    return containsNumber and containsUppercase