import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_usuario_email_remove_usuario_password_hash_and_more'),
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutina',
            name='usuario',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='rutinas_creadas',
                to='users.usuario',
            ),
        ),
    ]
