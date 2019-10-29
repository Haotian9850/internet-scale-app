import logging 
logging.basicConfig(filename="../pet_view_log.txt", level=logging.INFO)


def log_pet_views(view):
    logger = logging.getLogger("")
    logger.info(assemble_log_entry(view))



def assemble_log_entry(view):
    return "{}:{}".format(
        view["pet_id"],
        view["user_id"]
    )


def parse_pet_log():
    result = {}
    with open("../pet_view_log.txt") as log:
        lines = log.readlines()
    for line in lines:
        result[line.split(":")[2]] = result.get(line.split(":")[2], 0) + 1
    print(result)
    return result



'''
view = {
    "user_id": 29,
    "pet_id": 1
}
'''
