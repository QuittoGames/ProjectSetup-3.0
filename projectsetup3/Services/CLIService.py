import sys
import subprocess
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from tool import tool
import asyncio
from Config import Config
from Services.ProjectManagerService import ProjectManagerService
from pathlib import Path

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


    def listDataProjects(self,argv) -> None:
        path = Path(argv[2]) if len(argv) == 3 else Config.DIRETORIO

        Folders:list = os.listdir(path)

        for i in Folders:
            print(i)

def main():
    service = CLIService()
    service.run()

if __name__ == "__main__":
    main()
