# -*- coding: utf-8 -*-
"""Nox for python task automation.

nox.option.sessions is default run for 'nox' on command line. Currently only tests.
"""
import tempfile

import nox
from nox.sessions import Session

locations = "afkode", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "tests", "lint"
package = "afkode"
PY_VERSIONS = ["3.8"]


@nox.session(python=PY_VERSIONS)
def lint(session: Session) -> None:
    """Runs code quality checks.

    Done in order so that easier to pass tests run first.
    This is in a single command to avoid too much time on environment setup.
    * black - codestyle alignment
    * safety - security checks
    * sqlfluff - format checks SQL code
    * xdoctest - any code snippets in docstrings are run for correctness
    * mypy - type checking
    * flake8 - code format and consistency checks
    """
    args = session.posargs or locations
    session.run("poetry", "install", "--no-dev", "--extras", "lint", external=True)
    session.run("black", *args)
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
    session.run("python", "-m", "xdoctest", package, *args)
    session.run("mypy", "--install-types", *args)
    session.run("flake8", *args)


@nox.session(python=PY_VERSIONS)
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", "--extras", "tests", external=True)
    session.run("pytest", *args)


@nox.session(python=PY_VERSIONS)
def docs(session: Session) -> None:
    """Build documentation."""
    session.run("poetry", "install", "--no-dev", "--extras", "docs", external=True)
    session.run("rm", "-rf", "docs/_build")
    session.run("sphinx-build", "docs", "docs/_build", *session.posargs)
