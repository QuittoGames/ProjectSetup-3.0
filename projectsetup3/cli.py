import asyncio
import sys
from pathlib import Path

# Add src to path for src layout
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from projectsetup3.Services.CLI.CLIService import CLIService


def main():
    service = CLIService()
    service.run()
