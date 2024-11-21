"""A reference manager [`source <https://github.com/laminlabs/findrefs/blob/main/findrefs/models.py>`__].

This schema module provides a single registry `Reference` to store references to studies, reports, papers, blog posts, preprints.

Install and mount `findrefs` in a new instance:

>>> pip install findrefs
>>> lamin init --storage ./test-findrefs --schema findrefs

Import the package:

>>> import findrefs as fr

The `Reference` registry:

.. autosummary::
   :toctree: .

    Reference
"""

__version__ = "0.2.0"  # denote a pre-release for 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="findrefs")
    return globals()[name]


if _check_instance_setup():
    import lamindb

    del __getattr__  # delete so that imports work out
    from .models import Reference
