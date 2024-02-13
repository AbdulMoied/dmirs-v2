import random
import string
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for i in range(8))
    return password