from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def check_password(password, hash):
    return check_password_hash(hash, password)


password = 'password123'
hashed_password = hash_password(password)
print(f'The hashed Password for {password} is {hashed_password}')

newpassword = input('Enter a password: ')

print(f'The password {newpassword} is {check_password(newpassword, hashed_password)}')