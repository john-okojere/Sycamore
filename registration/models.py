from django.db import models

class Registrant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    accommodation = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], verbose_name="Do you need Accomodation")
    marital_status = models.CharField(max_length=10, choices=[
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ])
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        import qrcode
        from io import BytesIO
        from django.core.files import File
        from PIL import Image, ImageDraw

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'Registration ID: {self.id}')
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save QR code image to a BytesIO buffer
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        filename = f'{self.first_name}_{self.id}_qr.png'
        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)


class Volunteer(models.Model):
    registrant = models.OneToOneField(Registrant, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.registrant}'