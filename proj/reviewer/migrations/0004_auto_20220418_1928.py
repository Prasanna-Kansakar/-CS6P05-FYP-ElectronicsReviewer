# Generated by Django 3.2.12 on 2022-04-18 13:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviewer', '0003_auto_20220417_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='laptop04storage',
            options={'verbose_name': 'Laptop Storage'},
        ),
        migrations.AlterModelOptions(
            name='laptop05processor',
            options={'verbose_name': 'Laptop Processor'},
        ),
        migrations.AlterModelOptions(
            name='laptop06gpu',
            options={'verbose_name': 'Laptop GPU'},
        ),
        migrations.AlterModelOptions(
            name='laptop07display',
            options={'verbose_name': 'Laptop Display'},
        ),
        migrations.AlterModelOptions(
            name='laptop08os',
            options={'verbose_name': 'Laptop Operating System'},
        ),
        migrations.RenameField(
            model_name='reviews01laptop_review',
            old_name='raings',
            new_name='ratings',
        ),
        migrations.RemoveField(
            model_name='reviews01laptop_review',
            name='accessory',
        ),
        migrations.AddField(
            model_name='reviews01laptop_review',
            name='laptop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reviewer.laptop01laptop'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accessories04images',
            name='img_url',
            field=models.ImageField(upload_to='images/accessories'),
        ),
        migrations.AlterField(
            model_name='laptop04storage',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Storage'),
        ),
        migrations.AlterField(
            model_name='laptop05processor',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Processor'),
        ),
        migrations.AlterField(
            model_name='laptop06gpu',
            name='name',
            field=models.CharField(max_length=255, verbose_name='GPU'),
        ),
        migrations.AlterField(
            model_name='laptop06gpu',
            name='vRAM',
            field=models.CharField(max_length=10, verbose_name='VRAM'),
        ),
        migrations.AlterField(
            model_name='laptop07display',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Display'),
        ),
        migrations.AlterField(
            model_name='laptop08os',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Operating System'),
        ),
        migrations.AlterField(
            model_name='laptop09images',
            name='img_url',
            field=models.ImageField(upload_to='images/laptop'),
        ),
        migrations.CreateModel(
            name='Reviews01Accessories_Review',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ratings', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('content', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.accessories01accessories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
