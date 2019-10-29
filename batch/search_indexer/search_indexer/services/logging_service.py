import logging 
logging.basicConfig(filename="../pet_view_log.txt", level=logging.INFO)


def log_pet_views(view):
    logger = logging.getLogger("")
    logger.info(assemble_log_entry(view))



def assemble_log_entry(view):
    return "{}:{}".format(
        view["user_id"],
        view["pet_id"]
    )


view = {
    "user_id": 29,
    "pet_id": 1
}

log_pet_views(view)