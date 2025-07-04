# Generated by Django 5.2.2 on 2025-06-29 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookrating', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('user_id', 'edition'), name='unique_user_edition_rating'),
        ),
    ]
