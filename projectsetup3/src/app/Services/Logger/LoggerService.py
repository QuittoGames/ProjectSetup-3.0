from dataclasses import dataclass, field
from typing import Dict, Optional, Any, ClassVar
import logging
import json
import sys
import os
from pathlib import Path
from contextlib import contextmanager
import time
from datetime import datetime

from projectsetup3.src.core.config.Config import Config


# Variáveis de classe PARA O SINGLETON (fora do dataclass)
_instances: Dict[str, "LoggerService"] = {}
_initialized_flag: Dict[str, bool] = {}


@dataclass
class LoggerService:
    """Singleton logger service com suporte a categorias (estilo Log4j/Spring)."""

    _logger: Optional[logging.Logger] = field(default=None, init=False, repr=False)
    _category: str = field(default="", init=False, repr=False)
    _debug_mode: bool = field(default=False, init=False, repr=False)

    # Expor variáveis de módulo como atributos de classe para testes
    _instances: ClassVar[Dict[str, "LoggerService"]] = _instances
    _initialized_flag: ClassVar[Dict[str, bool]] = _initialized_flag

    def __new__(cls, category: str = "root") -> "LoggerService":
        if category not in _instances:
            instance = super().__new__(cls)
            instance._category = category
            _instances[category] = instance
        return _instances[category]

    def __init__(self, category: str = "root"):
        if _initialized_flag.get(category, False):
            return
        _initialized_flag[category] = True
        self._debug_mode = bool(getattr(Config, "Debug", False))
        self._setup_logger()

    @classmethod
    def get_logger(cls, category: str) -> "LoggerService":
        """Obtém instância singleton por categoria (estilo Log4j)."""
        return cls(category)

    @classmethod
    def reset(cls) -> None:
        """Limpa estado singleton para testes."""
        _instances.clear()
        _initialized_flag.clear()

    def _setup_logger(self) -> None:
        """Configura handlers: JSON stdout + Rich (TUI) ou StreamHandler (CLI) + File (se Debug)."""
        logger = logging.getLogger(f"ps3.{self._category}")
        logger.setLevel(logging.DEBUG if self._debug_mode else logging.INFO)
        logger.propagate = False

        logger.handlers.clear()

        # 1. JSON stdout handler (sempre ativo)
        json_handler = logging.StreamHandler(sys.stdout)
        json_handler.setFormatter(JsonFormatter())
        logger.addHandler(json_handler)

        # 2. Runtime detection: TUI (Rich) vs CLI (nerd-fonts)
        if self._is_tui_runtime():
            self._add_rich_handler(logger)
        else:
            self._add_console_handler(logger)

        # 3. File handler condicional (apenas quando Debug=True)
        if self._debug_mode:
            self._add_file_handler(logger)

        self._logger = logger

    def _is_tui_runtime(self) -> bool:
        return os.environ.get("PS3_RUNTIME", "cli") == "tui"

    def _add_rich_handler(self, logger: logging.Logger) -> None:
        try:
            from rich.logging import RichHandler
            from rich.console import Console

            console = Console(stderr=True)
            rich_handler = RichHandler(
                console=console,
                show_time=False,
                show_level=True,
                show_path=False,
                markup=True,
                rich_tracebacks=True,
            )
            rich_handler.setFormatter(logging.Formatter("%(message)s"))
            logger.addHandler(rich_handler)
        except ImportError:
            self._add_console_handler(logger)

    def _add_console_handler(self, logger: logging.Logger) -> None:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(ConsoleFormatter())
        logger.addHandler(console_handler)

    def _add_file_handler(self, logger: logging.Logger) -> None:
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "nLog.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(TextFormatter())
        logger.addHandler(file_handler)

    # Métodos de log
    def debug(self, message: str, **context: Any) -> None:
        self._logger.debug(message, extra={"context": context} if context else None)

    def info(self, message: str, **context: Any) -> None:
        self._logger.info(message, extra={"context": context} if context else None)

    def warn(self, message: str, **context: Any) -> None:
        self._logger.warning(message, extra={"context": context} if context else None)

    def warning(self, message: str, **context: Any) -> None:
        self.warn(message, **context)

    def error(self, message: str, **context: Any) -> None:
        self._logger.error(message, extra={"context": context} if context else None)

    def critical(self, message: str, **context: Any) -> None:
        self._logger.critical(message, extra={"context": context} if context else None)

    @contextmanager
    def timer(self, operation: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            if self._debug_mode:
                elapsed_ms = (time.perf_counter() - start) * 1000
                self.debug(f"{operation} concluída em {elapsed_ms:.2f}ms")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created)
            .astimezone()
            .isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        context = getattr(record, "context", None)
        if context:
            log_data["context"] = context
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    ICONS = {
        "DEBUG": " ",
        "INFO": " ",
        "WARNING": " ",
        "ERROR": " ",
        "CRITICAL": " ",
    }
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        icon = self.ICONS.get(record.levelname, " ")
        color = self.COLORS.get(record.levelname, "")
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        context = getattr(record, "context", None)
        ctx_str = f" {json.dumps(context, ensure_ascii=False)}" if context else ""
        return f"{color}{icon}{record.levelname:<8}{self.RESET} {timestamp} [{record.name}] {record.getMessage()}{ctx_str}"


class TextFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        context = getattr(record, "context", None)
        ctx_str = f" | {json.dumps(context, ensure_ascii=False)}" if context else ""
        exc = self.formatException(record.exc_info) if record.exc_info else ""
        return f"{timestamp} | {record.levelname:<8} | {record.name} | {record.getMessage()}{ctx_str}{exc}"
