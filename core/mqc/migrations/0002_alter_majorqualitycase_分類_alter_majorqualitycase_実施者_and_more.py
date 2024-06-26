# Generated by Django 4.2.13 on 2024-05-29 11:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mqc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='majorqualitycase',
            name='分類',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mqc.divisioncategory'),
        ),
        migrations.AlterField(
            model_name='majorqualitycase',
            name='実施者',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='実施者', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='majorqualitycase',
            name='実施部署',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mqc.department'),
        ),
        migrations.AlterField(
            model_name='majorqualitycase',
            name='発生場所',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mqc.location'),
        ),
        migrations.AlterField(
            model_name='majorqualitycase',
            name='製品分',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mqc.partcategory'),
        ),
        migrations.AlterField(
            model_name='majorqualitycase',
            name='責任者',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='責任者', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='majorqualitycase',
            name='責区',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mqc.responsibilitycategory'),
        ),
    ]
