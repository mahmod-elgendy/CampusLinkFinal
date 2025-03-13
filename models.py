from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# class Post(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link post to user
#     PostDesc = models.TextField()  # Assuming post description is a longer text
#     PostLikes = models.IntegerField(default=0)
#     PostComments = models.IntegerField(default=0)
#     PostTimestamp = models.DateTimeField(auto_now_add=True)  # Automatically set on post creation

#     def __str__(self):
#         return f"Post by {self.author.username}: {self.PostDesc[:20]}" 