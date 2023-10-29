import hashlib
from django.conf import settings


def encrypte_data(data: str) -> str:
    hash_data = hashlib.new("sha256")
    hash_data.update(bytes(data + settings.HASH_SALT, "utf-8"))
    return hash_data.hexdigest()
