
import os
import platform
from dataclasses import dataclass
from Config import Config
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from datetime import datetime

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

            #Project created successfully!