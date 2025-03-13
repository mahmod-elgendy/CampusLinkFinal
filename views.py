from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def index(request):
    return render(request, 'index.html')


def notification(request):
    return render(request, 'notification.html')

def login(request):
    return render(request, 'login.html')

# def register(request):
#     return render(request, 'register.html')


def search(username):

    users_ref = db.reference("users")
    users_data = users_ref.get()

    if not users_data:
        return []  # Return an empty list if no users are found

    matching_users = []
    for user_id, user_data in users_data.items():
        if user_data.get("username").lower().find(username.lower()) != -1:
            matching_users.append({
                "id": user_id,
                "username": user_data.get("username", ""),
            })

    return matching_users



def mentors(request):
    mentors_data = {}
    try:
        mentors_ref = db.reference('Mentor') 
        mentors_data = mentors_ref.get()
        if mentors_data is None:
            print("No mentor data found in Firebase.")
            mentors_data = {} 

    except Exception as e:
        print(f"Error fetching mentor data from Firebase: {e}")
        mentors_data = {}

    mentors = []
    for mentor_id, mentor_info in mentors_data.items():
        mentor = {
            'id': mentor_id,
            'name': mentor_info.get('MentorName', 'No Name'),
            'availability': mentor_info.get('MentorAvailability', 'Unknown'), 
            'email': mentor_info.get('MentorEmail', 'No Email'),
            'tags': mentor_info.get('MentorTags', []), 
        }
        mentors.append(mentor)
    context = {'mentors': mentors}
    return render(request, 'mentors.html', context)



