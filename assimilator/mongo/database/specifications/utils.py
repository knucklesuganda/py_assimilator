

def rename_mongo_id(field: str) -> str:
    return field.replace("id", "_id")


def contains_mongo_id(field: str) -> bool:
    return field.find("id") != -1
