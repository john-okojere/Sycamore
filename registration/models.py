from django.db import models
from qrcode import *
import uuid
import os

class Registrant(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    accommodation = models.CharField(
        max_length=3, 
        choices=[
            ('yes', 'Yes'), 
            ('no', 'No')
        ], 
        verbose_name="Do you need Accommodation"
    )
    marital_status = models.CharField(
        max_length=10, 
        choices=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
            ('widowed', 'Widowed'),
        ]
    )
    def qr_code(self):
        qrcode = make(self.uid)
        basename = str(self.first_name) + '_QR_CODE.png'
        directory = "media/QRCODE/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        qrcode.save('media/QRCODE/{}'.format(basename))
        return '/media/QRCODE/{}'.format(basename)

    def save(self, *args, **kwargs):
        self.qr_code()
        if self.accommodation.title() == "Yes":
            self.role = "Camper"
        else:
            self.role = 'Participant'
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



   

class Volunteer(models.Model):
    registrant = models.OneToOneField(Registrant, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Volunteer: {self.registrant.first_name} {self.registrant.last_name} ({self.role})'


class InHouse(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    department = models.CharField(
        max_length=25, 
        choices=[
            ('ushering', 'Ushering'),
            ('sanctuary', 'Sanctuary'),
            ('spirit & Truth', 'Spirit & Truth'),
            ('technical', 'Technical'),
            ('light & Power', 'Light & Power'),
            ('media', 'New Wine Media'),
            ('follow up', 'Labour Room (follow_up)'),
            ('decoration', 'Decoration'),
            ('welfare', 'Taste & See'),
            ('pastoral', 'Pastoral Care'),
            ('pastor', 'Pastor'),
            ('special Guest', 'Special Guest'),
        ]
    )
    def qr_code(self):
        qrcode = make(self.uid)
        basename = str(self.first_name) + '_QR_CODE.png'
        directory = "media/QRCODE/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        qrcode.save('media/QRCODE/{}'.format(basename))
        return '/media/QRCODE/{}'.format(basename)

    def save(self, *args, **kwargs):
        self.qr_code()
        if self.accomodation.title() == "Yes":
            self.role = "Camper"
        else:
            self.role = 'Participant'
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.department})'

class Minister(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        import qrcode
        from io import BytesIO
        from django.core.files import File

        if not self.id:
            super().save(*args, **kwargs)

        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"Minister's ID: {self.id}, Name: {self.first_name} {self.last_name}")
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, 'PNG')
        filename = f'{self.first_name}_{self.id}_qr.png'
        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)
