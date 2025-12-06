import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))        # pacote
sys.path.insert(0, str(root_dir.parent)) # módulos locais como Config, tool

# Dentro de projectsetup3/__main__.py
from .Services.CLIService import CLIService
from .Config import Config
from .tool import tool


def main():
    service = CLIService()
    service.run()

if __name__ == "__main__":
    main()
