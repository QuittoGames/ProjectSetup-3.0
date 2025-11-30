from pathlib import Path
import asyncio
import time
from datetime import datetime
import sys
import msvcrt

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.box import ROUNDED

from tool import tool
from Config import Config
from Services.ArrowsService import ArrrowsService
from Services.ProjectManagerService import ProjectManagerService

console = Console()
config = Config()

def print_project_summary(name: str, lang: str, path: Path, base: dict):
    tree = "\n".join(f" • {key}" for key in base.keys())
    now = datetime.now().strftime("%d/%m/%Y • %H:%M:%S")

    summary = (
        f"[bold cyan]Resumo do Projeto Criado[/bold cyan]\n\n"
        f"[cyan]Nome:[/cyan] {name}\n"
        f"[cyan]Linguagem:[/cyan] {lang}\n"
        f"[cyan]Diretório:[/cyan] {path}\n"
        f"[cyan]Criado em:[/cyan] {now}\n\n"
        f"[dim]Estrutura Inicial:[/dim]\n"
        f"{tree}"
    )

    console.print(Panel(summary, border_style="green", box=ROUNDED, width=72, padding=1))

    confirm = console.input("[bold]Confirmar criação?[/bold] [green](y para sim)[/green]: ")

    if confirm.lower() != "y":
        console.print("[yellow]Cancelado pelo usuário.[/yellow]")
        return False

    return True


# =======================================================
# HEADER — estilo Neovim
# =======================================================
def header():
    tool.clear_screen()

    title = Text(" ProjectSetup 3.0 ", style="bold cyan")
    subtitle = Text(" Core Manager • Project Automation ", style="green")

    console.print(
        Panel(
            Text.assemble(title, "\n", subtitle),
            border_style="cyan",
            width=72,
            padding=(1, 2),
            box=ROUNDED,
        )
    )


# =======================================================
# CONFIG
# =======================================================
def config_screen():
    tool.clear_screen()

    console.print(
        Panel(
            "[cyan]Área de Configurações[/cyan]\n"
            "[dim]Em desenvolvimento...[/dim]",
            border_style="cyan",
            box=ROUNDED,
            width=60,
        )
    )

    input("\nPressione ENTER para voltar...")


# =======================================================
# CRIAR PROJETO
# =======================================================
def create_project_interactive():
    tool.clear_screen()

    console.print(
        Panel("[bold cyan]Novo Projeto[/bold cyan]", border_style="cyan", box=ROUNDED, width=60)
    )

    name = input("Nome do Projeto: ").strip()
    if not name:
        console.print("[red]Nome inválido.[/red]")
        return

    TypeProject = input("Linguagem (default = python): ").strip().lower() or "python"

    console.print(
        Panel(
            f"[cyan]Path do projeto[/cyan]\n"
            f"[dim]Pressione Enter para usar o padrão:[/dim]\n"
            f"[green]{config.DIRETORIO}[/green]",
            border_style="cyan",
            box=ROUNDED,
            width=60,
        )
    )

    raw_path = input("Path: ").strip()
    path = Path(raw_path) if raw_path else Config.dispatch_path(TypeProject)

    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[red]Erro ao criar diretório: {e}[/red]")
        return

    try:
        base = ProjectManagerService.get_base_structure(TypeProject)

        if not print_project_summary(name, TypeProject, path, base):
            return

        ProjectManagerService.create_project(
            name=name,
            language=TypeProject,
            path=path
        )

        console.print(
            Panel(
                f"[bold green]Projeto criado com sucesso![/bold green]\n"
                f"[cyan]{path}[/cyan]",
                border_style="green",
                box=ROUNDED,
                width=60,
            )
        )

    except Exception as e:
        console.print(f"[red]Erro ao criar projeto: {e}[/red]")


# =======================================================
# LOOP PRINCIPAL
# =======================================================
def Start():
    while True:
        header()

        options = [
            "Criar Projeto",
            "Verificar Módulos",
            "Configurações",
            "Sair",
        ]

        choice = ArrrowsService.arrow_menu(options)

        if choice == 0:
            create_project_interactive()

        elif choice == 1:
            if config.Debug:
                tool.clear_screen()
                console.print("[cyan]Verificando módulos...[/cyan]\n")
                asyncio.run(tool.verify_modules())
            else:
                console.print("[red]Debug está desativado.[/red]")

        elif choice == 2:
            config_screen()

        elif choice == 3:
            console.print("\n[dim]Saindo...[/dim]")
            return

        input("\nPressione ENTER para continuar...")


# =======================================================
# MAIN ASSÍNCRONO
# =======================================================
async def main():
    try:
        cfg = Config()
        await tool.add_path_modules(cfg)

        if cfg.Debug:
            await tool.verify_modules()

    except Exception as e:
        console.print(f"[red][ERROR][/red] {e}")


if __name__ == "__main__":
    asyncio.run(main())
    Start()
