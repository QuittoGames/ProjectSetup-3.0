
import os
import platform
from dataclasses import dataclass
from projectsetup3.Config import Config
from projectsetup3.modules.Enums.ProjectType import ProjectType
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from datetime import datetime
from pathlib import Path
import shutil
import re

@dataclass
class tool:
    def clear_screen():
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    async def verify_modules():
        try:
            # #Uso Do modules por txt
            req_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "requirements", "requirements.txt"))
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
        except Exception as E:
            print(f"Erro Na Verificaçao De Modulos, Erro: {E}")
            return
        
    async def add_path_modules(data_local:Config):
        if Config.modules_local == None:return
        try:
            for i in Config.modules_local:
                sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), i)))
                if data_local.Debug:print(f"Module_local: {i}")
            return
        except Exception as E:
            print(f"Erro Al Adicionar Os Caminhos Brutos, Erro: {E}")
            return
        
    def menu():
        tool.clear_screen()
        console = Console()
        console.print(
            Panel(
                "[bold cyan]ProjectSetup 3.0[/bold cyan]",
                border_style="cyan",
                box=ROUNDED,
                width=60,
                padding=(1, 2)
            )
    )

    def get_sys_info():
        """Coleta informações do sistema."""
        return {
            "os": platform.system(),
            "py_ver": sys.version.split()[0],
            "user": os.getlogin() if hasattr(os, "getlogin") else "User",
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d/%m/%Y")
        }

    def type_to_extension(project_type: str) -> str:
        try:
            return ProjectType[project_type.upper()].value
        except KeyError:
            return ".txt"

    #Project created successfully!

    def init_git_repository(link: str, path: Path) -> None:
        try:
            # init (caso ainda não exista)
            if not (path / ".git").is_dir():
                subprocess.run(
                    ["git", "init"],
                    cwd=path,
                    check=True
                )

            # configura remote origin
            remotes = subprocess.run(
                ["git", "remote"],
                cwd=path,
                check=True,
                capture_output=True,
                text=True
            ).stdout.split()

            if "origin" in remotes:
                subprocess.run(
                    ["git", "remote", "set-url", "origin", link],
                    cwd=path,
                    check=True
                )
            else:
                subprocess.run(
                    ["git", "remote", "add", "origin", link],
                    cwd=path,
                    check=True
                )

            # add / commit inicial
            subprocess.run(["git", "add", "-A"], cwd=path, check=True)

            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=path,
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()

            if status:
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    cwd=path,
                    check=True
                )

            subprocess.run(["git", "branch", "-M", "main"], cwd=path, check=False)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=path, check=False)

        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar git: {e}")
        except Exception as e:
            print(f"Erro ao iniciar repositorio git: {e}")


    def verifyURL(url:str) -> bool:
        if url is None:return False
        return bool(re.match(r'^https://(github\.com|gitlab\.com|bitbucket\.org)/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+(\.git)?$', url))
    
    def getIsntallCommand() -> str:
        packageManeger = ""
        managers = ["apt", "dnf", "pacman", "zypper", "apk"]  # apk = Alpine
        for m in managers:
            if shutil.which(m):
                packageManeger = m 

        install_cmds = {
            "apt": lambda pkg: f"sudo apt update && sudo apt install -y {pkg}",
            "dnf": lambda pkg: f"sudo dnf install -y {pkg}",
            "pacman": lambda pkg: f"sudo pacman -Syu {pkg} --noconfirm",
            "zypper": lambda pkg: f"sudo zypper install -y {pkg}",
            "apk": lambda pkg: f"sudo apk add {pkg}",
        }

        return install_cmds.get(packageManeger)
    