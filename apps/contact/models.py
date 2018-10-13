from django.db import models


class Contact(models.Model):
    sender = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} {self.message[:20]}"
