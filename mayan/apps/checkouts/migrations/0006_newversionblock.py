from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0036_auto_20161222_0534'),
        ('checkouts', '0005_auto_20160122_0756')
    ]

    operations = [
        migrations.CreateModel(
            name='NewVersionBlock',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'document', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='documents.Document', verbose_name='Document'
                    )
                )
            ],
            options={
                'verbose_name': 'New version block',
                'verbose_name_plural': 'New version blocks'
            }
        )
    ]
