import firebase_admin
from firebase_admin import credentials, db
import requests

# Ensure Firebase is initialized only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config/firebase_admin_sdk.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://campuslink-56ae6-default-rtdb.firebaseio.com",
        "storageBucket": "campuslink-56ae6.appspot.com"
    })

def get_data(reference):
    ref = db.reference(reference)
    data = ref.get()
    if data is None:
        print(f"No data found at reference {reference}")
    return data

def set_data(reference, data):
    """
    Set data at a specified reference in Firebase.
    :param reference: The path in the database to set data at.
    :param data: The data to set at the specified reference.
    """
    ref = db.reference(reference)
    ref.set(data)

def update_data(reference, data):
    """
    Update data at a specified reference in Firebase.
    :param reference: The path in the database to update data at.
    :param data: The data to update at the specified reference.
    """
    ref = db.reference(reference)
    ref.update(data)

def delete_data(reference):
    """
    Delete data from a specified reference in Firebase.
    :param reference: The path in the database to delete data from.
    """
    ref = db.reference(reference)
    ref.delete()

def push_data(reference, data):
    """
    Push data to a specified reference in Firebase, automatically generating a unique key.
    :param reference: The path in the database to push data to.
    :param data: The data to push to the specified reference.
    """
    ref = db.reference(reference)
    new_ref = ref.push()  # Generates a unique key
    new_ref.set(data)  # Set the data at the new unique key
    return new_ref.key  # Return the new key


def create_data(path, data):
    """Create data at the specified Firebase path."""
    ref = db.reference(path)
    ref.push(data)
    

def upload_image_to_imgur(image_file):
    """
    Upload an image to Imgur and return the image URL.
    :param image_file: The image file to upload.
    :return: The URL of the uploaded image.
    """
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": "Client-ID YOUR_IMGUR_CLIENT_ID"}
    files = {"image": image_file}
    response = requests.post(url, headers=headers, files=files)
    response_data = response.json()

    if response.status_code == 200:
        return response_data["data"]["link"]  # Return the image URL
    else:
        raise Exception(f"Imgur upload failed: {response_data['data']['error']}")