from __future__ import annotations

from django.db import models
from django.db.models import CASCADE, PROTECT
from lnschema_core import ids
from lnschema_core.fields import (
    BigIntegerField,
    BooleanField,
    CharField,
    ForeignKey,
    TextField,
)
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
    """References such as a publication or document, with unique identifiers and metadata.

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
    uid: str = CharField(max_length=12, unique=True, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Title or name of the reference document."""
    abbr: str | None = CharField(
        max_length=32,
        db_index=True,
        unique=True,
        null=True,
    )
    """A unique abbreviation for the reference."""
    url: str | None = models.URLField(null=True)
    """URL linking to the reference."""
    pubmed_id: int | None = BigIntegerField(null=True)
    """A PudMmed ID."""
    doi: int | None = CharField(null=True, db_index=True)
    """Digital Object Identifier (DOI) for the reference."""
    text: str | None = TextField(null=True)
    """Text of the reference such as the abstract or the full-text to enable search."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactReference", related_name="references"
    )
    """Artifacts labeled with this reference."""


class ArtifactReference(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_reference")
    reference: Reference = ForeignKey(Reference, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactreference",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)
