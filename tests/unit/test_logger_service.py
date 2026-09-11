import pytest
import json
import os
import sys
import logging
from pathlib import Path
from unittest.mock import patch, PropertyMock, MagicMock
from io import StringIO

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from projectsetup3.src.core.Services.Engine.Logger.LoggerService import (
    LoggerService,
    JsonFormatter,
    ConsoleFormatter,
    TextFormatter,
)


class TestLoggerServiceSingleton:
    """US-001: Logger singleton com categorias (estilo Log4j/Spring)"""

    def setup_method(self):
        """Limpar instâncias entre testes."""
        LoggerService.reset()

    def teardown_method(self):
        LoggerService.reset()

    def test_AC_001_singleton_por_categoria(self):
        """AC-001: Obter logger por categoria retorna instância singleton por nome"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            LoggerService.reset()
            logger1 = LoggerService.get_logger("ProjectFactory")
            logger2 = LoggerService.get_logger("ProjectFactory")
            assert logger1 is logger2, (
                "Duas chamadas com mesma categoria devem retornar a mesma instância"
            )

    def test_AC_002_categorias_diferentes_instancias_diferentes(self):
        """AC-002: Categorias diferentes retornam instâncias diferentes"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            LoggerService.reset()
            logger1 = LoggerService.get_logger("ProjectFactory")
            logger2 = LoggerService.get_logger("CLIService")
            assert logger1 is not logger2, (
                "Categorias diferentes devem retornar instâncias distintas"
            )
            assert logger1._category == "ProjectFactory"
            assert logger2._category == "CLIService"


class TestLoggerServiceLevels:
    """US-002: Níveis de log configuráveis via Config.Debug"""

    def setup_method(self):
        LoggerService.reset()

    def teardown_method(self):
        LoggerService.reset()

    def test_AC_003_nivel_padrao_info_quando_debug_false(self):
        """AC-003: Nível padrão é INFO quando Config.Debug=False"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            LoggerService.reset()
            logger = LoggerService.get_logger("Test")
            assert logger._debug_mode is False
            assert logger._logger.level == logging.INFO

    def test_AC_004_nivel_debug_quando_debug_true(self):
        """AC-004: Nível DEBUG habilitado quando Config.Debug=True"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=True,
        ):
            LoggerService.reset()
            logger = LoggerService.get_logger("Test")
            assert logger._debug_mode is True
            assert logger._logger.level == logging.DEBUG


