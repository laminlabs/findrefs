"""A reference manager.

This schema provides a single registry `Reference` to store references to studies, reports, papers, blog posts, preprints.

Import the package::

   import findrefs as fr

This is the complete API reference:

.. autosummary::
   :toctree: .

    Reference
"""

__version__ = "0.1.0"  # denote a pre-release for 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="findrefs")
    return globals()[name]


if _check_instance_setup():
    del __getattr__  # delete so that imports work out
    from .models import Reference