from pathlib import Path
import asyncio
import time
from datetime import datetime
import sys
import msvcrt

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.box import ROUNDED

from tool import tool
from Config import Config
from Services.ProjectManagerService import ProjectManagerService

console = Console()
config = Config()

# =======================================================
# RESUMO DO PROJETO
# =======================================================
def print_project_summary(name: str, lang: str, path: Path, base: dict):
    tree = "\n".join(f" • {key}" for key in base.keys())
    now = datetime.now().strftime("%d/%m/%Y • %H:%M:%S")

    summary = (
        f"[bold cyan]Resumo do Projeto Criado[/bold cyan]\n\n"
        f"[cyan]Nome:[/cyan] {name}\n"
        f"[cyan]Linguagem:[/cyan] {lang}\n"
        f"[cyan]Diretório:[/cyan] {path}\n"
        f"[cyan]Criado em:[/cyan] {now}\n\n"
        f"[dim]Estrutura Inicial:[/dim]\n"
        f"{tree}"
    )

    console.print(Panel(summary, border_style="green", box=ROUNDED, width=72, padding=1))

    confirm = console.input("[bold]Confirmar criação?[/bold] [green](y para sim)[/green]: ")

    if confirm.lower() != "y":
        console.print("[yellow]Cancelado pelo usuário.[/yellow]")
        return False

    return True


# =======================================================
# HEADER — estilo Neovim
# =======================================================
def header():
    tool.clear_screen()

    title = Text("ProjectSetup 3.0 ", style="bold cyan")
    subtitle = Text("Advanced Project Builder ", style="green")

    console.print(
        Panel(
            Text.assemble(title, "\n", subtitle),
            border_style="cyan",
            width=72,
            padding=(1, 2),
            box=ROUNDED,
        )
    )


# =======================================================
# CONFIG
# =======================================================
def config_screen():
    tool.clear_screen()

    console.print(
        Panel(
            "[cyan]Área de Configurações[/cyan]\n"
            "[dim]Em desenvolvimento...[/dim]",
            border_style="cyan",
            box=ROUNDED,
            width=60,
        )
    )

    input("\nPressione ENTER para voltar...")


# =======================================================
# CRIAR PROJETO
# =======================================================
def create_project_interactive():
    tool.clear_screen()

    console.print(
        Panel("[bold cyan]Novo Projeto[/bold cyan]", border_style="cyan", box=ROUNDED, width=60)
    )

    name = input("Nome do Projeto: ").strip()
    if not name:
        console.print("[red]Nome inválido.[/red]")
        return

    TypeProject = input("Linguagem (default = python): ").strip().lower() or "python"

    console.print(
        Panel(
            f"[cyan]Path do projeto[/cyan]\n"
            f"[dim]Pressione Enter para usar o padrão:[/dim]\n"
            f"[green]{config.DIRETORIO}[/green]",
            border_style="cyan",
            box=ROUNDED,
            width=60,
        )
    )

    raw_path = input("Path: ").strip()
    path = Path(raw_path) if raw_path else Config.dispatch_path(TypeProject)

    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[red]Erro ao criar diretório: {e}[/red]")
        return

    try:
        base = ProjectManagerService.get_base_structure(TypeProject)

        if not print_project_summary(name, TypeProject, path, base):
            return

        ProjectManagerService.create_project(
            name=name,
            language=TypeProject,
            path=path
        )

        console.print(
            Panel(
                f"[bold green]Projeto criado com sucesso![/bold green]\n"
                f"[cyan]{path}[/cyan]",
                border_style="green",
                box=ROUNDED,
                width=60,
            )
        )

    except Exception as e:
        console.print(f"[red]Erro ao criar projeto: {e}[/red]")


# =======================================================
# LOOP PRINCIPAL
# =======================================================
def Start():
    while True:
        header()

        options = [
            "Criar Projeto",
            "Verificar Módulos",
            "Configurações",
            "Sair",
        ]

        choice = ArrrowsService.arrow_menu(options)

        if choice == 0:
            create_project_interactive()

        elif choice == 1:
            if config.Debug:
                tool.clear_screen()
                console.print("[cyan]Verificando módulos...[/cyan]\n")
                asyncio.run(tool.verify_modules())
            else:
                console.print("[red]Debug está desativado.[/red]")

        elif choice == 2:
            config_screen()

        elif choice == 3:
            tool.clear_screen()
            console.print("\n[dim]Saindo...[/dim]")
            return

        input("\nPressione ENTER para continuar...")


# =======================================================
# MAIN ASSÍNCRONO
# =======================================================
async def main():
    try:
        cfg = Config()
        await tool.add_path_modules(cfg)

        if cfg.Debug:
            await tool.verify_modules()

    except Exception as e:
        console.print(f"[red][ERROR][/red] {e}")


if __name__ == "__main__":
    asyncio.run(main())
    Start()
