import os

import nox
from laminci.nox import (
    build_docs,
    install_lamindb,
    login_testuser1,
    run,
    run_pre_commit,
    run_pytest,
)

# we'd like to aggregate coverage information across sessions
# and for this the code needs to be located in the same
# directory in every github action runner
# this also allows to break out an installation section
nox.options.default_venv_backend = "none"
IS_PR = os.getenv("GITHUB_EVENT_NAME") != "push"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session()
def build(session):
    branch = "main" if IS_PR else "release"  # point back to "release"
    install_lamindb(session, branch=branch, extras="bionty,aws")
    run(session, "uv pip install --system .[dev]")
    login_testuser1(session)
    run_pytest(session)
    build_docs(session, strict=False)  # temporarily disable strict mode