class TestLoggerServiceOutput:
    """US-003: Saída dual: JSON (stdout) + arquivo texto (quando Debug)"""

    def setup_method(self):
        LoggerService._instances.clear()

    def teardown_method(self):
        LoggerService._instances.clear()

    def test_AC_005_stdout_sempre_json_estruturado(self):
        """AC-005: Stdout sempre em JSON estruturado"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            LoggerService.reset()
            logger = LoggerService.get_logger("Test")

            old_stdout = sys.stdout
            sys.stdout = captured = StringIO()

            # Atualizar stream do JSON handler para o novo stdout
            for handler in logger._logger.handlers:
                if (
                    isinstance(handler, logging.StreamHandler)
                    and handler.stream == old_stdout
                ):
                    handler.stream = captured
                    break

            try:
                logger.info("mensagem de teste", contexto="valor")
                output = captured.getvalue().strip()
                assert output, "Deve haver saída no stdout"

                log_data = json.loads(output)
                assert "timestamp" in log_data
                assert "level" in log_data
                assert log_data["level"] == "INFO"
                assert "logger" in log_data
                assert log_data["logger"] == "ps3.Test"
                assert "message" in log_data
                assert log_data["message"] == "mensagem de teste"
                assert "context" in log_data
                assert log_data["context"] == {"contexto": "valor"}
            finally:
                sys.stdout = old_stdout

    def test_AC_006_arquivo_criado_apenas_quando_debug_true(self, tmp_path):
        """AC-006: Arquivo logs/nLog.log criado apenas quando Config.Debug=True"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=True,
        ):
            LoggerService._instances.clear()

            old_cwd = os.getcwd()
            os.chdir(tmp_path)

            try:
                logger = LoggerService.get_logger("TestFile")
                logger.info("teste arquivo")

                log_file = tmp_path / "logs" / "nLog.log"
                assert log_file.exists(), (
                    "Arquivo nLog.log deve ser criado quando Debug=True"
                )

                content = log_file.read_text(encoding="utf-8")
                assert "teste arquivo" in content
                assert "ps3.TestFile" in content
            finally:
                os.chdir(old_cwd)
                LoggerService._instances.clear()

    def test_AC_007_arquivo_nao_criado_quando_debug_false(self, tmp_path):
        """AC-007: Arquivo NÃO criado quando Config.Debug=False"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            LoggerService._instances.clear()

            old_cwd = os.getcwd()
            os.chdir(tmp_path)

            try:
                logger = LoggerService.get_logger("TestNoFile")
                logger.info("teste sem arquivo")

                log_dir = tmp_path / "logs"
                assert not log_dir.exists() or not (log_dir / "nLog.log").exists(), (
                    "Arquivo nLog.log NÃO deve ser criado quando Debug=False"
                )
            finally:
                os.chdir(old_cwd)


class TestLoggerServiceRuntime:
    """US-004: Integração com Rich (TUI) e console nerd-fonts (CLI ps3)"""

    def setup_method(self):
        LoggerService._instances.clear()

    def teardown_method(self):
        LoggerService._instances.clear()

    def test_AC_008_handler_rich_tui(self):
        """AC-008: Handler Rich ativo no runtime principal (TUI)"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            with patch.dict(os.environ, {"PS3_RUNTIME": "tui"}):
                LoggerService._instances.clear()
                logger = LoggerService.get_logger("TestTUI")

                from rich.logging import RichHandler

                has_rich = any(
                    isinstance(h, RichHandler) for h in logger._logger.handlers
                )
                assert has_rich, "Deve ter RichHandler quando PS3_RUNTIME=tui"

    def test_AC_009_handler_console_cli(self):
        """AC-009: Handler console simples ativo no CLI ps3"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            with patch.dict(os.environ, {"PS3_RUNTIME": "cli"}):
                LoggerService._instances.clear()
                logger = LoggerService.get_logger("TestCLI")

                from rich.logging import RichHandler

                has_rich = any(
                    isinstance(h, RichHandler) for h in logger._logger.handlers
                )
                assert not has_rich, "NÃO deve ter RichHandler quando PS3_RUNTIME=cli"

                has_console_formatter = any(
                    isinstance(h.formatter, ConsoleFormatter)
                    for h in logger._logger.handlers
                    if h.formatter
                )
                assert has_console_formatter, "Deve ter ConsoleFormatter no CLI"


class TestLoggerServiceTimer:
    """US-005: Logging de performance (duração) em nível DEBUG"""

    def setup_method(self):
        LoggerService._instances.clear()

    def teardown_method(self):
        LoggerService._instances.clear()

    def test_AC_010_timer_loga_duracao_em_debug(self):
        """AC-010: Método timer() retorna context manager que loga duração em DEBUG"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=True,
        ):
            LoggerService.reset()
            logger = LoggerService.get_logger("TestTimer")

            old_stdout = sys.stdout
            sys.stdout = captured = StringIO()

            # Atualizar stream do JSON handler para o novo stdout
            for handler in logger._logger.handlers:
                if (
                    isinstance(handler, logging.StreamHandler)
                    and handler.stream == old_stdout
                ):
                    handler.stream = captured
                    break

            try:
                with logger.timer("operação X"):
                    pass

                output = captured.getvalue().strip()
                assert output, "Deve haver saída no stdout"

                log_data = json.loads(output)
                assert log_data["level"] == "DEBUG"
                assert "operação X concluída em" in log_data["message"]
                assert "ms" in log_data["message"]
            finally:
                sys.stdout = old_stdout
                LoggerService.reset()

    def test_AC_011_timer_nao_loga_quando_debug_false(self):
        """AC-011: Timer não loga quando Config.Debug=False"""
        with patch(
            "projectsetup3.src.config.Config.Config.Debug",
            new_callable=PropertyMock,
            return_value=False,
        ):
            LoggerService._instances.clear()
            logger = LoggerService.get_logger("TestTimerNoDebug")

            old_stdout = sys.stdout
            sys.stdout = captured = StringIO()

            try:
                with logger.timer("operação Y"):
                    pass

                output = captured.getvalue().strip()
                debug_logs = [
                    line for line in output.split("\n") if '"level": "DEBUG"' in line
                ]
                assert len(debug_logs) == 0, "Timer NÃO deve logar quando Debug=False"
            finally:
                sys.stdout = old_stdout


class TestFormatters:
    """Testes dos formatters individuais"""

    def test_json_formatter_timestamp_iso8601_com_tz(self):
        """Timestamp deve ser ISO 8601 com timezone"""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test message",
            args=(),
            exc_info=None,
        )
        record.context = {"key": "value"}

        output = formatter.format(record)
        log_data = json.loads(output)

        assert "timestamp" in log_data
        timestamp = log_data["timestamp"]
        assert "T" in timestamp
        assert "+" in timestamp or "-" in timestamp.split("T")[1]

    def test_console_formatter_icones_nerd_fonts(self):
        """ConsoleFormatter deve incluir ícones nerd-fonts"""
        formatter = ConsoleFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg="warning message",
            args=(),
            exc_info=None,
        )

        output = formatter.format(record)
        assert "" in output, "Deve conter ícone nerd-font para WARNING"
        assert "WARNING" in output

    def test_text_formatter_legivel(self):
        """TextFormatter deve produzir formato legível para arquivo"""
        formatter = TextFormatter()
        record = logging.LogRecord(
            name="ps3.Test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="error message",
            args=(),
            exc_info=None,
        )
        record.context = {"detail": "info"}

        output = formatter.format(record)
        assert "ps3.Test" in output
        assert "ERROR" in output
        assert "error message" in output
        assert "detail" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
