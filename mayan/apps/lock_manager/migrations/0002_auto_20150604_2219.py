from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lock_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lock',
            name='name',
            field=models.CharField(
                unique=True, max_length=64, verbose_name='Name'
            ),
            preserve_default=True,
        ),
    ]
