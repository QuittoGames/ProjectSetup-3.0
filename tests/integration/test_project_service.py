"""Integration tests for ProjectSetup3 ProjectService API (no Rich TUI).

Objective: prove, in isolation, whether the public ProjectService API works
and reproduce the "Project language must be set before loading its
configuration" failure that the Rich TUI surfaces as a "TEXT" fallback.

Run:
    python -m pytest tests/integration/test_project_service.py -v
or standalone:
    python tests/integration/test_project_service.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from projectsetup3.src.core.models.Enums.RegistredProjectType import (
    RegistredProjectType as ProjectType,
)
from projectsetup3.src.core.models.Projects.Project import Project
from projectsetup3.src.core.Services.Engine.ProjectService import ProjectService
from projectsetup3.src.core.Services.Engine.ProjectFactory import ProjectFactory


# ---------------------------------------------------------------------------
# Test A — normalize_language
# ---------------------------------------------------------------------------
def test_normalize_language_variants():
    assert ProjectService.normalize_language("python") is ProjectType.PYTHON
    assert ProjectService.normalize_language("Python") is ProjectType.PYTHON
    assert ProjectService.normalize_language(".py") is ProjectType.PYTHON
    assert ProjectService.normalize_language("py") is ProjectType.PYTHON
    assert ProjectService.normalize_language("  python  ") is ProjectType.PYTHON
    print("[A] normalize_language variants -> PASS")


def test_normalize_language_unsupported():
    try:
        ProjectService.normalize_language("definitely_not_a_lang")
    except ValueError:
        print("[A] normalize_language unsupported -> PASS")
        return
    raise AssertionError("expected ValueError for unsupported language")


# ---------------------------------------------------------------------------
# Test B — loadProjectConfiguration via service
# ---------------------------------------------------------------------------
def test_load_project_configuration():
    service = ProjectService()
    try:
        structure = service.loadProjectConfiguration("python")
    except Exception as e:
        print(f"[B] FAIL -> {type(e).__name__}: {e}")
        raise
    assert isinstance(structure, dict)
    assert ".gitignore" in structure
    print("[B] loadProjectConfiguration('python') -> PASS, keys=", sorted(structure))


# ---------------------------------------------------------------------------
# Test C — create_project via service (temp dir)
# ---------------------------------------------------------------------------
def test_create_project(tmp_path):
    service = ProjectService()
    try:
        service.create_project(name="TestProject", language="python", path=tmp_path)
    except Exception as e:
        print(f"[C] FAIL -> {type(e).__name__}: {e}")
        raise
    created = tmp_path / "TestProject"
    assert created.is_dir()
    assert (created / ".gitignore").is_file()
    print(
        "[C] create_project('python') -> PASS, files=",
        sorted(p.name for p in created.iterdir()),
    )


# ---------------------------------------------------------------------------
# Test D — simulate the broken call (Factory receiving a Project w/o language)
# ---------------------------------------------------------------------------
def test_factory_without_language_raises_expected():
    factory = ProjectFactory()
    project = Project(name="", basestruture={})
    try:
        factory.loadProjectConfiguration(project=project)
    except ValueError as e:
        msg = str(e)
        print(f"[D] Factory w/o setLanguage -> raised ValueError: {msg!r}")
        assert "Project language must be set" in msg
        print("[D] reproduces EXACT reported error -> PASS")
        return
    raise AssertionError("expected ValueError but no exception raised")


# ---------------------------------------------------------------------------
# Standalone runner (no pytest required)
# ---------------------------------------------------------------------------
def _standalone():
    import tempfile

    test_normalize_language_variants()
    test_normalize_language_unsupported()
    test_load_project_configuration()
    with tempfile.TemporaryDirectory(prefix="ps3_itest_") as td:
        test_create_project(Path(td))
    test_factory_without_language_raises_expected()


if __name__ == "__main__":
    _standalone()
