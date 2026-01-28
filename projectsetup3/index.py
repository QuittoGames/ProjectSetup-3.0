from pathlib import Path
import asyncio
import time
import sys
import os
import json

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
from projectsetup3.Services.InstallService import InstallService

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
# DASHBOARD DO PROJETO
# =======================================================
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
# SISTEMA DE CONFIGURAÇÃO
# =======================================================
def load_user_config():
    """Carrega configurações personalizadas do usuário"""
    config_file = config.appdata / "Config" / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_config(user_config):
    """Salva configurações personalizadas do usuário usando Config.saveConfig"""
    # Atualiza a instância global do config
    if 'BASECODEEDITOR' in user_config:
        Config.BASECODEEDITOR = user_config['BASECODEEDITOR']
    if 'GitAvaliable' in user_config:
        Config.GitAvaliable = user_config['GitAvaliable']
    if 'HistoryAvaliable' in user_config:
        Config.HistoryAvaliable = user_config['HistoryAvaliable']
    if 'READMEAvaliable' in user_config:
        Config.READMEAvaliable = user_config['READMEAvaliable']
    if 'DIRETORIO' in user_config:
        Config.DIRETORIO = Path(user_config['DIRETORIO'])
    if 'DIRETORIO_WEB' in user_config:
        Config.DIRETORIO_WEB = Path(user_config['DIRETORIO_WEB'])
    if 'DIRETORIO_CPP' in user_config:
        Config.DIRETORIO_CPP = Path(user_config['DIRETORIO_CPP'])
    
    # Salva usando o método do backend
    Config.saveConfig(config)
    
    # Também salva cores no user_config.json separado
    colors_config = {k: v for k, v in user_config.items() if 'color' in k or k in ['text_dim', 'text_main']}
    if colors_config:
        colors_file = config.appdata / "user_config.json"
        config.appdata.mkdir(parents=True, exist_ok=True)
        with open(colors_file, 'w', encoding='utf-8') as f:
            json.dump(colors_config, f, indent=2, ensure_ascii=False)

