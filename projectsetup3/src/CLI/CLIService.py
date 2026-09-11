import sys
import subprocess
import os
import asyncio
from pathlib import Path

# Ensure package can be imported when running script directly
try:
    import projectsetup3  # pragma: no cover
except ModuleNotFoundError:
    current = Path(__file__).resolve()
    repo_root = current.parents[2]
    sys.path.insert(0, str(repo_root))

from projectsetup3.src.core.tool import tool
from projectsetup3.src.config.Config import Config
from projectsetup3.src.core.Services.Engine.core.ProjectService import (
    ProjectService as ProjectManagerService,
)
from projectsetup3.src.UI.Icons import Icons
from projectsetup3.index import run
from projectsetup3.src.core.Services.Engine.Logger.LoggerService import LoggerService

from rich.console import Console
from rich.table import Table

# ps3cli <path:str> <type:str> <name:str> <gitRepoLink:str>(Opicional)
# ps3cli list <path:str> -> Return Projects In Path
# ps3cli -> Main Code

data_local = Config()


class CLIService:
    def __init__(self):
        self._logger = LoggerService.get_logger("CLIService")

    def run(self):
        self._logger.info("Iniciando CLIService")
        try:
            asyncio.run(tool.add_path_modules(data_local))
        except Exception as e:
            self._logger.error("Erro ao adicionar paths", error=str(e))
            print(f"Erro ao adicionar paths: {e}")

        if len(sys.argv) >= 2 and sys.argv[1] == "list":
            self.listDataProjects(sys.argv)
            return

        if len(sys.argv) >= 2:
            self.startProject(sys.argv)
            return

        try:
            self._logger.info("Executando interface interativa")
            run()
        except Exception as e:
            self._logger.error("Falha ao iniciar interface interativa", error=str(e))
            print(f"[ERROR] Falha ao iniciar interface interativa: {e}")

    def startProject(self, argv):
        try:
            self._logger.info("Criando projeto", args=argv[1:4])
            path = Path(argv[1]) if len(argv) > 1 else Config.DIRETORIO
            typeProject = argv[2] if len(argv) > 2 and argv[2] else "python"
            name = argv[3] if len(argv) > 3 and argv[3] else "BaseProject"
            gitRepoLink = argv[4] if len(argv) > 4 and argv[4] else None

            if not path.exists():
                self._logger.error("Caminho não existe", path=str(path))
                print(f"[ERROR] O caminho não existe: {path}")
                return

            if not path.is_dir():
                self._logger.error("Caminho não é diretório válido", path=str(path))
                print("[ERROR] O caminho precisa ser um diretório válido")
                return

            if (
                data_local.GitAvaliable
                and gitRepoLink
                and (not tool.verifyURL(url=gitRepoLink))
            ):
                self._logger.error("URL git inválida", url=gitRepoLink)
                print(f"[ERROR] O URL nao e valida: {gitRepoLink}")
                return

            self._logger.info("Projeto criado com sucesso", name=name, type=typeProject)
            ProjectManagerService.create_project(
                name=name, language=typeProject, path=path, gitRepoLink=gitRepoLink
            )
        except ValueError as VE:
            self._logger.error("Value Not Found", error=str(VE))
            print(f"[ERROR] Value Not Found , Erro: {VE}")
        except NotADirectoryError as NAD:
            self._logger.error("Erro de diretório", error=str(NAD))
            print(f"[ERROR] Erro: {NAD}")

    def listDataProjects(self, argv) -> None:
        if argv[2] == ".":
            path = Path(os.getcwd())
        elif argv[2] == "py":
            path = Config.DIRETORIO
        elif argv[2] == "web":
            path = Config.DIRETORIO_WEB
        elif argv[2] == "cpp":
            path = Config.DIRETORIO_CPP
        else:
            path = Path(argv[2])

        if not path.exists() or not path.is_dir():
            self._logger.error("Caminho inválido", path=str(path))
            print(f"[ERROR] Caminho inválido: {path}")
            return

        projects = [p for p in path.iterdir() if p.is_dir()]

        console = Console()
        table = Table(
            title=f"📂 Projetos em: [bold yellow]{path}[/]",
            show_header=True,
            header_style="bold white on blue",
            border_style="bright_blue",
            expand=True,
            box=None,
            padding=(0, 2),
            show_lines=False,
        )

        table.add_column("Nome", style="bold cyan", no_wrap=True)
        table.add_column("Tipo", style="green", justify="left")
        table.add_column("Git", style="magenta", justify="center")
        table.add_column("Caminho Completo", style="italic white")

        for project in projects:
            project_type = "Desconhecido"
            files = list(project.iterdir())

            for ptype, rules in Config.PROJECT_TYPES.items():
                if any((project / f).exists() for f in rules["files"]):
                    project_type = ptype.capitalize()
                    break

            if project_type == "Desconhecido":
                for ptype, rules in Config.PROJECT_TYPES.items():
                    if any(
                        f.suffix in rules["extensions"] for f in files if f.is_file()
                    ):
                        project_type = ptype.capitalize()
                        break

            isGit = (project / ".git").exists()
            git_status = "✅" if isGit else "❌"

            row_style = "on #152b15" if isGit else None

            icon = Icons.getIconProject(project_type)
            table.add_row(
                f"{icon} {project.name}",
                f"[bold]{project_type}[/]",
                f"{git_status}",
                str(project.resolve()),
                style=row_style,
            )

        console.print(table)


def main():
    service = CLIService()
    service.run()


if __name__ == "__main__":
    main()
