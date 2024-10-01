from __future__ import annotations

from django.db import models
from django.db.models import CASCADE, PROTECT
from lnschema_core import ids
from lnschema_core.models import (
    Artifact,
    CanValidate,
    Feature,
    LinkORM,
    Record,
    TracksRun,
    TracksUpdates,
)


class Reference(Record, CanValidate, TracksRun, TracksUpdates):
    """References.

    Example:
        >>> reference = Reference(
        ...     name="A paper title",
        ...     doi="A doi",
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = models.CharField(max_length=255, default=None, db_index=True)
    """Title or name of the reference."""
    abbr: str | None = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation."""
    url: str | None = models.URLField(max_length=255, null=True, default=None)
    """A URL to view."""
    pubmed_id: int | None = models.BigIntegerField(null=True, default=None)
    """A pudbmed ID."""
    doi: int | None = models.CharField(
        max_length=255, null=True, default=None, db_index=True
    )
    """A DOI."""
    text: str | None = models.TextField(null=True, default=None)
    """Text of the reference included in search, e.g. the abstract or the full-text."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactReference", related_name="references"
    )
    """Artifacts labeled with this reference."""


class ArtifactReference(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_reference"
    )
    reference: Reference = models.ForeignKey(
        Reference, PROTECT, related_name="links_artifact"
    )
    feature: Feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactreference",
    )
    label_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
