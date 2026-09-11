# Tasks: Logger service

> feature: logger-service

<!--
  Como ler este arquivo (o formato é verificado por `onp-spec audit`):
  - T-xxx = tarefa (código de rastreio, único no projeto inteiro).
  - Toda tarefa referencia em `Refs:` pelo menos uma história de usuário
    (US-xxx) ou critério de aceite (AC-xxx).
  - Toda tarefa lista os arquivos que cria/altera em `Arquivos:` — capriche:
    é o que decide o que `onp-spec plano` roda em PARALELO (arquivos
    disjuntos) e o que roda em sequência.
  - Campos opcionais por tarefa, usados pelo plano de execução:
    `- Modelo: claude-sonnet-5` e `- Esforço: alto` (baixo|medio|alto|xalto|max).
  - Uma tarefa só pode virar [concluida] quando os critérios de aceite dela
    tiverem prova PASS registrada por `onp-spec verify`.
  Status: pendente | em-andamento | concluida
    (atalho: `onp-spec tarefa <feature> <T-xxx> <status>`)
-->

## T-001 — Implementar LoggerService singleton com get_logger(category) [pendente]

- Refs: US-001, AC-001, AC-002
- Arquivos: projectsetup3/src/core/Services/Egine/Logger/LoggerService.py
- Notas: Singleton por categoria (dict interno); correção typo LooggerService → LoggerService; @dataclass

## T-002 — Configurar handlers: JSON stdout + RichHandler (TUI) + StreamHandler (CLI) [pendente]

- Refs: US-004, AC-008, AC-009
- Arquivos: projectsetup3/src/core/Services/Egine/Logger/LoggerService.py
- Notas: Detectar runtime (TUI vs CLI) via env var ou arg; RichHandler com markup para TUI; StreamHandler com nerd-fonts para CLI

## T-003 — File handler condicional (Config.Debug) → logs/nLog.log [pendente]

- Refs: US-003, AC-006, AC-007
- Arquivos: projectsetup3/src/core/Services/Egine/Logger/LoggerService.py
- Notas: Criar logs/ em Path.cwd() apenas quando Config.Debug=True; formato texto legível; nenhum arquivo quando False

## T-004 — Níveis: INFO default, DEBUG quando Config.Debug=True [pendente]

- Refs: US-002, AC-003, AC-004
- Arquivos: projectsetup3/src/core/Services/Egine/Logger/LoggerService.py
- Notas: Ler Config.Debug na inicialização; setLevel correspondente; WARN simplificado (alias para WARNING)

## T-005 — Formatter JSON estruturado para stdout [pendente]

- Refs: US-003, AC-005
- Arquivos: projectsetup3/src/core/Services/Egine/Logger/LoggerService.py
- Notas: timestamp ISO 8601 com TZ, level, logger, message, context (opcional); json.dumps com ensure_ascii=False

## T-006 — Context manager timer() para performance logging [pendente]

- Refs: US-005, AC-010, AC-011
- Arquivos: projectsetup3/src/core/Services/Egine/Logger/LoggerService.py
- Notas: Retorna context manager; loga duração em DEBUG apenas quando Config.Debug=True; overhead zero quando False

## T-007 — Testes unitários cobrindo AC-001 a AC-011 [pendente]

- Refs: US-006, AC-012
- Arquivos: tests/unit/test_logger_service.py
- Notas: pytest + mocks para Config.Debug; testar singleton, níveis, formatos, arquivo, timer; @spec:AC-xxx no título

## T-008 — Integração: expor LoggerService nos serviços legados [pendente]

- Refs: US-001, AC-001, AC-002
- Arquivos: projectsetup3/src/core/Services/Egine/ProjectFactory.py, projectsetup3/src/CLI/CLIService.py
- Notas: Substituir prints por logger.get_logger(__name__); facilitar refatoração