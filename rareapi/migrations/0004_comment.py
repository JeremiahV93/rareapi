# Generated by Django 3.1.4 on 2021-01-06 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0003_rareuser_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date', models.DateField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='rareapi.post')),
                ('rareuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comments', to='rareapi.rareuser')),
            ],
        ),
    ]