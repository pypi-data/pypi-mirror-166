from hashlib import md5


def calculate_md5(filename):
    return md5(filename).hexdigest()
