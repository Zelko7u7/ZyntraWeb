import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
        ("achievements", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="logro",
            name="usuario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="logros_creados",
                to="users.usuario",
            ),
        ),
        migrations.AlterField(
            model_name="logrousuario",
            name="logro",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="desbloqueos",
                to="achievements.logro",
            ),
        ),
        migrations.AlterField(
            model_name="logrousuario",
            name="usuario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="logros_desbloqueados",
                to="users.usuario",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="logrousuario",
            unique_together={("usuario", "logro")},
        ),
    ]