def timeline(request):
    posts_data = {}

    try:
        posts_ref = db.reference('Post')
        posts_data = posts_ref.get()
        if posts_data is None:
            print("No post data found in Firebase.")
            posts_data = {}  

    except Exception as e:
        print(f"Error fetching post data from Firebase: {e}")
        posts_data = {}  

    posts = []
    for post_id, post_info in posts_data.items():
        post = {
            'id': post_id,
            'title': post_info.get('PostDesc', 'No Title'),  # Extract title from PostDesc
            'content': post_info.get('PostDesc', 'No Content'),  # Use PostDesc for content
            'image_url': post_info.get('imageUrl', ''),  # Assume 'imageUrl' field for image
            # Add other fields as needed
        }
        posts.append(post)
    context = {'posts': posts}
    return render(request, 'hero.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)



from django.shortcuts import render, redirect
from django.http import JsonResponse
from firebase_config.firebase_helpers import get_data, update_data, delete_data
from django.middleware.csrf import get_token  # Import CSRF token function



def get_user_profile_query(request):
    user_id = request.GET.get('user_id')  # Get user_id from the query string
    if not user_id:
        return JsonResponse({"error": "User ID not provided"}, status=400)

    return get_user_profile_logic(request, user_id)  # Pass request to the function

def get_user_profile_path(request, user_id):
    return get_user_profile_logic(request, user_id)  # Pass request to the function

def get_user_profile_logic(request, user_id):
    users = get_data("User")  # Fetch the 'User' node from Firebase

    if not users:
        return JsonResponse({"error": "No users found in Firebase."}, status=404)

    # Check if the user with the specific UserID exists
    user = None
    for key, user_data in users.items():
        if user_data.get("UserID") == user_id:  # Compare the UserID in the data
            user = user_data
            break

    if user:
        # Make sure to pass `request` so `csrf_token` is available in the template
        return render(request, "profile.html", {"user": user, "csrf_token": get_token(request)})  # Pass csrf_token here
    else:
        return JsonResponse({"error": "User not found"}, status=404)


def update_user_page(request, user_id):
    users = get_data("User")  # Get all users from Firebase

    user = None
    for key, data in users.items():
        if data.get("UserID") == user_id:
            user = data
            break

    if user != None:
        return render(request, 'update_profile.html', {'user': user})
    else:
        return JsonResponse({"error": "User not found"}, status=404)

def update_user_profile(request, user_id):
    if request.method == "POST":
        try:
            # Collect updated data from the form
            updated_data = {
                "UserName": request.POST.get('UserName'),
                "UserEmail": request.POST.get('UserEmail'),
                "UserBio": request.POST.get('UserBio'),
                "UserPFP": request.POST.get('UserPFP'),
                "UserCV": request.POST.get('UserCV'),
                "UserTags": request.POST.get('UserTags'),
                "UserNfollowers": int(request.POST.get('UserNfollowers')),
                "UserNfollowing": int(request.POST.get('UserNfollowing')),
                "UserAccess": request.POST.get('UserAccess'),
                "UserPass": request.POST.get('UserPass'),
            }

            # Fetch all users from Firebase
            users = get_data("User")

            # Find the user and update their data
            for key, user in users.items():
                if user.get("UserID") == user_id:
                    update_data(f"User/{key}", updated_data)
                    # Redirect back to the profile page
                    return redirect('get_user_profile_path', user_id=user_id)

            # If user not found
            return JsonResponse({"error": "User not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)




def delete_user_profile(request, user_id):
    if request.method == 'DELETE':  # Ensure method is DELETE
        users = get_data("User")  # Fetch the 'User' node from Firebase

        for key, user in users.items():
            if user.get("UserID") == user_id:
                delete_data(f"User/{key}")  # Delete the user from Firebase
                return JsonResponse({"message": "Profile deleted successfully!"})

        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Invalid method"}, status=405)




from django.shortcuts import render, redirect
from django.http import JsonResponse
from firebase_config.firebase_helpers import get_data, create_data, update_data, delete_data
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from datetime import datetime

@csrf_protect  # Ensure CSRF protection
def create_post(request):
    """Create a new post with a description and an optional photo."""
    if request.method == "POST":
        description = request.POST.get("description")
        image_file = request.FILES.get("image")

        if image_file:
            fs = FileSystemStorage(location='src/media/posts')  # Define where to store the image
            filename = fs.save(image_file.name, image_file)  # Save the file
            image_url = fs.url(filename)  # Get the URL to access the image
        else:
            image_url = None

        post_data = {
            "description": description,
            "image_url": image_url,
            "likes": 0,  # Initialize likes count
            "comments": [],  # Initialize comments list
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use real timestamp
        }

        # Save post data to Firebase, post ID will be generated automatically by Firebase
        post_id = create_data("Posts", post_data)

        # Redirect to home page after post creation
        return redirect('home')

    return render(request, "create_post.html")



@csrf_protect
def edit_post(request, post_id):
    """Edit an existing post."""
    if request.method == "POST":
        updated_description = request.POST.get("description")
        updated_image_file = request.FILES.get("image")

        image_url = None
        if updated_image_file:
            fs = FileSystemStorage(location='src/media/posts')  # Use the same location
            filename = fs.save(updated_image_file.name, updated_image_file)
            image_url = fs.url(filename)

        # Update the post with the new description or image URL
        update_data(f"Posts/{post_id}", {"description": updated_description, "image_url": image_url})
        
        # Redirect to the home page after post update
        return redirect('home')

    post = get_data(f"Posts/{post_id}")
    return render(request, "edit_post.html", {"post": post})


@csrf_protect  # Ensure CSRF protection
def delete_post(request, post_id):
    """Delete a specific post."""
    if request.method == 'DELETE':
        try:
            delete_data(f"Posts/{post_id}")
            return JsonResponse({"message": "Post deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


from django.conf import settings

def your_view_function(request):
    posts = {
        '1': {'description': 'First post', 'image_url': 'posts/Screenshot 2024-12-15 115513_b1shwrx.png'},
        '2': {'description': 'Second post', 'image_url': 'posts/example2.jpg'},
        # Add more posts as needed
    }
    return render(request, 'your_template.html', {'posts': posts, 'MEDIA_URL': settings.MEDIA_URL})



import requests
from django.shortcuts import render



from firebase_admin import db
from datetime import datetime

def seed_database(dynamic_user_id, author_id, description, tags, not_type="New Post"):
    """
    Seed the Firebase database with a post and related notification.
    """
    # Post data structure
    post_data = {
        "author_id": author_id,
        "description": description,
        "tags": tags,
        "likes": 0,  # Initialize with 0 likes
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # Current timestamp
    }

    # Add the post to the /Posts node
    posts_ref = db.reference('/Posts')
    post_id = posts_ref.push(post_data).key  # Generate unique post ID

    # Create a notification for the user
    notifications_ref = db.reference(f"/Notifications/{dynamic_user_id}")

    notification_data = {
        "NotID": f"Not-{post_id}",
        "NotContent": f"{author_id} posted: {description}",
        "NotTags": tags,
        "NotTimestamp": post_data["timestamp"],
        "NotType": not_type  # Add notification type
    }

    notifications_ref.push(notification_data)

    print(f"Seeded data: Post ID {post_id}, Notification: {notification_data}")

# Example data to test the function
dynamic_user_id = "UserID5"  # Dynamic user ID
author_id = "AuthorID1"  # Author's ID
description = "This is a test post."  # Post description
tags = ["tag1", "tag2"]  # Tags for the post

# Call the function to create a new post and a notification
seed_database(dynamic_user_id, author_id, description, tags)

seed_database(dynamic_user_id, author_id, description, tags, not_type="Mentions")