def save_all_config():
    """Salva todas as configurações atuais"""
    make_simple_header("Salvar Configurações")
    
    # Preview das configurações
    preview_table = Table.grid(padding=(0, 3))
    preview_table.add_column(style=text_dim, justify="right", width=20)
    preview_table.add_column(style="bold", width=30)
    
    # Seção: Editor
    preview_table.add_row("", "")
    preview_table.add_row("💻 EDITOR", "")
    preview_table.add_row("  Padrão:", Text(Config.BASECODEEDITOR.upper(), style=accent_color))
    
    # Seção: Features
    preview_table.add_row("", "")
    preview_table.add_row("⚡ RECURSOS", "")
    preview_table.add_row("  Git:", Text("✓ ATIVO" if Config.GitAvaliable else "✗ DESATIVADO", 
                                       style=success_color if Config.GitAvaliable else warning_color))
    preview_table.add_row("  README IA:", Text("✓ ATIVO" if Config.READMEAvaliable else "✗ DESATIVADO", 
                                               style=success_color if Config.READMEAvaliable else warning_color))
    preview_table.add_row("  Histórico:", Text("✓ ATIVO" if Config.HistoryAvaliable else "✗ DESATIVADO", 
                                                style=success_color if Config.HistoryAvaliable else warning_color))
    
    # Seção: Diretórios
    preview_table.add_row("", "")
    preview_table.add_row("📁 DIRETÓRIOS", "")
    preview_table.add_row("  Python:", Text(str(Config.DIRETORIO)[-30:], style=accent_color))
    preview_table.add_row("  Web:", Text(str(Config.DIRETORIO_WEB)[-30:], style=accent_color))
    preview_table.add_row("  C++:", Text(str(Config.DIRETORIO_CPP)[-30:], style=accent_color))
    
    # Seção: Tema
    preview_table.add_row("", "")
    preview_table.add_row("🎨 TEMA", "")
    preview_table.add_row("  Principal:", Text(f"● {theme_color}", style=theme_color))
    preview_table.add_row("  Destaque:", Text(f"● {accent_color}", style=accent_color))
    preview_table.add_row("  Sucesso:", Text(f"● {success_color}", style=success_color))
    
    preview_panel = Panel(
        preview_table,
        title=f"[bold {theme_color}]📋 RESUMO DAS CONFIGURAÇÕES[/]",
        subtitle=f"[{text_dim}]Preview do que será salvo[/]",
        border_style=theme_color,
        box=ROUNDED,
        width=80,
        padding=(1, 2)
    )
    
    console.print(Align.center(preview_panel))
    console.print()
    
    # Confirmação estilizada
    confirm_text = Text()
    confirm_text.append("💾 ", style=f"bold {theme_color}")
    confirm_text.append("Salvar estas configurações?", style=f"bold {text_main}")
    
    confirm_panel = Panel(
        Align.center(confirm_text),
        border_style=accent_color,
        box=ROUNDED,
        width=50,
        padding=(0, 2)
    )
    
    console.print(Align.center(confirm_panel))
    console.print()
    
    options = [
        f"  ✓ Sim, salvar agora   ",
        f"  ✗ Cancelar            "
    ]
    
    choice = ArrrowsService.arrow_menu(options)
    
    if choice == 0:
        console.print()
        
        # Animação de salvamento
        with console.status(f"[{theme_color}]💾 Salvando configurações...[/]", spinner="dots"):
            try:
                # Salva usando o método do backend
                success = Config.saveConfig(config)
                
                # Salva cores separadamente
                colors_config = {
                    'theme_color': theme_color,
                    'accent_color': accent_color,
                    'success_color': success_color,
                    'warning_color': warning_color,
                    'text_dim': text_dim,
                    'text_main': text_main
                }
                colors_file = config.appdata / "user_config.json"
                config.appdata.mkdir(parents=True, exist_ok=True)
                with open(colors_file, 'w', encoding='utf-8') as f:
                    json.dump(colors_config, f, indent=2, ensure_ascii=False)
                
                time.sleep(1)  # Delay visual
                
                # Mensagem de sucesso estilizada
                console.print()
                
                success_table = Table.grid(padding=(0, 1))
                success_table.add_column(justify="center")
                
                success_table.add_row(Text("✓", style=f"bold {success_color} blink", justify="center"))
                success_table.add_row("")
                success_table.add_row(Text("CONFIGURAÇÕES SALVAS!", style=f"bold {success_color}"))
                success_table.add_row("")
                success_table.add_row(Text("Suas preferências foram armazenadas", style=text_dim))
                success_table.add_row(Text("e serão carregadas automaticamente", style=text_dim))
                success_table.add_row("")
                success_table.add_row(Text("📁 Localização:", style=text_dim))
                success_table.add_row(Text(str(config.appdata / "Config" / "config.json"), style=accent_color))
                
                success_panel = Panel(
                    success_table,
                    border_style=success_color,
                    box=HEAVY,
                    width=70,
                    padding=(1, 2)
                )
                
                console.print(Align.center(success_panel))
                
            except Exception as e:
                console.print()
                
                error_text = Text()
                error_text.append("✗ ERRO AO SALVAR\n\n", style=f"bold {warning_color}")
                error_text.append(f"Detalhes: {str(e)}\n\n", style=text_dim)
                error_text.append("Tente novamente ou verifique as permissões", style=text_dim)
                
                error_panel = Panel(
                    Align.center(error_text),
                    border_style=warning_color,
                    box=ROUNDED,
                    width=60,
                    padding=(1, 2)
                )
                
                console.print(Align.center(error_panel))
    else:
        console.print()
        cancel_text = Text("✗ Salvamento cancelado", style=warning_color)
        console.print(Align.center(cancel_text))
    
    console.print()
    console.print(Align.center(f"[{text_dim}]Enter para voltar...[/]"))
    input(f"{' ' * 40}")

