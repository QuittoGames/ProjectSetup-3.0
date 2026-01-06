from dataclasses import dataclass
from projectsetup3.Config import Config
from projectsetup3.tool import tool
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

        if not appdata_local.exists():
            InstallService.checkDependencies()
            InstallService.getData()
    
        Path(config.appdata / "PROJECTSETUP-3.O").parent.mkdir(parents=True, exist_ok=True)
        Path(config.appdata / "History").parent.mkdir(parents=True,exist_ok=True)

        dest = config.appdata / "PROJECTSETUP-3.O" / "Languages"
        shutil.copytree(appdata_local, dest, dirs_exist_ok=True)
    
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
    
    def checkDependencies():
        console = Console()
        deps = ["curl", "unzip"] if platform.system() != "Windows" else []
        for dep in deps:
            if shutil.which(dep) is None:
                console.print(f"[bold yellow]Aviso:[/bold yellow] {dep} não encontrado.")
                resposta = input(f"Quer instalar o {dep}? (y/n): ").strip().lower()
                if resposta == "y":
                    if platform.system() == "Windows":
                        try:
                            subprocess.run(f"winget install --id {dep} -e", shell=True, check=True)
                        except subprocess.CalledProcessError:
                            console.print(f"[bold red]Erro:[/bold red] Não foi possível instalar {dep} automaticamente.")
                            return
                    return
                #Linux
                try:
                    cmd = tool.getIsntallCommand()
        
                    if cmd:
                        subprocess.run(cmd, shell=True, check=True)
                    else:
                        print(f"Gerenciador {cmd} detectado, mas não há comando definido. Instale {dep} manualmente.")

                except Exception as E:
                    console.print(f"[bold red]Erro:[/bold red] Não foi possível instalar {dep} automaticamente.")
                
    @staticmethod
    def getData():
        if platform.system() == "Windows":
            powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
            command = (
                f'curl -L https://github.com/QuittoGames/ProjectSetup-3.0/archive/refs/heads/main.zip -o repo.zip && '
                f'"{powershell_path}" -Command "Expand-Archive -Force repo.zip repo; '
                'New-Item -ItemType Directory -Force appdata | Out-Null; '
                'Move-Item repo\\ProjectSetup-3.0-main\\projectsetup3\\appdata\\Languages appdata\\Languages"'
            )
        else:
            Path("appdata/Languages").mkdir(parents=True, exist_ok=True) if not os.path.exists("appdata/Languages") else None

            command = (
                'curl -L https://github.com/QuittoGames/ProjectSetup-3.0/archive/refs/heads/main.zip -o repo.zip && '
                'unzip -o repo.zip '
                '"ProjectSetup-3.0-main/projectsetup3/appdata/Languages/*" '
                '-d appdata/Languages && '
                'rm repo.zip'
            )

        subprocess.run(command, shell=True, check=True)
        
    @staticmethod
    def isIstall(config: Config) -> bool:
        if Path(config.appdata / "PROJECTSETUP-3.O").exists():
            return True
        return False
