import random
from datetime import datetime


def get_message_authentication_random_number() -> int:
    HASH = "A19B7!@@#AMMs*SDF"
    random.seed(str(datetime.now()) + HASH)
    result = random.randrange(100000, 999999)
    return result