def apply_user_config():
    """Aplica configurações salvas do usuário"""
    global theme_color, accent_color, success_color, warning_color, text_dim, text_main
    
    # Carrega configurações do backend (Config/config.json)
    backend_config = Config.getCofig()
    
    # Aplica configurações do backend
    if backend_config:
        if 'BASECODEEDITOR' in backend_config:
            Config.BASECODEEDITOR = backend_config['BASECODEEDITOR']
        if 'GitAvaliable' in backend_config:
            Config.GitAvaliable = backend_config['GitAvaliable']
        if 'HistoryAvaliable' in backend_config:
            Config.HistoryAvaliable = backend_config['HistoryAvaliable']
        if 'READMEAvaliable' in backend_config:
            Config.READMEAvaliable = backend_config['READMEAvaliable']
        if 'DIRETORIO' in backend_config:
            Config.DIRETORIO = Path(backend_config['DIRETORIO'])
        if 'DIRETORIO_WEB' in backend_config:
            Config.DIRETORIO_WEB = Path(backend_config['DIRETORIO_WEB'])
        if 'DIRETORIO_CPP' in backend_config:
            Config.DIRETORIO_CPP = Path(backend_config['DIRETORIO_CPP'])
    
    # Carrega cores do user_config.json separado (apenas cores)
    colors_file = config.appdata / "user_config.json"
    if colors_file.exists():
        try:
            with open(colors_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                
            # Aplica apenas cores
            if 'theme_color' in user_config:
                theme_color = user_config['theme_color']
            if 'accent_color' in user_config:
                accent_color = user_config['accent_color']
            if 'success_color' in user_config:
                success_color = user_config['success_color']
            if 'warning_color' in user_config:
                warning_color = user_config['warning_color']
            if 'text_dim' in user_config:
                text_dim = user_config['text_dim']
            if 'text_main' in user_config:
                text_main = user_config['text_main']
        except:
            pass  # Se falhar, mantém cores padrão

# =======================================================
# TELAS
# =======================================================
def config_screen():
    """Menu de configurações interativo"""
    while True:
        make_simple_header("Configurações")
        
        user_config = load_user_config()
        
        # Mostra valores atuais
        config_display = Table.grid(padding=(0, 2))
        config_display.add_column(style=text_dim, justify="right")
        config_display.add_column(style=accent_color)
        
        config_display.add_row("Editor Padrão:", Config.BASECODEEDITOR)
        config_display.add_row("Git:", "✓ Ativo" if Config.GitAvaliable else "✗ Desativado")
        config_display.add_row("README IA:", "✓ Ativo" if Config.READMEAvaliable else "✗ Desativado")
        config_display.add_row("Histórico:", "✓ Ativo" if Config.HistoryAvaliable else "✗ Desativado")
        config_display.add_row("", "")
        config_display.add_row("Dir. Python:", str(Config.DIRETORIO)[:50] + "..." if len(str(Config.DIRETORIO)) > 50 else str(Config.DIRETORIO))
        config_display.add_row("Dir. Web:", str(Config.DIRETORIO_WEB)[:50] + "..." if len(str(Config.DIRETORIO_WEB)) > 50 else str(Config.DIRETORIO_WEB))
        config_display.add_row("Dir. C++:", str(Config.DIRETORIO_CPP)[:50] + "..." if len(str(Config.DIRETORIO_CPP)) > 50 else str(Config.DIRETORIO_CPP))
        config_display.add_row("", "")
        config_display.add_row("Tema Principal:", theme_color)
        config_display.add_row("Cor de Destaque:", accent_color)
        config_display.add_row("Cor de Sucesso:", success_color)
        
        panel = Panel(
            config_display,
            title=f"[bold {theme_color}]Configurações Atuais[/]",
            border_style=theme_color,
            box=ROUNDED,
            width=80,
            padding=(1, 2)
        )
        
        console.print(Align.center(panel))
        console.print()
        
        options = [
            "  Editor Padrão        ",
            "  Git                  ",
            "  README IA            ",
            "  Histórico            ",
            "  Diretórios           ",
            "  Cores do Tema        ",
            "  💾 Salvar Tudo        ",
            "  Restaurar Padrões    ",
            "  ← Voltar             "
        ]
        
        choice = ArrrowsService.arrow_menu(options)
        
        if choice == 0:  # Editor
            edit_editor_config()
        elif choice == 1:  # Git
            toggle_git_config()
        elif choice == 2:  # README IA
            toggle_readme_config()
        elif choice == 3:  # Histórico
            toggle_history_config()
        elif choice == 4:  # Diretórios
            edit_directories_config()
        elif choice == 5:  # Cores
            edit_colors_config()
        elif choice == 6:  # Salvar Tudo
            save_all_config()
        elif choice == 7:  # Restaurar
            restore_default_config()
        elif choice == 8:  # Voltar
            break

def edit_editor_config():
    """Edita o editor padrão"""
    make_simple_header("Editor Padrão")
    
    editors = [
        ("VSCode", "vscode"),
        ("Cursor", "cursor"),
        ("VSCodium", "vscodium"),
        ("Sublime Text", "sublime"),
        ("PyCharm", "pycharm"),
        ("IntelliJ IDEA", "idea"),
        ("WebStorm", "webstorm")
    ]
    
    editor_text = Text()
    editor_text.append("Selecione seu editor preferido:\n\n", style=f"bold {theme_color}")
    editor_text.append(f"Atual: {Config.BASECODEEDITOR}\n", style=accent_color)
    
    console.print(Align.center(editor_text))
    console.print()
    
    options = [f"  {name:<20}" for name, _ in editors] + ["  ← Cancelar          "]
    choice = ArrrowsService.arrow_menu(options)
    
    if choice < len(editors):
        selected_editor = editors[choice][1]
        Config.BASECODEEDITOR = selected_editor
        
        user_config = load_user_config()
        user_config['BASECODEEDITOR'] = selected_editor
        save_user_config(user_config)
        
        console.print()
        console.print(Align.center(f"[{success_color}]✓ Editor alterado para: {selected_editor}[/]"))
        time.sleep(1.5)

def toggle_git_config():
    """Submenu visual para configuração do Git"""
    while True:
        make_simple_header("Git Configuration")
        
        # Status atual
        status_text = Text()
        status_text.append("📦 Controle de Versão Git\n\n", style=f"bold {theme_color}")
        status_text.append("Status: ", style=text_dim)
        
        if Config.GitAvaliable:
            status_text.append("✓ ATIVO\n\n", style=success_color)
            status_text.append("Recursos habilitados:\n", style=text_main)
            status_text.append("  • Inicialização automática de repositório\n", style=accent_color)
            status_text.append("  • Configuração de remote URL\n", style=accent_color)
            status_text.append("  • Commit inicial do projeto\n", style=accent_color)
            status_text.append("  • Criação de .gitignore\n\n", style=accent_color)
        else:
            status_text.append("✗ DESATIVADO\n\n", style=warning_color)
            status_text.append("Projetos serão criados sem Git\n", style=text_dim)
            status_text.append("Você pode inicializar manualmente depois\n\n", style=text_dim)
        
        status_text.append("💡 Exemplo de uso:\n", style=theme_color)
        status_text.append("  Ao criar projeto 'MeuApp':\n", style=text_dim)
        if Config.GitAvaliable:
            status_text.append("  ✓ git init\n", style=success_color)
            status_text.append("  ✓ git remote add origin <url>\n", style=success_color)
            status_text.append("  ✓ git add .\n", style=success_color)
            status_text.append("  ✓ git commit -m 'Initial commit'", style=success_color)
        else:
            status_text.append("  ✗ Sem inicialização Git", style=warning_color)
        
        panel = Panel(
            Align.center(status_text),
            border_style=success_color if Config.GitAvaliable else warning_color,
            box=ROUNDED,
            width=70,
            padding=(1, 2)
        )
        
        console.print(Align.center(panel))
        console.print()
        
        options = [
            f"  {'✓' if Config.GitAvaliable else '✗'} {'Desativar' if Config.GitAvaliable else 'Ativar'} Git        ",
            "  ← Voltar             "
        ]
        
        choice = ArrrowsService.arrow_menu(options)
        
        if choice == 0:
            Config.GitAvaliable = not Config.GitAvaliable
            user_config = load_user_config()
            user_config['GitAvaliable'] = Config.GitAvaliable
            save_user_config(user_config)
            
            status = "ativado" if Config.GitAvaliable else "desativado"
            color = success_color if Config.GitAvaliable else warning_color
            console.print()
            console.print(Align.center(f"[{color}]✓ Git {status}![/]"))
            time.sleep(1)
        elif choice == 1:
            break

def toggle_readme_config():
    """Submenu visual para configuração do README IA"""
    while True:
        make_simple_header("README IA Configuration")
        
        # Status atual
        status_text = Text()
        status_text.append("🤖 Geração Inteligente de README\n\n", style=f"bold {theme_color}")
        status_text.append("Status: ", style=text_dim)
        
        if Config.READMEAvaliable:
            status_text.append("✓ ATIVO\n\n", style=success_color)
            status_text.append("Recursos habilitados:\n", style=text_main)
            status_text.append("  • Geração automática de README.md\n", style=accent_color)
            status_text.append("  • Análise de descrição do projeto\n", style=accent_color)
            status_text.append("  • Seções personalizadas\n", style=accent_color)
            status_text.append("  • Badges e formatação Markdown\n\n", style=accent_color)
            status_text.append("🔋 Powered by: Gemini 2.5 Flash\n\n", style=text_dim)
        else:
            status_text.append("✗ DESATIVADO\n\n", style=warning_color)
            status_text.append("README.md não será gerado automaticamente\n", style=text_dim)
            status_text.append("Você pode criar manualmente depois\n\n", style=text_dim)
        
        status_text.append("💡 Exemplo de uso:\n", style=theme_color)
        status_text.append("  Descrição: ", style=text_dim)
        status_text.append("'Sistema de blog com Django'\n", style=accent_color)
        if Config.READMEAvaliable:
            status_text.append("  ↓\n", style=text_dim)
            status_text.append("  README.md gerado com:\n", style=text_dim)
            status_text.append("  • Descrição do projeto\n", style=success_color)
            status_text.append("  • Tecnologias utilizadas\n", style=success_color)
            status_text.append("  • Instruções de instalação\n", style=success_color)
            status_text.append("  • Como usar\n", style=success_color)
            status_text.append("  • Estrutura do projeto", style=success_color)
        else:
            status_text.append("  ✗ Sem geração automática", style=warning_color)
        
        panel = Panel(
            Align.center(status_text),
            border_style=success_color if Config.READMEAvaliable else warning_color,
            box=ROUNDED,
            width=70,
            padding=(1, 2)
        )
        
        console.print(Align.center(panel))
        console.print()
        
        options = [
            f"  {'✓' if Config.READMEAvaliable else '✗'} {'Desativar' if Config.READMEAvaliable else 'Ativar'} README IA  ",
            "  ← Voltar             "
        ]
        
        choice = ArrrowsService.arrow_menu(options)
        
        if choice == 0:
            Config.READMEAvaliable = not Config.READMEAvaliable
            user_config = load_user_config()
            user_config['READMEAvaliable'] = Config.READMEAvaliable
            save_user_config(user_config)
            
            status = "ativado" if Config.READMEAvaliable else "desativado"
            color = success_color if Config.READMEAvaliable else warning_color
            console.print()
            console.print(Align.center(f"[{color}]✓ README IA {status}![/]"))
            time.sleep(1)
        elif choice == 1:
            break

def view_history():
    """Visualiza o histórico de projetos criados"""
    from projectsetup3.Services.HistoryService import HistoryService
    
    make_simple_header("Histórico de Projetos")
    
    history = HistoryService.getHistory()
    projects = history.get("projects", [])
    
    if not projects:
        empty_text = Text()
        empty_text.append("📭 Nenhum projeto no histórico\n\n", style=f"bold {warning_color}")
        empty_text.append("Crie seu primeiro projeto para começar!", style=text_dim)
        
        panel = Panel(
            Align.center(empty_text),
            border_style=text_dim,
            box=ROUNDED,
            width=60,
            padding=(2, 4)
        )
        
        console.print(Align.center(panel))
        console.print()
        console.print(Align.center(f"[{text_dim}]Enter para voltar...[/]"))
        input(f"{' ' * 40}")
        return
    
    # Cria tabela de histórico
    table = Table(
        title=f"[bold {theme_color}]Projetos Criados: {len(projects)}[/]",
        show_header=True,
        header_style=f"bold {theme_color}",
        border_style=accent_color,
        box=ROUNDED,
        expand=False,
        padding=(0, 1)
    )
    
    table.add_column("#", style=text_dim, justify="right", width=4)
    table.add_column("Nome", style=f"bold {accent_color}", width=20)
    table.add_column("Linguagem", style=success_color, width=12)
    table.add_column("Data", style=text_dim, width=18)
    table.add_column("Caminho", style=text_main, width=40)
    
    # Mostra últimos 15 projetos
    recent_projects = projects[-15:] if len(projects) > 15 else projects
    
    for idx, project in enumerate(reversed(recent_projects), 1):
        name = project.get("name", "Desconhecido")
        lang = project.get("language", "N/A").upper()
        date = project.get("created_at", "N/A")
        path = project.get("path", "N/A")
        
        # Trunca caminho se muito longo
        if len(path) > 40:
            path = "..." + path[-37:]
        
        table.add_row(str(idx), name, lang, date, path)
    
    console.print(Align.center(table))
    console.print()
    
    if len(projects) > 15:
        info_text = Text()
        info_text.append(f"Mostrando últimos 15 de {len(projects)} projetos\n", style=text_dim)
        info_text.append(f"Arquivo: {Config.baseDiretoryHistory / 'history.json'}", style=text_dim)
        console.print(Align.center(info_text))
        console.print()
    
    console.print(Align.center(f"[{text_dim}]Enter para voltar...[/]"))
    input(f"{' ' * 40}")

def toggle_history_config():
    """Submenu visual para configuração do Histórico"""
    while True:
        make_simple_header("History Configuration")
        
        # Status atual
        status_text = Text()
        status_text.append("📚 Histórico de Projetos\n\n", style=f"bold {theme_color}")
        status_text.append("Status: ", style=text_dim)
        
        if Config.HistoryAvaliable:
            status_text.append("✓ ATIVO\n\n", style=success_color)
            status_text.append("Recursos habilitados:\n", style=text_main)
            status_text.append("  • Registro automático de projetos\n", style=accent_color)
            status_text.append("  • Rastreamento de data/hora\n", style=accent_color)
            status_text.append("  • Armazenamento de metadados\n", style=accent_color)
            status_text.append("  • Visualização de histórico\n\n", style=accent_color)
            status_text.append(f"📁 Localização: {Config.baseDiretoryHistory}\n\n", style=text_dim)
        else:
            status_text.append("✗ DESATIVADO\n\n", style=warning_color)
            status_text.append("Projetos não serão registrados\n", style=text_dim)
            status_text.append("Histórico não será mantido\n\n", style=text_dim)
        
        status_text.append("💡 Informações salvas:\n", style=theme_color)
        if Config.HistoryAvaliable:
            status_text.append("  • Nome do projeto\n", style=success_color)
            status_text.append("  • Linguagem/tipo\n", style=success_color)
            status_text.append("  • Caminho completo\n", style=success_color)
            status_text.append("  • Data de criação\n", style=success_color)
            status_text.append("  • Configurações usadas", style=success_color)
        else:
            status_text.append("  ✗ Sem registro de histórico", style=warning_color)
        
        panel = Panel(
            Align.center(status_text),
            border_style=success_color if Config.HistoryAvaliable else warning_color,
            box=ROUNDED,
            width=70,
            padding=(1, 2)
        )
        
        console.print(Align.center(panel))
        console.print()
        
        options = [
            f"  {'✓' if Config.HistoryAvaliable else '✗'} {'Desativar' if Config.HistoryAvaliable else 'Ativar'} Histórico  ",
            "  📖 Ver Histórico       ",
            "  ← Voltar             "
        ]
        
        choice = ArrrowsService.arrow_menu(options)
        
        if choice == 0:
            Config.HistoryAvaliable = not Config.HistoryAvaliable
            user_config = load_user_config()
            user_config['HistoryAvaliable'] = Config.HistoryAvaliable
            save_user_config(user_config)
            
            status = "ativado" if Config.HistoryAvaliable else "desativado"
            color = success_color if Config.HistoryAvaliable else warning_color
            console.print()
            console.print(Align.center(f"[{color}]✓ Histórico {status}![/]"))
            time.sleep(1)
        elif choice == 1:
            view_history()
        elif choice == 2:
            break

def edit_directories_config():
    """Edita os diretórios padrão"""
    while True:
        make_simple_header("Diretórios Padrão")
        
        dir_display = Table.grid(padding=(0, 2))
        dir_display.add_column(style=text_dim, justify="right")
        dir_display.add_column(style=accent_color)
        
        dir_display.add_row("Python:", str(Config.DIRETORIO))
        dir_display.add_row("Web:", str(Config.DIRETORIO_WEB))
        dir_display.add_row("C++:", str(Config.DIRETORIO_CPP))
        
        panel = Panel(
            dir_display,
            title=f"[bold {theme_color}]Diretórios Atuais[/]",
            border_style=theme_color,
            box=ROUNDED,
            width=80,
            padding=(1, 2)
        )
        
        console.print(Align.center(panel))
        console.print()
        
        options = [
            "  Dir. Python          ",
            "  Dir. Web             ",
            "  Dir. C++             ",
            "  ← Voltar             "
        ]
        
        choice = ArrrowsService.arrow_menu(options)
        
        if choice == 0:  # Python
            edit_single_directory('DIRETORIO', 'Python')
        elif choice == 1:  # Web
            edit_single_directory('DIRETORIO_WEB', 'Web')
        elif choice == 2:  # C++
            edit_single_directory('DIRETORIO_CPP', 'C++')
        elif choice == 3:  # Voltar
            break

def edit_single_directory(config_key, display_name):
    """Edita um diretório específico"""
    make_simple_header(f"Diretório {display_name}")
    
    current = getattr(Config, config_key)
    
    dir_text = Text()
    dir_text.append(f"Editar diretório padrão para {display_name}\n\n", style=f"bold {theme_color}")
    dir_text.append(f"Atual: {current}\n\n", style=accent_color)
    dir_text.append("Digite o novo caminho (ou Enter para cancelar):", style=text_dim)
    
    console.print(Align.center(dir_text))
    console.print()
    
    new_path = input(f"{' ' * 20}▸ ").strip()
    
    if new_path:
        new_path_obj = Path(new_path)
        setattr(Config, config_key, new_path_obj)
        
        user_config = load_user_config()
        user_config[config_key] = str(new_path_obj)
        save_user_config(user_config)
        
        console.print()
        console.print(Align.center(f"[{success_color}]✓ Diretório {display_name} atualizado[/]"))
        time.sleep(1.5)

def edit_colors_config():
    """Edita as cores do tema"""
    while True:
        make_simple_header("Cores do Tema")
        
        color_display = Table.grid(padding=(0, 2))
        color_display.add_column(style=text_dim, justify="right")
        color_display.add_column()
        
        color_display.add_row("Tema Principal:", Text(f"● {theme_color}", style=theme_color))
        color_display.add_row("Destaque:", Text(f"● {accent_color}", style=accent_color))
        color_display.add_row("Sucesso:", Text(f"● {success_color}", style=success_color))
        color_display.add_row("Aviso:", Text(f"● {warning_color}", style=warning_color))
        color_display.add_row("Texto Dim:", Text(f"● {text_dim}", style=text_dim))
        color_display.add_row("Texto Principal:", Text(f"● {text_main}", style=text_main))
        
        panel = Panel(
            color_display,
            title=f"[bold {theme_color}]Cores Atuais[/]",
            border_style=theme_color,
            box=ROUNDED,
            width=60,
            padding=(1, 2)
        )
        
        console.print(Align.center(panel))
        console.print()
        
        # Informação sobre cores disponíveis com exemplos visuais
        info_text = Text()
        info_text.append("🎨 Cores disponíveis:\n\n", style=f"bold {theme_color}")
        
        # Cores primárias
        info_text.append("Primárias:\n", style=text_dim)
        info_text.append("  ● bright_blue  ", style="bright_blue")
        info_text.append("● blue  ", style="blue")
        info_text.append("● cyan\n", style="cyan")
        
        # Cores de status
        info_text.append("Status:\n", style=text_dim)
        info_text.append("  ● green  ", style="green")
        info_text.append("● yellow  ", style="yellow")
        info_text.append("● red\n", style="red")
        
        # Cores neutras
        info_text.append("Neutras:\n", style=text_dim)
        info_text.append("  ● white  ", style="white")
        info_text.append("● bright_black  ", style="bright_black")
        info_text.append("● black\n", style="black")
        
        # Outras
        info_text.append("Outras:\n", style=text_dim)
        info_text.append("  ● magenta  ", style="magenta")
        info_text.append("● bright_magenta  ", style="bright_magenta")
        info_text.append("● bright_cyan\n\n", style="bright_cyan")
        
        info_text.append("💡 Exemplo: ", style=text_dim)
        info_text.append("'bright_blue' para azul vibrante", style="bright_blue")
        
        info_panel = Panel(
            Align.center(info_text),
            border_style=accent_color,
            box=ROUNDED,
            width=70,
            padding=(1, 2)
        )
        
        console.print(Align.center(info_panel))
        console.print()
        
        options = [
            "  Tema Principal       ",
            "  Destaque             ",
            "  Sucesso              ",
            "  Aviso                ",
            "  Texto Dim            ",
            "  Texto Principal      ",
            "  ← Voltar             "
        ]
        
        choice = ArrrowsService.arrow_menu(options)
        
        if choice == 0:
            edit_single_color('theme_color', 'Tema Principal')
        elif choice == 1:
            edit_single_color('accent_color', 'Destaque')
        elif choice == 2:
            edit_single_color('success_color', 'Sucesso')
        elif choice == 3:
            edit_single_color('warning_color', 'Aviso')
        elif choice == 4:
            edit_single_color('text_dim', 'Texto Dim')
        elif choice == 5:
            edit_single_color('text_main', 'Texto Principal')
        elif choice == 6:
            break

def edit_single_color(color_key, display_name):
    """Edita uma cor específica"""
    global theme_color, accent_color, success_color, warning_color, text_dim, text_main
    
    make_simple_header(f"Cor: {display_name}")
    
    current = globals()[color_key]
    
    color_text = Text()
    color_text.append(f"Editar cor: {display_name}\n\n", style=f"bold {theme_color}")
    color_text.append("Atual: ", style=text_dim)
    color_text.append(f"● {current}\n\n", style=current)
    color_text.append("Digite a nova cor (ou Enter para cancelar):", style=text_dim)
    
    console.print(Align.center(color_text))
    console.print()
    
    new_color = input(f"{' ' * 30}▸ ").strip()
    
    if new_color:
        globals()[color_key] = new_color
        
        user_config = load_user_config()
        user_config[color_key] = new_color
        save_user_config(user_config)
        
        console.print()
        console.print(Align.center(Text.assemble(
            ("✓ Cor ", success_color),
            (display_name, accent_color),
            (" atualizada para: ", success_color),
            (f"● {new_color}", new_color)
        )))
        time.sleep(1.5)

def restore_default_config():
    """Restaura configurações padrão"""
    make_simple_header("Restaurar Padrões")
    
    warning_text = Text()
    warning_text.append("⚠ ATENÇÃO\n\n", style=f"bold {warning_color}")
    warning_text.append("Isso irá restaurar todas as configurações\n", style=text_dim)
    warning_text.append("para os valores padrão do sistema.\n\n", style=text_dim)
    warning_text.append("Deseja continuar?", style=text_main)
    
    panel = Panel(
        Align.center(warning_text),
        border_style=warning_color,
        box=ROUNDED,
        width=60,
        padding=(1, 2)
    )
    
    console.print(Align.center(panel))
    console.print()
    
    options = [
        "  Sim, restaurar       ",
        "  Não, cancelar        "
    ]
    
    choice = ArrrowsService.arrow_menu(options)
    
    if choice == 0:
        # Remove os arquivos de configuração
        config_file = config.appdata / "Config" / "config.json"
        colors_file = config.appdata / "user_config.json"
        
        if config_file.exists():
            config_file.unlink()
        if colors_file.exists():
            colors_file.unlink()
        
        console.print()
        console.print(Align.center(f"[{success_color}]✓ Configurações restauradas![/]"))
        console.print(Align.center(f"[{text_dim}]Reinicie o programa para aplicar[/]"))
        time.sleep(2)

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
    display_lang = raw_type.upper()
    
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
    
    # Coleta descrição do projeto se READMEAvaliable estiver ativo
    projectDescription = None
    if config.READMEAvaliable:
        console.print()
        
        # Painel de introdução README
        readme_intro = Text()
        readme_intro.append("📝 Geração de README.md\n\n", style=f"bold {theme_color}")
        readme_intro.append("Descreva o objetivo do seu projeto em detalhes.\n", style=text_dim)
        readme_intro.append("Isso será usado pela IA para gerar um README.md profissional.\n\n", style=text_dim)
        readme_intro.append("💡 Dicas:\n", style=accent_color)
        readme_intro.append("• Múltiplas linhas: pressione Enter para nova linha\n", style=text_dim)
        readme_intro.append("• Finalize: deixe uma linha em branco e pressione Enter\n", style=text_dim)
        readme_intro.append("• Pular: pressione Enter diretamente na primeira linha\n\n", style=text_dim)
        readme_intro.append("Exemplo:\n", style=accent_color)
        readme_intro.append("'Sistema de gerenciamento de projetos com CLI interativa.\n", style=text_dim)
        readme_intro.append("Suporta Python, JavaScript e outras linguagens.\n", style=text_dim)
        readme_intro.append("Inclui geração automática de README com IA.'", style=text_dim)
        
        readme_panel = Panel(
            Align.center(readme_intro),
            border_style=accent_color,
            box=ROUNDED,
            width=80,
            padding=(1, 2)
        )
        
        console.print(Align.center(readme_panel))
        console.print()
        
        # Captura multi-linha
        console.print(Align.center(f"[{accent_color}]Digite sua descrição (linha vazia para finalizar):[/]"))
        console.print()
        
        description_lines = []
        line_count = 0
        
        while True:
            prefix = f"{' ' * 28}│ " if line_count > 0 else f"{' ' * 28}▸ "
            line = input(prefix).strip()
            
            # Se primeira linha vazia, pula o README
            if line_count == 0 and not line:
                break
            
            # Se linha vazia após ter conteúdo, finaliza
            if not line and description_lines:
                break
            
            # Adiciona a linha se não for vazia
            if line:
                description_lines.append(line)
                line_count += 1
        
        # Junta todas as linhas em um único texto
        projectDescription = " ".join(description_lines) if description_lines else None
        
        if projectDescription:
            console.print()
            
            # Mostra preview da descrição
            preview_text = projectDescription[:100] + "..." if len(projectDescription) > 100 else projectDescription
            
            success_readme_text = Text()
            success_readme_text.append("✓ Descrição capturada!\n\n", style=success_color)
            success_readme_text.append("Preview:\n", style=text_dim)
            success_readme_text.append(f'"{preview_text}"\n\n', style=accent_color)
            success_readme_text.append(f"Total: {len(projectDescription)} caracteres, {len(description_lines)} linhas", style=text_dim)
            
            success_readme_panel = Panel(
                Align.center(success_readme_text),
                title=f"[{success_color}]README.md será gerado[/]",
                border_style=success_color,
                box=ROUNDED,
                width=80,
                padding=(1, 2)
            )
            
            console.print(Align.center(success_readme_panel))
            time.sleep(2)
        else:
            console.print()
            
            skip_readme_text = Text.assemble(
                ("✘ ", warning_color),
                ("README.md não será gerado", text_dim)
            )
            
            skip_readme_panel = Panel(
                Align.center(skip_readme_text),
                border_style=text_dim,
                box=ROUNDED,
                width=60,
                padding=(0, 2)
            )
            
            console.print(Align.center(skip_readme_panel))
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
            ("Linguagem: ", text_dim), (f"{display_lang}\n", accent_color),
            ("Diretório: ",  tempValidPath), (f"{path}\n", tempValidPath),
            ("Git: ", text_dim), 
            (f"{'Ativo' if gitRepoLink else 'Desativado'}\n", success_color if gitRepoLink else warning_color),
            (f"{gitRepoLink}\n" if gitRepoLink else "", accent_color if gitRepoLink else ""),
            ("README IA: ", text_dim),
            (f"{'Ativo' if projectDescription else 'Desativado'}", success_color if projectDescription else warning_color),
            )),
            title=f"[{theme_color}]Status[/]",
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
            lang=display_lang,
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
            ProjectManagerService.create_project(name=name, language=type_project, path=path, gitRepoLink=gitRepoLink, content=projectDescription)
            time.sleep(1)
        
        tool.clear_screen()
        console.print()

        editor_link = Config.get_editor_link(Config.BASECODEEDITOR, path / name)

        success_text = Text()
        success_text.append(f"✓ Projeto '{name}' criado com sucesso!\n\n", style=success_color)
        success_text.append(f"📂 Abrir no {Config.BASECODEEDITOR}\n", style=accent_color)
        link_text = Text(editor_link, style=text_dim)
        link_text.stylize(f"link {editor_link}")
        success_text.append_text(link_text)
        success_text.append("\n", style=text_dim)

        success_panel = Panel(
            Align.center(success_text),
            title=f"[{theme_color}]Sucesso[/]",
            border_style=theme_color,
            box=ROUNDED,

            
            padding=(1, 2),
            width=60,
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
async def Start():
    while True:
        draw_main_dashboard()
        
        # Instruções de navegação
        console.print(Align.center(
            Text("Use ↑↓ ou j/k para navegar | Enter para selecionar", style=text_dim)
        ))
        console.print()
        
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
                await tool.verify_modules()
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
        
        # Carrega configurações do usuário
        apply_user_config()
        
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
        
        # Aplica configurações salvas no início
        apply_user_config()
        
        await tool.add_path_modules(config)

        if not InstallService.isIstall(config):
            InstallService.install(config=config)
        
        if config.Debug:
            await tool.verify_modules()
        
        await asyncio.sleep(1.5)
        await Start()    
    except Exception as e:
        console.print(f"[bold red]ERRO CRÍTICO[/]: {e}")
        sys.exit(1)

def run():
    """Entry point síncrono para console_scripts"""
    asyncio.run(main())

if __name__ == "__main__":
    run()