# Generated by Django 3.0.8 on 2020-08-28 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_content', models.TextField()),
                ('post_timestamp', models.DateTimeField(auto_now_add=True)),
                ('post_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_timestamp', models.DateTimeField(auto_now_add=True)),
                ('like_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('like_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.Post')),
            ],
        ),
    ]
