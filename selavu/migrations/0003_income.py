# Generated by Django 5.1.7 on 2025-04-01 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selavu', '0002_category_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('Salary', 'Salary'), ('equity', 'equity'), ('Allowance', 'Allowance'), ('Other', 'Other')], default='Salary', max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
