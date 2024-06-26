from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0008_auto_20150624_0520'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='in_trash',
            field=models.BooleanField(
                default=False, verbose_name='In trash?', editable=False
            ),
            preserve_default=True,
        ),
    ]
