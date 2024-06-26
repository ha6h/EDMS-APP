from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0010_auto_20151001_0055')
    ]

    operations = [
        migrations.CreateModel(
            name='SaneScanner',
            fields=[
                (
                    'interactivesource_ptr', models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True, primary_key=True, serialize=False,
                        to='sources.InteractiveSource'
                    )
                ),
                (
                    'device_name', models.CharField(
                        help_text='Device name as returned by the SANE '
                        'backend.', max_length=255,
                        verbose_name='Device name'
                    )
                )
            ],
            options={
                'verbose_name': 'SANE Scanner',
                'verbose_name_plural': 'SANE Scanners'
            },
            bases=('sources.interactivesource',),
        )
    ]
