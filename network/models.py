from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content}"


class Follows(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    followed = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed")

    def __str__(self):
        return f"{self.user} following {self.followed}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post")

    def __str__(self):
        return f"{self.user} likes post by {self.post}"
