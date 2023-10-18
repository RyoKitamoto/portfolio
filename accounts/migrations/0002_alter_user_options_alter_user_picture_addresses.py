# Generated by Django 4.1 on 2023-09-24 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'ユーザ', 'verbose_name_plural': 'ユーザ一覧'},
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.FileField(blank=True, default='user_picture/noname_user.png', null=True, upload_to='user_picture/'),
        ),
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('prefecture', models.CharField(default='大阪府', max_length=10)),
                ('city', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]