from pathlib import Path
import asyncio
import time
from datetime import datetime
import sys
import os

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED, HEAVY, DOUBLE
from rich.table import Table
from rich.tree import Tree
from rich.padding import Padding
from rich.align import Align

from projectsetup3.tool import tool
from projectsetup3.Config import Config
from projectsetup3.Services.ArrowsService import ArrrowsService
from projectsetup3.Services.ProjectManagerService import ProjectManagerService
from projectsetup3.modules.Class.Icons import Icons

# =======================================================
# TEMA MODERNO - AZUL E PRETO (Inspirado NeoVim)
# =======================================================
theme_color = "bright_blue"      # Azul principal
accent_color = "cyan"            # Azul claro para destaques
success_color = "green"          # Verde para sucesso
warning_color = "yellow"         # Amarelo para avisos
text_dim = "bright_black"        # Cinza escuro
text_main = "white"              # Branco principal
bg_dark = "black"                # Fundo escuro

config = Config()
console = Console()

# =======================================================
# HELPERS VISUAIS
# =======================================================

def draw_main_dashboard():
    """Dashboard principal com design moderno e minimalista."""
    tool.clear_screen()
    
    info = tool.get_sys_info()
    
    # Taskbar superior - linha única compacta
    taskbar = Table.grid(expand=True, padding=0)
    taskbar.add_column(justify="left", ratio=1)
    taskbar.add_column(justify="center", ratio=2)
    taskbar.add_column(justify="right", ratio=1)
    
    # Esquerda - User
    left_text = Text.assemble(
        ("● ", success_color),
        (f"{info['user']}", accent_color)
    )
    
    # Centro - Nome do app
    center_text = Text("PROJECT SETUP v3.0", style=f"bold {theme_color}")
    
    # Direita - Sistema
    right_text = Text.assemble(
        (f"{info['os']} ", text_dim),
        ("| ", text_dim),
        (f"Py {info['py_ver']} ", text_dim),
        ("| ", text_dim),
        (f"{info['time']}", accent_color)
    )
    
    taskbar.add_row(left_text, Align.center(center_text), right_text)
    
    # Painel taskbar
    taskbar_panel = Panel(
        taskbar,
        box=ROUNDED,
        border_style=theme_color,
        padding=(0, 2),
        width=90
    )
    
    console.print(Align.center(taskbar_panel))
    console.print()

def make_simple_header(title_str="Menu"):
    """Header minimalista para telas internas."""
    tool.clear_screen()
    
    info = tool.get_sys_info()
    
    # Header em painel arredondado
    header_grid = Table.grid(expand=True)
    header_grid.add_column(justify="center")
    
    title = Text(title_str.upper(), style=f"bold {theme_color}")
    subtitle = Text(f"{info['time']} • {info['user']}@{info['os']}", style=text_dim)
    
    header_grid.add_row(title)
    header_grid.add_row(subtitle)
    
    header_panel = Panel(
        header_grid,
        box=ROUNDED,
        border_style=theme_color,
        padding=(0, 2),
        width=60
    )
    
    console.print(Align.center(header_panel))
    console.print()

# =======================================================
# MENU PRINCIPAL COM UX MELHORADA
# =======================================================
def draw_menu_options():
    options = [
        f"{Icons.get_icon('new_project')} Novo Projeto",
        f"{Icons.get_icon('modules')} Módulos",
        f"{Icons.get_icon('settings')} Configurações",
        f"{Icons.get_icon('exit')} Sair",
    ]

    console.print()

    title = Panel(
        Align.center(Text(" MENU PRINCIPAL ", style="bold cyan")),
        box=ROUNDED,
        border_style=text_dim,
        width=70
    )

    console.print(Align.center(title))
    console.print()

    console.print(Align.center(
        Text("Use ↑↓ para navegar | Enter para selecionar", style=text_dim)
    ))
    console.print()

    # Captura da renderização do menu
    with console.capture() as capture:
        choice = ArrrowsService.arrow_menu(options)

    menu_rendered = capture.get()

    console.print(Align.center(menu_rendered))

    return choice

