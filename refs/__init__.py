"""A clinical schema.

Import the package::

   import refs

This is the complete API reference:

.. autosummary::
   :toctree: .

   Biosample
   ClinicalTrial
   Medication
   Patient
   Treatment
"""

__version__ = "0.0.1"  # denote a pre-release for 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="refs")
    return globals()[name]


if _check_instance_setup():
    del __getattr__  # delete so that imports work out
    from .models import (
        Biosample,
        ClinicalTrial,
        Medication,
        Patient,
        Treatment,
    )
