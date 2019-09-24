
def assemble_err_msg(id, options, name):
    if options == "NOT_FOUND":
        return name + " with id " + id + " not found in database."
    elif options == "WRONG_REQUEST_METHOD":
        return "Wrong request method. Request method must be " + name 
        