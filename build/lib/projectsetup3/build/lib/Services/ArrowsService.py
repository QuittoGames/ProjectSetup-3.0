import time
import sys

from rich.live import Live
from rich.panel import Panel
from rich.box import ROUNDED
from rich.align import Align


class ArrrowsService:

    @staticmethod
    def arrow_menu(options):
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
                    return sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)

        selected = 0

        # ========================
        #   UI DO MENU
        # ========================
        def render():
            itens = []
            for i, op in enumerate(options):
                if i == selected:
                    itens.append(f"[bold cyan]›[/bold cyan] [white]{op}[/white]")
                else:
                    itens.append(f"  [dim]{op}[/dim]")

            return Panel(
                "\n".join(itens),
                border_style="cyan",
                width=60,
                padding=(1, 2),
                box=ROUNDED,
            )

        # ========================
        #   LOOP PRINCIPAL
        # ========================
        with Live(Align.center(render()), refresh_per_second=20) as live:
            while True:
                key = get_key()

                # --------------------------
                # WINDOWS (bytes)
                # --------------------------
                if isinstance(key, bytes):

                    # Seta ↑
                    if key in (b"\xe0H", b"\x00H"):
                        selected = (selected - 1) % len(options)

                    # Seta ↓
                    elif key in (b"\xe0P", b"\x00P"):
                        selected = (selected + 1) % len(options)

                    # ENTER
                    elif key == b"\r":
                        return selected

                # --------------------------
                # LINUX (strings)
                # --------------------------
                else:
                    # Seta ↑/↓ como sequência escape
                    if key == "\x1b":
                        nxt = sys.stdin.read(2)
                        full = key + nxt

                        if full == "\x1b[A":  # ↑
                            selected = (selected - 1) % len(options)

                        elif full == "\x1b[B":  # ↓
                            selected = (selected + 1) % len(options)

                    # Vim-style: k (up) / j (down)
                    elif key == "k":
                        selected = (selected - 1) % len(options)

                    elif key == "j":
                        selected = (selected + 1) % len(options)

                    # ENTER
                    elif key == "\n":
                        return selected

                live.update(Align.center(render()))
