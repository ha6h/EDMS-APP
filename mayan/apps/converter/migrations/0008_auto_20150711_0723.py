from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0007_auto_20150711_0656')
    ]

    operations = [
        migrations.AlterField(
            model_name='transformation',
            name='order',
            field=models.PositiveIntegerField(
                default=0, help_text='Order in which the transformations '
                'will be executed.', db_index=True, verbose_name='Order',
                blank=True
            ),
            preserve_default=True
        ),
        migrations.AlterUniqueTogether(
            name='transformation',
            unique_together={
                ('content_type', 'object_id', 'order')
            }
        )
    ]
