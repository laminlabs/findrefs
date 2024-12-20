# Generated by Django 5.1.1 on 2024-10-01 10:28

import django.db.models.deletion
import lnschema_core.ids
import lnschema_core.models
import lnschema_core.users
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("lnschema_core", "0066_alter_artifact__feature_values_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtifactReference",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("label_ref_is_name", models.BooleanField(default=None, null=True)),
                ("feature_ref_is_name", models.BooleanField(default=None, null=True)),
                (
                    "artifact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_reference",
                        to="lnschema_core.artifact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "feature",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_artifactreference",
                        to="lnschema_core.feature",
                    ),
                ),
                (
                    "run",
                    models.ForeignKey(
                        default=lnschema_core.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.run",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(lnschema_core.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="Reference",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(
                        default=lnschema_core.ids.base62_12, max_length=12, unique=True
                    ),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                (
                    "abbr",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("url", models.URLField(default=None, max_length=255, null=True)),
                ("pubmed_id", models.BigIntegerField(default=None, null=True)),
                (
                    "doi",
                    models.CharField(
                        db_index=True, default=None, max_length=255, null=True
                    ),
                ),
                ("text", models.TextField(default=None, null=True)),
                (
                    "_previous_runs",
                    models.ManyToManyField(related_name="+", to="lnschema_core.run"),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="references",
                        through="findrefs.ArtifactReference",
                        to="lnschema_core.artifact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "run",
                    models.ForeignKey(
                        default=lnschema_core.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.run",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(lnschema_core.models.CanCurate, models.Model),
        ),
        migrations.AddField(
            model_name="artifactreference",
            name="reference",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_artifact",
                to="findrefs.reference",
            ),
        ),
    ]
