import time
import sys
import os

from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from rich.align import Align


class ArrrowsService:

    @staticmethod
    def arrow_menu(options):
        console = Console()
        
        # ========================
        #   CAPTURA DE TECLA
        # ========================
        try:
            import msvcrt  # ---- WINDOWS ----

            def get_key():
                ch = msvcrt.getch()
                if ch in (b"\x00", b"\xe0"):  # Teclas especiais
                    ch2 = msvcrt.getch()
                    return ch + ch2
                return ch

        except ImportError:
            # ---- LINUX / MAC ----
            import termios
            import tty

            def get_key():
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                    
                    # Se for ESC, lê a sequência completa
                    if ch == '\x1b':
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            ch3 = sys.stdin.read(1)
                            return ch + ch2 + ch3
                        return ch + ch2
                    return ch
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)

        selected = 0

        # ========================
        #   UI DO MENU
        # ========================
        def render_menu():
            itens = []
            for i, op in enumerate(options):
                if i == selected:
                    itens.append(f"[bold cyan]›[/bold cyan] [white]{op}[/white]")
                else:
                    itens.append(f"  [dim]{op}[/dim]")

            panel = Panel(
                "\n".join(itens),
                border_style="cyan",
                width=60,
                padding=(1, 2),
                box=ROUNDED,
            )
            return Align.center(panel)

        # Oculta cursor para navegação fluida
        sys.stdout.write("\033[?25l")  # Oculta cursor
        sys.stdout.flush()
        
        # Renderiza menu inicial
        console.print(render_menu())
        # Calcula quantas linhas o menu ocupa
        menu_lines = len(options) + 4

        # ========================
        #   LOOP PRINCIPAL
        # ========================
        try:
            while True:
                key = get_key()
                needs_redraw = False
                
                # --------------------------
                # WINDOWS / WINDOWS NT (bytes)
                # --------------------------
                if isinstance(key, bytes):
                    # Seta ↑
                    if key in (b"\xe0H", b"\x00H"):
                        selected = (selected - 1) % len(options)
                        needs_redraw = True
                    # Seta ↓
                    elif key in (b"\xe0P", b"\x00P"):
                        selected = (selected + 1) % len(options)
                        needs_redraw = True
                    # ENTER
                    elif key == b"\r":
                        # Limpa menu e mostra cursor
                        for _ in range(menu_lines):
                            sys.stdout.write("\033[F\033[K")
                        sys.stdout.write("\033[?25h")  # Mostra cursor
                        sys.stdout.flush()
                        return selected

                # --------------------------
                # LINUX / MAC (strings)
                # --------------------------
                else:
                    # Seta ↑
                    if key == "\x1b[A":
                        selected = (selected - 1) % len(options)
                        needs_redraw = True
                    # Seta ↓
                    elif key == "\x1b[B":
                        selected = (selected + 1) % len(options)
                        needs_redraw = True
                    # Vim-style: k (up) / j (down)
                    elif key in ("k", "K"):
                        selected = (selected - 1) % len(options)
                        needs_redraw = True
                    elif key in ("j", "J"):
                        selected = (selected + 1) % len(options)
                        needs_redraw = True
                    # ENTER
                    elif key in ("\n", "\r"):
                        # Limpa menu e mostra cursor
                        for _ in range(menu_lines):
                            sys.stdout.write("\033[F\033[K")
                        sys.stdout.write("\033[?25h")  # Mostra cursor
                        sys.stdout.flush()
                        return selected
                    # ESC sozinho - ignora
                    elif key == "\x1b":
                        continue

                # Atualiza o menu apenas se necessário
                if needs_redraw:
                    # Move cursor para cima e limpa cada linha
                    for _ in range(menu_lines):
                        sys.stdout.write("\033[F")  # Sobe uma linha
                        sys.stdout.write("\033[K")  # Limpa a linha
                    sys.stdout.flush()
                    # Redesenha o menu
                    console.print(render_menu())
                
        except (KeyboardInterrupt, EOFError):
            # Tratamento seguro de interrupções
            for _ in range(menu_lines):
                sys.stdout.write("\033[F\033[K")
            sys.stdout.write("\033[?25h")  # Mostra cursor
            sys.stdout.flush()
            return len(options) - 1  # Retorna última opção (geralmente "Sair")
