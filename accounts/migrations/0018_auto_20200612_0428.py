# Generated by Django 3.0.7 on 2020-06-11 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20200612_0420'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentee',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Mentor'),
        ),
        migrations.AddField(
            model_name='mentee',
            name='note',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='CGPA',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
    ]