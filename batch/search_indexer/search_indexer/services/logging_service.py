

def log_pet_views(view):
    log_file = open("../../pet_view_log.txt", "a+")
    log_file.write(assemble_log_entry(view))
    log_file.close()
    
    



def assemble_log_entry(view):
    return "{}:{}\n".format(
        view["pet_id"],
        view["username"]
    )


def parse_pet_log():
    result = {}
    with open("../pet_view_log.txt") as log:
        lines = log.readlines()
    for line in lines:
        result[line.split(":")[2]] = result.get(line.split(":")[2], 0) + 1
    return result



'''
view = {
    "username": hao,
    "pet_id": 1
}
'''
