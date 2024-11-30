# Generated by Django 5.1.3 on 2024-11-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0003_alter_registrant_accommodation_volunteer"),
    ]

    operations = [
        migrations.CreateModel(
            name="InHouse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone_number", models.CharField(max_length=15)),
                (
                    "department",
                    models.CharField(
                        choices=[
                            ("ushering", "Ushering"),
                            ("sanctuary", "Sanctuary"),
                            ("spirit&truth", "Spirit & Truth"),
                            ("technical", "Technical"),
                        ],
                        max_length=25,
                    ),
                ),
                ("qr_code", models.ImageField(blank=True, upload_to="qrcodes/")),
            ],
        ),
        migrations.AddField(
            model_name="volunteer",
            name="role",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="registrant",
            name="accommodation",
            field=models.CharField(
                choices=[("yes", "Yes"), ("no", "No")],
                max_length=3,
                verbose_name="Do you need Accommodation",
            ),
        ),
    ]