def dashboard_project(name: str, lang: str, path: Path, base: dict, path_color: str, git_repo_url: str | None = None):
    """
    Gera um painel com resumo e árvore de arquivos aninhada.
    """
    # --- Coluna da Esquerda: Informações ---
    info_text = Text()
    info_text.append("Nome do Projeto:\n", style=text_dim)
    info_text.append(f"{name}\n\n", style=theme_color)
    
    info_text.append("Linguagem:\n", style=text_dim)
    info_text.append(f"{lang.upper()}\n\n", style=accent_color)
    
    info_text.append("Caminho de Destino:\n", style=text_dim)
    info_text.append(f"{path}\n\n", style=path_color)
    
    # Adiciona informação do Git
    info_text.append("Git:\n", style=text_dim)
    if git_repo_url:
        info_text.append("Ativo\n", style=success_color)
        info_text.append("Repositório:\n", style=text_dim)
        info_text.append(f"{git_repo_url}\n", style=accent_color)
    else:
        info_text.append("Desativado\n", style=warning_color)

    # --- Coluna da Direita: Árvore de Arquivos ---
    tree = Tree(f"[bold {theme_color}]📁 {name}[/]", guide_style=text_dim)
    
    # Mapa para cache de pastas criadas (evita duplicar pastas no visual)
    folder_map = {} 

    for file_path in sorted(base.keys()):
        # Verifica se é um arquivo dentro de pasta (tem barra)
        if "/" in file_path:
            parts = file_path.split("/")
            filename = parts[-1]
            folders = parts[:-1] # Lista das pastas até o arquivo
            
            current_branch = tree
            accumulated_path = ""
            
            # Navega ou cria a estrutura de pastas
            for folder in folders:
                # Cria chave única para o mapa
                accumulated_path = f"{accumulated_path}/{folder}" if accumulated_path else folder
                
                if accumulated_path not in folder_map:
                    # Adiciona a pasta na árvore e guarda a referência
                    folder_map[accumulated_path] = current_branch.add(f"[bold {text_main}]📂 {folder}[/]")
                
                # Desce o nível
                current_branch = folder_map[accumulated_path]
            
            # Adiciona o arquivo na pasta final
            current_branch.add(f"[{text_dim}]📄 {filename}[/]")
            
        else:
            # Arquivo na raiz
            tree.add(f"[{text_dim}]📄 {file_path}[/]")

    # --- Montagem do Layout ---
    layout = Table.grid(expand=True, padding=(0, 2))
    layout.add_column(ratio=4) # Coluna Info
    layout.add_column(ratio=6) # Coluna Tree
    
    # Adiciona conteúdo lado a lado
    layout.add_row(info_text, tree)

    return Panel(
        layout,
        title=f"[bold {theme_color}]Confirmação do Projeto[/]",
        border_style=theme_color,
        box=ROUNDED,
        padding=(1, 2),
        width=80
    )


# =======================================================
# TELAS
# =======================================================
def config_screen():
    make_simple_header("Configurações")
    
    config_text = Text()
    config_text.append("⚙ Sistema de Configuração\n\n", style=f"bold {theme_color}")
    config_text.append("Em desenvolvimento...\n", style=text_dim)
    config_text.append("Recursos futuros:\n", style=text_main)
    config_text.append("• Temas personalizados\n", style=text_dim)
    config_text.append("• Diretórios padrão\n", style=text_dim)
    config_text.append("• Atalhos de teclado", style=text_dim)
    
    panel = Panel(
        Align.center(config_text),
        border_style=text_dim,
        box=ROUNDED,
        width=60,
        padding=(2, 4)
    )
    
    console.print(Align.center(panel))
    console.input(f"\n{' ' * 30}[{text_dim}]Enter para voltar...[/]")

