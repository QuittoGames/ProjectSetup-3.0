import sys
import subprocess
import os
import asyncio
from pathlib import Path
from projectsetup3.tool import tool
from projectsetup3.Config import Config
from projectsetup3.Services.ProjectManagerService import ProjectManagerService

from rich.console import Console
from rich.table import Table

# ps3cli <path:str> <type:str> <name:str>
# ps3cli list <path:str> -> Return Projects In Path 
# ps3cli -> Main Code

data_local = Config()

class CLIService:
    def run(self):
        try:
            asyncio.run(tool.add_path_modules(data_local))
        except Exception as e:
            print(f"Erro ao adicionar paths: {e}")

        if len(sys.argv) >= 2 and sys.argv[1] == "list":
            self.listDataProjects(sys.argv)
            return

        if len(sys.argv) >= 2:
            self.startProject(sys.argv)
            return

        try:
            root = Path(__file__).resolve().parent
            script = root / ("ps3.bat" if os.name == "nt" else "ps3")
            subprocess.run([sys.executable, script],shell=False)
        except FileNotFoundError:
            print("[ERROR] Entry script 'ps3' not found. Ensure 'ps3' or 'ps3.bat' exists in the project root")

    def startProject(self, argv):
        try:
            # Add agoritmo for if one value is none the outher values iis this value modify the command stuture
            path = Path(argv[1]) if len(argv) > 1 else None
            typeProject = argv[2] if len(argv) > 2 and argv[2] else "python"
            name = argv[3] if len(argv) > 3 and argv[3] else "BaseProject"

            if not path:
                print("[ERROR] É necessário passar o caminho do projeto")
                subprocess.run("echo É necessário passar o caminho do projeto")
                return

            if not path.exists():
                print(f"[ERROR] O caminho não existe: {path}")
                return

            if not path.is_dir():
                print("[ERROR] O caminho precisa ser um diretório válido")
                return
                        
            ProjectManagerService.create_project(name=name,language=typeProject,path=path)
        except ValueError as VE:
            print(f"[ERROR] Value Not Found , Erro: {VE}")
        except NotADirectoryError as NAD:
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
            print(f"[ERROR] Caminho inválido: {path}")
            return

        projects = [p for p in path.iterdir() if p.is_dir()]

        console = Console()
        table = Table(title=f"Projetos em: {path}", show_header=True, header_style="bold blue")

        table.add_column("Nome", style="cyan", no_wrap=True)
        table.add_column("Tipo", style="green")
        table.add_column("Caminho Completo", style="dim")
        
        #Refactor for dict
        for project in projects:
            project_type = "Desconhecido"

            files = list(project.iterdir())  # evita iterar várias vezes

            # Python
            if (
                (project / "requirements.txt").exists()
                or (project / "pyproject.toml").exists()
                or any(f.suffix == ".py" for f in files)
            ):
                project_type = "Python"

            # Node / JavaScript / TypeScript
            elif (project / "package.json").exists() or any(
                f.suffix in {".js", ".ts", ".tsx"} for f in files
            ):
                project_type = "Node/JS"

            # Java
            elif (project / "pom.xml").exists() or any(
                f.suffix == ".java" for f in files
            ):
                project_type = "Java"

            # Rust
            elif (project / "Cargo.toml").exists() or any(
                f.suffix == ".rs" for f in files
            ):
                project_type = "Rust"

            # C++
            elif any(f.suffix in {".cpp", ".cc", ".cxx", ".hpp", ".h"} for f in files):
                project_type = "C++"

            # C
            elif any(f.suffix in {".c", ".h"} for f in files):
                project_type = "C"

            # Go
            elif any(f.suffix == ".go" for f in files):
                project_type = "Go"

            # C#
            elif any(f.suffix in {".cs", ".csproj"} for f in files):
                project_type = "C#"

            # Ruby
            elif any(f.suffix == ".rb" for f in files):
                project_type = "Ruby"

            # Lua (inclui Roblox Lua)
            elif any(f.suffix == ".lua" for f in files):
                project_type = "Lua"

            # Shell / Bash
            elif any(f.suffix in {".sh", ".bash"} for f in files):
                project_type = "Shell"

            # YAML
            elif any(f.suffix in {".yaml", ".yml"} for f in files):
                project_type = "YAML"

            # Web / HTML / CSS
            elif any(f.suffix in {".html", ".css"} for f in files):
                project_type = "Web"
            
            table.add_row(f"📁 {project.name}", project_type, str(project.resolve()))

        console.print(table)

def main():
    service = CLIService()
    service.run()

if __name__ == "__main__":
    main()
