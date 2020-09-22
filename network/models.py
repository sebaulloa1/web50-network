from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField()
    post_timestamp = models.DateTimeField(auto_now_add=True)
    post_likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "post_id": self.id,
            "post_user": self.post_user.id,
            "post_username": self.post_user.username,
            "post_content": self.post_content,
            "post_timestamp": self.post_timestamp.strftime("%b %#d %Y, %#I:%M %p"),
        }

    def __str__ (self):
        return f"{self.id}: {self.post_user.username} said ({self.post_content})."
    
class Like(models.Model):
    like_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_by = models.ForeignKey(User, on_delete=models.CASCADE)
    like_timestamp = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follow_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    follow_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')

    def __str__ (self):
        return f"{self.id}: (Follow_user) {self.follow_user.username} follows (follow_following) {self.follow_following.username}."


