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
from pathlib import Path

# ps3 <path:str> <type:str> <name:str>

data_local = Config()

@dataclass
class CLIService:
    def run(self):
        try:
            asyncio.run(tool.add_path_modules(data_local))
        except Exception as e:
            print(f"Erro ao adicionar paths: {e}")

        if len(sys.argv) < 2:
            subprocess.run([sys.executable, "ps3"])
        else:
            self.startProject(sys.argv)

    def startProject(self, argv):
        path = Path(argv[1]) if len(argv) > 1 else None
        typeProject = argv[2] if len(argv) > 2 and argv[2] else "python"
        name = argv[3] if len(argv) > 3 and argv[3] else "BaseProject"
        path = Path(path)

        if not path:
            print("[ERROR] É necessário passar pelo menos o caminho do projeto")
            return

        ProjectLocal = ProjectMaps.project_map[typeProject.lower()]()
        ProjectLocal.openBaseCodeJson()
        project_path = path if path else Config.DIRETORIO
        ProjectLocal.create(path=project_path,name = name)

if __name__ == "__main__":
    Service = CLIService()
    Service.run()


