"""
Ponto de entrada para o executável PyInstaller.
Este arquivo evita problemas com importações relativas.
"""

import sys
from pathlib import Path

# Add src to path for src layout
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from projectsetup3.cli import main

if __name__ == "__main__":
    main()
