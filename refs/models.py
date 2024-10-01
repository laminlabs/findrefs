from __future__ import annotations

from typing import overload

from bionty import ids as bionty_ids
from bionty.models import BioRecord, CellType, Disease, Ethnicity, Source, Tissue
from django.db import models
from django.db.models import CASCADE, PROTECT
from lnschema_core import ids
from lnschema_core.models import (
    Artifact,
    CanValidate,
    Collection,
    Feature,
    LinkORM,
    Record,
    TracksRun,
    TracksUpdates,
)


class ClinicalTrial(Record, CanValidate, TracksRun, TracksUpdates):
    """Models a ClinicalTrials.

    Example:
        >>> trail = ClinicalTrial(
        ...     name="NCT00000000",
        ...     description="A refsl trial to evaluate the efficacy of drug X in patients with disease Y.",
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.base62_8)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """ClinicalTrials.gov ID, the format is "NCT" followed by an 8-digit number."""
    title = models.TextField(null=True, default=None)
    """Official title of the clinical trial."""
    objective = models.TextField(null=True, default=None)
    """Objective of the clinical trial."""
    description = models.TextField(null=True, default=None)
    """Description of the clinical trial."""
    collections = models.ManyToManyField(Collection, related_name="clinical_trials")
    """Collections linked to the clinical trial."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactClinicalTrial", related_name="clinical_trials"
    )
    """Artifacts linked to the clinical trial."""


class ArtifactClinicalTrial(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_clinical_trial"
    )
    clinicaltrial: ClinicalTrial = models.ForeignKey(
        ClinicalTrial, PROTECT, related_name="links_artifact"
    )
    feature: Feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactclinicaltrial",
    )
    label_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = models.BooleanField(null=True, default=None)


class Biosample(Record, CanValidate, TracksRun, TracksUpdates):
    """Models a specimen derived from an patient, such as tissue, blood, or cells.

    Examples:
        >>> biosample = Biosample(
        ...     name="control",
        ...     batch="ctrl_1"
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True, null=True)
    """Name of the biosample."""
    batch = models.CharField(max_length=60, default=None, null=True, db_index=True)
    """Batch label of the biosample."""
    description = models.TextField(null=True, default=None)
    """Description of the biosample."""
    patient = models.ForeignKey(
        "Patient", PROTECT, related_name="biosamples", null=True, default=None
    )
    """Patient linked to the biosample."""
    clinical_trial = models.ForeignKey(
        ClinicalTrial, PROTECT, related_name="biosamples", null=True, default=None
    )
    """Clinical trial linked to the biosample."""
    tissues = models.ManyToManyField(Tissue, related_name="biosamples")
    """Tissues linked to the biosample."""
    cell_types = models.ManyToManyField(CellType, related_name="biosamples")
    """Cell types linked to the biosample."""
    diseases = models.ManyToManyField(Disease, related_name="biosamples")
    """Diseases linked to the biosample."""
    medications = models.ManyToManyField("Medication", related_name="biosamples")
    """Medications linked to the biosample."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactBiosample", related_name="biosamples"
    )
    """Artifacts linked to the biosample."""


class ArtifactBiosample(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_biosample"
    )
    biosample: Biosample = models.ForeignKey(
        Biosample, PROTECT, related_name="links_artifact"
    )
    feature: Feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactbiosample",
    )
    label_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = models.BooleanField(null=True, default=None)


class Patient(Record, CanValidate, TracksRun, TracksUpdates):
    """Models a patient in a clinical study.

    Examples:
        >>> patient = Patient(
        ...     uid="internal_patient_id_5446"
        ...     name="Patient 5446",
        ...     age=45,
        ...     gender="female"
        ... ).save()
    """

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
        ("unknown", "Unknown"),
    ]

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances. Use this field to model internal patient IDs."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the patient."""
    age = models.IntegerField(null=True, default=None, db_index=True)
    """Age of the patient."""
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, default=None, db_index=True
    )
    """Gender of the patient."""
    ethnicity = models.ForeignKey(Ethnicity, PROTECT, null=True, default=None)
    """Ethnicity of the patient."""
    birth_date = models.DateField(db_index=True, null=True, default=None)
    """Birth date of the patient."""
    deceased = models.BooleanField(db_index=True, null=True, default=None)
    """Whether the patient is deceased."""
    deceased_date = models.DateField(db_index=True, null=True, default=None)
    """Date of death of the patient."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactPatient", related_name="patients"
    )
    """Artifacts linked to the patient."""


class ArtifactPatient(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_patient"
    )
    patient: Patient = models.ForeignKey(
        Patient, PROTECT, related_name="links_artifact"
    )
    feature: Feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactpatient",
    )
    label_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = models.BooleanField(null=True, default=None)


class Medication(BioRecord, TracksRun, TracksUpdates):
    """Models a medication."""

    class Meta(BioRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    _name_field: str = "name"
    _ontology_id_field: str = "ontology_id"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = models.CharField(unique=True, max_length=8, default=bionty_ids.ontology)
    """A universal id (hash of selected field)."""
    name: str = models.CharField(max_length=256, db_index=True)
    """Name of the medication."""
    ontology_id: str | None = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the medication."""
    chembl_id: str | None = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """ChEMBL ID of the medication."""
    abbr: str | None = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of medication."""
    synonyms: str | None = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this medication."""
    description: str | None = models.TextField(null=True, default=None)
    """Description of the medication."""
    parents: Medication = models.ManyToManyField(
        "self", symmetrical=False, related_name="children"
    )
    """Parent medication records."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactMedication", related_name="medications"
    )
    """Artifacts linked to the medication."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[Medication],
        source: Source | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class ArtifactMedication(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_medication"
    )
    medication: Medication = models.ForeignKey(
        Medication, PROTECT, related_name="links_artifact"
    )
    feature: Feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactmedication",
    )
    label_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = models.BooleanField(null=True, default=None)


class Treatment(Record, CanValidate, TracksRun, TracksUpdates):
    """Models compound treatments such as drugs.

    Examples:
        >>> aspirin_treatment = compound_treatment = Treatment(
        ...    name="Aspirin 325 MG Enteric Coated Tablet",
        ... ).save()
    """

    STATUS_CHOICES = [
        ("in-progress", "In Progress"),
        ("completed", "Completed"),
        ("entered-in-error", "Entered in Error"),
        ("stopped", "Stopped"),
        ("on-hold", "On Hold"),
        ("unknown", "Unknown"),
        ("not-done", "Not Done"),
    ]

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the treatment."""
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, null=True, default=None
    )
    """Status of the treatment."""
    medication = models.ForeignKey(Medication, PROTECT, null=True, default=None)
    """Medications linked to the treatment."""
    dosage = models.FloatField(null=True, default=None)
    """Dosage of the treatment."""
    dosage_unit = models.CharField(max_length=32, null=True, default=None)
    """Unit of the dosage."""
    administered_datetime = models.DateTimeField(null=True, default=None)
    """Date and time the treatment was administered."""
    duration = models.DurationField(null=True, default=None)
    """Duration of the treatment."""
    route = models.CharField(max_length=32, null=True, default=None)
    """Route of administration of the treatment."""
    site = models.CharField(max_length=32, null=True, default=None)
    """Body site of administration of the treatment."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactTreatment", related_name="treatments"
    )
    """Artifacts linked to the treatment."""


class ArtifactTreatment(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="links_treatment"
    )
    treatment: Treatment = models.ForeignKey(
        Treatment, PROTECT, related_name="links_artifact"
    )
    feature: Feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifacttreatment",
    )
    label_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = models.BooleanField(null=True, default=None)