def create_project_interactive():
    make_simple_header("Novo Projeto")
    
    # Nome
    console.print(Align.center(f"[{text_dim}]Nome do projeto[/]"))
    console.print()
    name = input(f"{' ' * 32}▸ ").strip()
    
    if not name:
        console.print()
        console.print(Align.center(f"[{warning_color}]✘ Nome inválido[/]"))
        time.sleep(1.5)
        return
    
    # Linguagem (mesma tela)
    console.print()
    console.print(Align.center(f"[{text_dim}]Linguagem (python/web/lua) [padrão: python][/]"))
    console.print()
    raw_type = input(f"{' ' * 32}▸ ").strip().lower() or "python"
    type_project = tool.type_to_extension(raw_type)
    
    # Path (mesma tela)
    console.print()
    default_path = config.DIRETORIO
    console.print(Align.center(f"[{text_dim}]Diretório padrão: {default_path}[/]"))
    console.print(Align.center(f"[dim](Enter para usar padrão)[/]"))
    console.print()
    raw_path = input(f"{' ' * 32}▸ ").strip()
    
    path = Path(raw_path) if raw_path else Config.dispatch_path(type_project)

    gitRepoLink = None
    if config.GitAvaliable:
        console.print()
        console.print(Align.center(f"[{text_dim}]Inicializar repositório Git?[/]"))
        console.print(Align.center(f"[dim](Deixe em branco para pular)[/]"))
        console.print()
        
        # Pergunta se quer usar Git
        use_git = input(f"{' ' * 32}▸ [Y/n]: ").strip().lower()
        
        if use_git in ['y', 'yes', '']:
            console.print()
            console.print(Align.center(f"[{text_dim}]URL do repositório remoto: [/]"))
            console.print(Align.center(f"[dim](Ex: https://github.com/user/repo.git)[/]"))
            console.print()
            gitRepoLink = input(f"{' ' * 32}▸ ").strip()
            
            if gitRepoLink:
                console.print()
                console.print(Align.center(f"[{success_color}]✓ Repositório configurado[/]"))
                time.sleep(1)
    
    # Criação
    try:
        tool.clear_screen()
        console.print()

        tempValidPath = None

        # Painel de verificação de diretório + infos do projeto
        if os.path.exists(path / name):
            console.print(Align.center(f"[{warning_color}]✘ Diretório já existe![/]"))
            time.sleep(3)
            return
        
        if not os.path.exists(path):
            tempValidPath = warning_color
        else:
            tempValidPath = success_color
            
        dir_panel = Panel(
            Align.center(Text.assemble(
            ("Nome: ", text_dim), (f"{name}\n", theme_color),
            ("Linguagem: ", text_dim), (f"{type_project.upper()}\n", accent_color),
            ("Diretório: ",  tempValidPath), (f"{path}\n", tempValidPath),
            ("Git: ", text_dim), 
            (f"{'Ativo' if gitRepoLink else 'Desativado'}\n", success_color if gitRepoLink else warning_color),
            (f"{gitRepoLink}" if gitRepoLink else "", accent_color if gitRepoLink else ""),
            )),
            title=f"[{theme_color}]Status[/]",
            border_style=theme_color,
            box=ROUNDED,
            padding=(1, 2),
            width=60
        )
        console.print(Align.center(dir_panel))
        console.print()

        base = ProjectManagerService.get_base_structure(type_project)

        # Painel de arquivos a serem criados
        files_text = Text()
        files_text.append("Arquivos a serem criados:\n", style=text_dim)

        project_dashboard = dashboard_project(
            name=name,
            lang=type_project,
            path=path,
            base=base,
            path_color=tempValidPath,
            git_repo_url=gitRepoLink
        )
        
        console.print(Align.center(project_dashboard))
        console.print()
        
        console.print()
        console.print(Align.center(Text.assemble(
            ("Confirmar criação? [", text_dim),
            ("Y", success_color),
            ("/", text_dim),
            ("N", warning_color),
            ("]", text_dim)
        )))
        console.print()
        
        confirm = input(f"{' ' * 38}> ").strip().lower()
        
        if confirm != "y":
            console.print()

            cancel_panel = Panel(
                Align.center(
                    Text.assemble(
                        ("✘ OPERAÇÃO CANCELADA\n", f"bold {warning_color}"),
                    )
                ),
                title=f"[bold {warning_color}]Cancelado[/]",
                subtitle=f"[{text_dim}]Voltando ao menu...[/]",
                border_style=warning_color,
                box=ROUNDED,
                padding=(1, 2),
                width=60,
            )

            console.print(Align.center(cancel_panel))

            console.print()
            time.sleep(1.5)
            return
        
        console.print()
        console.print(Align.center(f"[{success_color}]▸ Criando projeto...[/]"))
        with console.status("", spinner="dots"):
            ProjectManagerService.create_project(name=name, language=type_project, path=path, gitRepoLink=gitRepoLink)
            time.sleep(1)
        
        tool.clear_screen()
        console.print()
        success_panel = Panel(
            Align.center(Text.assemble(
                (f"✓ Projeto '{name}' criado com sucesso!\n\n", success_color),
                (f"📂 Abrir no {Config.BASECODEEDITOR}\n", accent_color),
                (f"{Config.get_editor_link(Config.BASECODEEDITOR,path)}, text_dim")
            )),
            
            title=f"[{theme_color}]Sucesso[/]",
            border_style=theme_color,
            box=ROUNDED,
            padding=(1, 2),
            width=60
        )
        console.print(Align.center(success_panel))
        console.print()
        console.print(Align.center(f"[{text_dim}]Pressione Enter para continuar...[/]"))
        input(f"{' ' * 45}")
        
    except Exception as e:
        console.print()
        console.print(Align.center(f"[{warning_color}]✘ Erro: {e}[/]"))
        input(f"\n{' ' * 30}[{text_dim}]Enter para voltar...[/]")

