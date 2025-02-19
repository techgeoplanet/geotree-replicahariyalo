from django.db import models

# Create your models here.
class QrcodeVisiter(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    qrcode = models.CharField(max_length=255)  # QR Code field
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto-set on creation

    def __str__(self):
        return f"Visiter {self.id} - {self.qrcode}"