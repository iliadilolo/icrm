# Generated by Django 4.2.3 on 2023-07-26 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0008_category_lead_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]
