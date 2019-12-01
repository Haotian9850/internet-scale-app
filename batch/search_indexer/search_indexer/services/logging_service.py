

def log_pet_views(view):
    log_file1 = open("/app/pet_view_log.txt", "a+")
    log_file1.write(assemble_log_entry(view))
    log_file1.close()
    log_file2 = open("/home/whiskey/pet_view_log.txt", "a+")
    log_file2.write(assemble_log_entry(view))
    log_file2.close()
    
    

def assemble_log_entry(view):
    return "{}:{}\n".format(
        view["username"],
        view["pet_id"]
    )

def parse_pet_log():
    result = {}
    with open("/app/pet_view_log.txt") as log:
        lines = log.readlines()
    for line in lines:
        result[line.split(":")[1].rstrip()] = result.get(line.split(":")[1].rstrip(), 0) + 1
    return result



'''
view = {
    "username": hao,
    "pet_id": 1
}
'''
