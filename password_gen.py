import random
import string

carac_qt = int(input('Quantos caraceteres são necessários? '))

def generate_password(lenghth: str = carac_qt):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(alphabet) for i in range(lenghth))
    return password

password = generate_password()
print(f'Senha gerada é: {password}')