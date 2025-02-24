import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

def send_firebase_otp(phone_number):
    try:
        auth.create_user(phone_number=phone_number)
        print(f"OTP sent to {phone_number} via Firebase.")
    except Exception as e:
        print(f"Failed to send Firebase OTP: {e}")
