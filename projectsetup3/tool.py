
import os
import platform
from dataclasses import dataclass
from projectsetup3.Config import Config
from modules.Enums.ProjectType import ProjectType
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from datetime import datetime
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

    def init_git_repository(link: str) -> None:
        try:
            # init (caso ainda não exista)
            if not os.path.isdir(".git"):
                subprocess.run(["git", "init"], check=True)

            # configura remote origin (cria ou atualiza)
            remotes = subprocess.run(
                ["git", "remote"],
                check=True,
                capture_output=True,
                text=True
            ).stdout.split()

            if "origin" in remotes:
                subprocess.run(["git", "remote", "set-url", "origin", link], check=True)
            else:
                subprocess.run(["git", "remote", "add", "origin", link], check=True)

            # add/commit inicial (se tiver arquivos)
            subprocess.run(["git", "add", "-A"], check=True)

            status = subprocess.run(
                ["git", "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()

            if status:
                subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

            # tenta definir branch main e fazer push (não falha se não der)
            subprocess.run(["git", "branch", "-M", "main"], check=False)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=False)

        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar git: {e}")
        except Exception as e:
            print(f"Erro ao iniciar repositorio git: {e}")

    def verifyURL(url:str) -> bool:
        return bool(re.match(r'^https://(github\.com|gitlab\.com|bitbucket\.org)/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+(\.git)?$', url))