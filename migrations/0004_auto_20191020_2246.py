# Generated by Django 2.1.7 on 2019-10-20 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0003_auto_20191019_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='collection',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('done', models.IntegerField(default=0)),
                ('note_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Note')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='usercomment',
            options={'verbose_name_plural': 'usercomment'},
        ),
    ]