# =======================================================
# LOOP PRINCIPAL
# =======================================================
def Start():
    while True:
        draw_main_dashboard()
        
        options = [
            "  Novo Projeto     ",
            "  Módulos          ",
            "  Configurações    ",
            "  Sair             "
        ]
        
        # Menu com bordas arredondadas integrado
        choice = ArrrowsService.arrow_menu(options)
        
        if choice == 0:
            create_project_interactive()
        elif choice == 1:
            if config.Debug:
                make_simple_header("Diagnóstico")
                console.print(f"[{theme_color}]Verificando dependências...[/]\n")
                asyncio.run(tool.verify_modules())
                console.input(f"\n{' ' * 30}[{text_dim}]Enter para voltar...[/]")
            else:
                console.print(Align.center(f"[{warning_color}]Debug desativado[/]"))
                time.sleep(1.5)
        elif choice == 2:
            config_screen()
        elif choice == 3:
            tool.clear_screen()
            console.print(Align.center(Panel(
                f"[{theme_color}]Encerrando...[/]",
                box=ROUNDED,
                border_style=text_dim,
                width=40
            )))
            time.sleep(1)
            break

# =======================================================
# MAIN
# =======================================================
async def main():
    try:
        console.clear()
        
        # Splash screen
        splash_logo = Text()
        splash_logo.append("\n", style=f"bold {theme_color}")
        splash_logo.append("PROJECT SETUP 3.0\n\n", style=f"bold {text_main}")
        splash_logo.append("Loading...", style=text_dim)
        
        console.print(Align.center(Panel(
            Align.center(splash_logo),
            box=ROUNDED,
            border_style=theme_color,
            width=35,
            padding=(1, 2)
        ), vertical="middle"))
        
        cfg = Config()
        await tool.add_path_modules(cfg)
        
        if cfg.Debug:
            await tool.verify_modules()
        
        await asyncio.sleep(1.5)
        Start()    
    except Exception as e:
        console.print(f"[bold red]ERRO CRÍTICO[/]: {e}")
        sys.exit(1)

def run():
    """Entry point síncrono para console_scripts"""
    asyncio.run(main())

if __name__ == "__main__":
    run()