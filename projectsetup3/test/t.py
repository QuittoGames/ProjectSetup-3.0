"""Runnable test harness for `ProjectManagerService`.

Creates a temporary project using the base templates and prints created files.
"""

from pathlib import Path
import tempfile
import sys

# Ensure local package is importable when running this test from inside the package
try:
	import projectsetup3  # pragma: no cover
except ModuleNotFoundError:
	repo_root = Path(__file__).resolve().parents[1]
	sys.path.insert(0, str(repo_root))

from projectsetup3.Config import Config
from projectsetup3.Services.ProjectManagerService import ProjectManagerService


def main():
	tmp = tempfile.TemporaryDirectory(prefix="ps3_test_")
	base_path = Path(tmp.name)
	name = "test_project"
	language = "python"

	print(f"Creating project '{name}' (language={language}) in {base_path}")
	try:
		ProjectManagerService.create_project(name=name, language=language, path=base_path)
	except Exception as e:
		print(f"Error creating project: {e}")
		tmp.cleanup()
		sys.exit(1)

	project_dir = base_path / name
	print(f"Project created at: {project_dir}")
	for p in sorted(project_dir.rglob("*")):
		rel = p.relative_to(project_dir)
		if p.is_dir():
			print(f"  [dir]  {rel}")
		else:
			print(f"  [file] {rel}")

	tmp.cleanup()


if __name__ == "__main__":
	main()