
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("firebase_config/firebase_admin_sdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://campuslink-56ae6-default-rtdb.firebaseio.com/'
})
