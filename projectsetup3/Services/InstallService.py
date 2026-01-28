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

        if not appdata_local.exists() or not all((appdata_local / f).exists() for f in ["python.json","java.json"]):
            InstallService.checkDependencies()
            InstallService.getData()
    
        # Cria diretórios necessários
        dest_languages = config.appdata / "Languages"
        dest_languages.mkdir(parents=True, exist_ok=True)
        
        dest_history = config.appdata / "History"
        dest_history.mkdir(parents=True, exist_ok=True)

        # Remove estruturas antigas incorretas se existirem
        old_structures = [
            config.appdata / "PROJECTSETUP-3.O",
            config.appdata / "Languages" / "ProjectSetup-3.0-main"
        ]
        
        for old_path in old_structures:
            if old_path.exists():
                shutil.rmtree(old_path)
        
        # Copia todos os arquivos .json
        for json_file in appdata_local.glob("*.json"):
            shutil.copy2(json_file, dest_languages / json_file.name)
    
        InstallService.setEnv()

    @staticmethod
    def setEnv() -> None:
        path = os.getcwd()
        
        try:
            if platform.system() == "Windows":
                command = f'setx PATH "%PATH%;{path}"'
                subprocess.run(command, shell=True, check=True)
            else:
                # Linux/Unix: adiciona ao .bashrc se não existir
                command = f'grep -qxF \'export PATH="$PATH:{path}"\' ~/.bashrc || echo \'export PATH="$PATH:{path}"\' >> ~/.bashrc'
                subprocess.run(command, shell=True, check=True, executable='/bin/bash')
        except subprocess.CalledProcessError as e:
            console = Console()
            console.print(f"[bold red]Erro ao configurar PATH:[/bold red] {e}")
    
    @staticmethod
    def checkDependencies():
        tool.clear_screen()
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
        console = Console()
        
        if platform.system() == "Windows":
            powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
            command = (
                f'curl -L https://github.com/QuittoGames/ProjectSetup-3.0/archive/refs/heads/main.zip -o repo.zip && '
                f'"{powershell_path}" -Command "Expand-Archive -Force repo.zip .; '
                'New-Item -ItemType Directory -Force appdata\\Languages | Out-Null; '
                'Copy-Item ProjectSetup-3.0-main\\projectsetup3\\appdata\\Languages\\*.json appdata\\Languages\\ -Force; '
                'Remove-Item -Recurse -Force ProjectSetup-3.0-main, repo.zip"'
            )
        else:
            # Cria diretório se não existir
            Path("appdata/Languages").mkdir(parents=True, exist_ok=True)

            command = (
                'curl -L https://github.com/QuittoGames/ProjectSetup-3.0/archive/refs/heads/main.zip -o repo.zip && '
                'unzip -o repo.zip && '
                'cp ProjectSetup-3.0-main/projectsetup3/appdata/Languages/*.json appdata/Languages/ && '
                'rm -rf ProjectSetup-3.0-main repo.zip'
            )

        try:
            subprocess.run(command, shell=True, check=True)
            console.print("[bold green]✓[/bold green] Arquivos de linguagem baixados com sucesso!")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]✘ Erro ao baixar dados:[/bold red] {e}")
            raise
        
    @staticmethod
    def isIstall(config: Config) -> bool:
        languages_path = config.appdata / "Languages"
        if languages_path.exists() and any(languages_path.glob("*.json")):
            return True
        return False
