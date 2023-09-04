# with open('firebase_credentials.txt', 'r') as f:
#     creds = [line.strip() for line in f]

# config = {
#     "apiKey": creds[0],
#     "authDomain": creds[1],
#     "databaseURL": creds[2],
#     "storageBucket": creds[3]
# }

# firebase = pyrebase.initialize_app(config)

# auth = firebase.auth()

# email = "saatwik.vasishtha@gmail.com"
# # password = "HelloWorld123"
# # auth.create_user_with_email_and_password(email, password)
# password = "HelloWorld"
# try:
#     user = auth.sign_in_with_email_and_password(email, password)
# except:
#     print("Invalid Credentials")

# password = "HelloWorld123"
# try:
#     user = auth.sign_in_with_email_and_password(email, password)
#     print("Logged In")
# except:
#     print("Invalid Credentials")
def check_pass(email,password,firebase):
    auth = firebase.auth()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return True
    except:
        return False

def signup(name,email,password, firebase):
    auth = firebase.auth()
    try:
        auth.create_user_with_email_and_password(email, password)
        return True
    except: 
        return False
