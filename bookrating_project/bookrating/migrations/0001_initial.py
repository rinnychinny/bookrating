# Generated by Django 5.2.2 on 2025-06-18 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookEdition',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('isbn', models.CharField(blank=True, max_length=13, null=True)),
                ('isbn13', models.CharField(blank=True, max_length=13, null=True)),
                ('language_code', models.CharField(blank=True, max_length=10, null=True)),
                ('num_pages', models.PositiveIntegerField(blank=True, null=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('publisher', models.CharField(blank=True, max_length=255, null=True)),
                ('ratings_count', models.PositiveIntegerField()),
                ('avg_rating', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('original_year', models.IntegerField(blank=True, null=True)),
                ('avg_rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('ratings_count', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('rating', models.PositiveSmallIntegerField()),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookrating.bookedition')),
            ],
        ),
        migrations.CreateModel(
            name='EditionTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookrating.bookedition')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookrating.tag')),
            ],
        ),
        migrations.AddField(
            model_name='bookedition',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editions', to='bookrating.work'),
        ),
        migrations.CreateModel(
            name='WorkAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookrating.author')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookrating.work')),
            ],
        ),
        migrations.AddField(
            model_name='work',
            name='authors',
            field=models.ManyToManyField(through='bookrating.WorkAuthor', to='bookrating.author'),
        ),
    ]
