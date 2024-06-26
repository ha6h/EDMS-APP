from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dynamic_search', '0001_initial')
    ]

    operations = [
        migrations.AlterField(
            model_name='recentsearch',
            name='user',
            field=models.ForeignKey(
                editable=False, on_delete=models.CASCADE,
                to=settings.AUTH_USER_MODEL, verbose_name='User'
            ),
            preserve_default=True
        )
    ]
