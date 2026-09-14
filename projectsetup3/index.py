"""
Compatibility launcher.

A implementação real do runtime vive em ``projectsetup3.src.runtime.index``
(composition root). Este módulo apenas encaminha a execução e preserva os
contratos públicos históricos (``main``, ``run``) usados por ``ps3``,
``python -m projectsetup3`` e ``CLIService``.
"""

from projectsetup3.src.runtime.index import main, run

__all__ = ["main", "run"]
