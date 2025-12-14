import sys
import subprocess
import os
import asyncio
from pathlib import Path
from projectsetup3.tool import tool
from projectsetup3.Config import Config
from projectsetup3.Services.ProjectManagerService import ProjectManagerService
from projectsetup3.modules.Class.Icons import Icons

from rich.console import Console
from rich.table import Table

# ps3cli <path:str> <type:str> <name:str> <gitRepoLink:str>(Opicional) 
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
            # Futuramente colcoar argparse
            path = Path(argv[1]) if len(argv) > 1 else Config.DIRETORIO
            typeProject = argv[2] if len(argv) > 2 and argv[2] else "python"
            name = argv[3] if len(argv) > 3 and argv[3] else "BaseProject"
            gitRepoLink = argv[4] if len(argv) > 4 and argv[4] else None 

            if not path.exists():
                print(f"[ERROR] O caminho não existe: {path}")
                return

            if not path.is_dir():
                print("[ERROR] O caminho precisa ser um diretório válido")
                return
            
            if gitRepoLink and data_local.GitAvaliable and (not tool.verifyURL(url = gitRepoLink)):
                print(f"[ERROR] O URL nao e valida: {path}")
                return
                        
            ProjectManagerService.create_project(name=name,language=typeProject,path=path,gitRepoLink=gitRepoLink)
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
        table = Table(
            title=f"📂 Projetos em: [bold yellow]{path}[/]", 
            show_header=True, 
            header_style="bold white",
            border_style="bright_blue",
            expand=True,
            box=None,
            show_lines=True
        )

        table.add_column("Nome", style="bold cyan", no_wrap=True)
        table.add_column("Tipo", style="green", justify="center")
        table.add_column("Caminho Completo", style="italic dim")

        for project in projects:
            project_type = "Desconhecido"
            files = list(project.iterdir())
            
            # Detecta tipo baseado em arquivos específicos
            for ptype, rules in Config.PROJECT_TYPES.items():
                if any((project / f).exists() for f in rules["files"]):
                    project_type = ptype.capitalize()
                    break
                
            # Verifica extensões se não encontrou por arquivo
            if project_type == "Desconhecido":
                for ptype, rules in Config.PROJECT_TYPES.items():
                    if any(f.suffix in rules["extensions"] for f in files if f.is_file()):
                        project_type = ptype.capitalize()
                        break
                    
            icon = Icons.getIconProject(project_type)
            table.add_row(f"{icon} {project.name}", f"[bold]{project_type}[/]", str(project.resolve()))

        console.print(table)

def main():
    service = CLIService()
    service.run()

if __name__ == "__main__":
    main()
