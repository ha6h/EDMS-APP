from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('documents', '0041_auto_20170823_1855')
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPageContent',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'content', models.TextField(
                        blank=True, verbose_name='Content'
                    )
                ),
                (
                    'document_page', models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='content', to='documents.DocumentPage',
                        verbose_name='Document page'
                    )
                )
            ],
            options={
                'verbose_name': 'Document page content',
                'verbose_name_plural': 'Document pages contents'
            }
        ),
        migrations.CreateModel(
            name='DocumentVersionParseError',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'datetime_submitted', models.DateTimeField(
                        auto_now_add=True, db_index=True,
                        verbose_name='Date time submitted'
                    )
                ),
                (
                    'result', models.TextField(
                        blank=True, null=True, verbose_name='Result'
                    )
                ),
                (
                    'document_version', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='parse_errors',
                        to='documents.DocumentVersion',
                        verbose_name='Document version'
                    )
                )
            ],
            options={
                'ordering': ('datetime_submitted',),
                'verbose_name': 'Document version parse error',
                'verbose_name_plural': 'Document version parse errors'
            }
        )
    ]
