from dataclasses import dataclass
import sys
import subprocess
from typing import overload
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from tool import tool
import asyncio
from Config import Config
from modules.DataMap.project_map import ProjectMaps
from Services.ProjectManagerService import ProjectManagerService
from pathlib import Path
from time import sleep

# ps3cli <path:str> <type:str> <name:str>

data_local = Config()

@dataclass
class CLIService:
    def run(self):
        try:
            asyncio.run(tool.add_path_modules(data_local))
        except Exception as e:
            print(f"Erro ao adicionar paths: {e}")

        if len(sys.argv) >= 2:
            self.startProject(sys.argv)
            return

        try:
            if os.name == "Linux":
                subprocess.run([sys.executable, "ps3"], check=False)
            else:
                subprocess.run(["ps3.bat"], shell=True, check=False)
        except FileNotFoundError:
            print("[ERROR] Entry script 'ps3' not found. Ensure 'ps3' or 'ps3.bat' exists in the project root")

    def startProject(self, argv):
        try:
            # Add agoritmo for if one value is none the outher values iis this value modify the command stuture
            path = Path(argv[1]) if len(argv) > 1 else None
            typeProject = argv[2] if len(argv) > 2 and argv[2] else "python"
            name = argv[3] if len(argv) > 3 and argv[3] else "BaseProject"
            path = Path(path)

            if os.path.isfile(path):
                raise NotADirectoryError("Expected a directory, got a file instead.")
            
            if not path:
                print("[ERROR] É necessário passar pelo menos o caminho do projeto")
                return
            
            ProjectManagerService.create_project(name=name,language=typeProject,path=path)
        except ValueError as VE:
            print(f"[ERROR] Value Not Found , Erro: {VE}")
        except NotADirectoryError as NAD:
            print(f"[ERROR] Erro: {NAD}")

if __name__ == "__main__":
    Service = CLIService()
    Service.run()


