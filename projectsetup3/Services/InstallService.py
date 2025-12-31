from dataclasses import dataclass
from Config import Config
import os
import shutil
from pathlib import Path
import subprocess
from rich.console import Console
import platform


@dataclass
class InstallService:
    @staticmethod
    def install(config: Config) -> None:
        appdata_local = Path(os.getcwd()) / "appdata" / "Languages"

        if not appdata_local.exists():return

        if Path(config.appdata / "PROJECTSETUP-3.O").exists():return

        Path(config.appdata / "PROJECTSETUP-3.O").parent.mkdir(parents=True, exist_ok=True)
        Path(config.appdata / "History").parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(appdata_local), str(config.appdata))
    
        InstallService.setEnv()

    @staticmethod
    def setEnv() -> None:
        command = (
            f'setx PATH "%PATH%;{os.getcwd()}"'
            if platform.system() == "Windows"
            else f'echo \'export PATH="$PATH:{os.getcwd()}"\' >> ~/.bashrc'
        )

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            console = Console()
            console.print(f"[bold red]Erro ao configurar PATH:[/bold red] {e}")
            
            
        
            
