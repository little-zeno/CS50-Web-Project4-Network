from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import signals


class User(AbstractUser):
    pass

def create_model_follow(sender, instance, created, **kwargs):
    if created:
        Follow.objects.create(user=instance)
signals.post_save.connect(create_model_follow, sender=User, weak=False, dispatch_uid='models.create_model_follow')


class Post(models.Model):
    post_text = models.CharField(max_length=300, blank=True, null=True)
    pub_date = models.DateTimeField("date posted", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweeter")
    likes = models.ManyToManyField(User, related_name="post_like")

    def serialize(self):
        return {
            "id": self.id,
            "count": self.likes.count()
        }

    class Meta:
        ordering = ['-pub_date']
    
    
    
class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow_person = models.ManyToManyField(User, related_name="following")
    followed = models.ManyToManyField(User, related_name="follower")
    follow_date = models.DateTimeField("date followed", auto_now_add=True)
    def __str__(self):
        return f"{self.user} is following {self.follow_person} and followed by {self.followed}"


class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter", null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=False)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment", null=True)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment