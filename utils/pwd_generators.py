import secrets
import string
from random import randint

# for a 20-character password
def generate_20char_pwd():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20)) 
    return password

# for a N-digits password
def generate_N_dig_pwd(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)