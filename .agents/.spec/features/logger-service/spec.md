# Spec: Logger service

> feature: logger-service
> status: rascunho

<!--
  Como ler este arquivo (o formato é verificado por `onp-spec audit`):
  - US-xxx = história de usuário · AC-xxx = critério de aceite
    ASM-xxx = suposição · Q-xxx = pergunta em aberto
    São códigos de rastreio: ligam a especificação às tarefas e aos testes.
  - Toda história de usuário precisa de pelo menos um critério de aceite.
  - Todo critério de aceite precisa de Dado/Quando/Então completos.
  - Os códigos são únicos no projeto inteiro (nunca reutilize um número).
  - Suposições e Perguntas em aberto são OBRIGATÓRIAS: se não há nenhuma,
    escreva "Nenhuma." — mas desconfie: quase toda feature esconde uma.
-->

## Contexto

O projeto ProjectSetup-3.0 precisa de um sistema de logging robusto, tipado e configurável que substitua prints espalhados e facilite a refatoração dos serviços legados. O LoggerService deve seguir o padrão singleton com suporte a categorias (análogo ao Log4j/Spring), permitindo que cada serviço/classe obtenha um logger nomeado. A configuração de nível e saída é controlada centralmente via `Config.Debug` (bool). Logs persistem em arquivo (`logs/nLog.log`) apenas quando `Debug=True`; em produção (`Debug=False`) apenas JSON no stdout. Integração com Rich para TUI principal e console nerd-fonts para CLI ps3.

## Histórias

### US-001 — Logger singleton com categorias (estilo Log4j/Spring)

Como **desenvolvedor do PS3**, quero **obter um logger nomeado por categoria** (ex.: `LoggerService.get_logger("ProjectFactory")`) para que **cada serviço tenha seu contexto de log isolado e rastreável**.

#### AC-001 — Obter logger por categoria retorna instância singleton por nome

- **Dado** que `LoggerService` foi inicializado
- **Quando** chamo `LoggerService.get_logger("ProjectFactory")` duas vezes
- **Então** ambas as chamadas retornam a **mesma instância** (singleton por categoria)

#### AC-002 — Categorias diferentes retornam instâncias diferentes

- **Dado** que `LoggerService` foi inicializado
- **Quando** chamo `LoggerService.get_logger("ProjectFactory")` e `LoggerService.get_logger("CLIService")`
- **Então** recebo **duas instâncias distintas**, cada uma com seu `name` igual à categoria

### US-002 — Níveis de log configuráveis via Config.Debug

Como **desenvolvedor**, quero **nível INFO por padrão e DEBUG apenas quando `Config.Debug=True`** para que **produção não vaze detalhes e desenvolvimento tenha verbosidade**.

#### AC-003 — Nível padrão é INFO quando Config.Debug=False

- **Dado** `Config.Debug = False`
- **Quando** obtenho um logger via `LoggerService.get_logger("Test")`
- **Então** o logger efetivo loga `INFO`, `WARN`, `ERROR`, `CRITICAL` mas **não loga `DEBUG`**

#### AC-004 — Nível DEBUG habilitado quando Config.Debug=True

- **Dado** `Config.Debug = True`
- **Quando** obtenho um logger via `LoggerService.get_logger("Test")`
- **Então** o logger efetivo loga **todos os níveis**, inclusive `DEBUG`

### US-003 — Saída dual: JSON (stdout) + arquivo texto (quando Debug)

Como **operador/DevOps**, quero **logs em JSON no stdout para parsing e arquivo legível em desenvolvimento** para que **pipeline de logs e debug local coexistam**.

#### AC-005 — Stdout sempre em JSON estruturado

- **Dado** qualquer valor de `Config.Debug`
- **Quando** um log é emitido
- **Então** a linha no stdout é **JSON válido** com campos: `timestamp`, `level`, `logger`, `message`, `context` (opcional)

#### AC-006 — Arquivo `logs/nLog.log` criado apenas quando Config.Debug=True

- **Dado** `Config.Debug = True`
- **Quando** o primeiro log é emitido
- **Então** o diretório `logs/` é criado na raiz do projeto (runtime) e o arquivo `nLog.log` recebe logs em **formato texto legível**

#### AC-007 — Arquivo NÃO criado quando Config.Debug=False

- **Dado** `Config.Debug = False`
- **Quando** logs são emitidos
- **Então** **nenhum arquivo** é criado em `logs/` e nada é escrito em disco

### US-004 — Integração com Rich (TUI) e console nerd-fonts (CLI ps3)

Como **usuário da TUI principal**, quero **logs renderizados com Rich** para que **cores, markup e layout funcionem no dashboard**; como **usuário do CLI ps3**, quero **console simples com ícones nerd-fonts**.

#### AC-008 — Handler Rich ativo no runtime principal (TUI)

- **Dado** execução via `index.py` (TUI principal)
- **Quando** logs são emitidos
- **Então** a saída no terminal usa `rich.logging.RichHandler` com markup, cores e traceback rico

#### AC-009 — Handler console simples ativo no CLI ps3

- **Dado** execução via `cli.py` / `run.py` (ps3cli)
- **Quando** logs são emitidos
- **Então** a saída usa `logging.StreamHandler` com formatador que inclui ícones nerd-fonts (ex.: ``, ``, ``)

### US-005 — Logging de performance (duração) em nível DEBUG

Como **desenvolvedor**, quero **medir tempo de execução de operações** via logger para que **gargalos sejam identificados quando `Debug=True`**.

#### AC-010 — Método `timer()` retorna context manager que loga duração em DEBUG

- **Dado** `Config.Debug = True` e logger obtido via `get_logger("Test")`
- **Quando** uso `with logger.timer("operação X"): ...`
- **Então** ao sair do bloco, um log `DEBUG` é emitido: `"operação X concluída em 123.45ms"`

#### AC-011 — Timer não loga quando Config.Debug=False

- **Dado** `Config.Debug = False`
- **Quando** uso `with logger.timer("operação X"): ...`
- **Então** **nenhum log** de duração é emitido (overhead zero)

### US-006 — Testes unitários cobrindo comportamento público

Como **mantenedor**, quero **testes automatizados** para que **regressões no logger sejam detectadas no CI**.

#### AC-012 — Testes verificam singleton por categoria, níveis, formatos, arquivo, timer

- **Dado** suite de testes rodando
- **Quando** executo `pytest tests/unit/test_logger_service.py`
- **Então** todos os testes passam cobrindo AC-001 a AC-011

## Fora de escopo

- Adaptação da TUI existente para consumir o novo sistema de log (será feito depois, item separado)
- Handlers remotos (syslog, ELK, Loki, etc.) — podem ser adicionados futuramente via handlers customizados
- Rotação de log por tamanho/tempo (arquivo é simples, apenas `nLog.log`; rotação futura se necessário)
- Filtros avançados por módulo/thread — não necessário no MVP

## Suposições

| ID | Suposição | Status | Resolução |
|---|---|---|---|
| ASM-001 | `Config.Debug` é um `bool` acessível via `from projectsetup3.src.config.Config import Config` | confirmada | — |
| ASM-002 | A raiz do projeto em runtime é obtida via `Path.cwd()` ou `Config.DIRETORIO` | aberta | — |
| ASM-003 | `rich` já está nas dependências do projeto (usado na TUI) | confirmada | — |
| ASM-004 | Python 3.10+ (match-case, union types `X | Y`) | confirmada | — |
| ASM-005 | Serviços legados serão refatorados para usar `LoggerService.get_logger(__name__)` | confirmada | — |

## Perguntas em aberto

| ID | Pergunta | Status | Resposta |
|---|---|---|---|
| Q-001 | Qual o caminho exato da raiz do projeto para criar `logs/`? (`Path.cwd()` vs `Config.DIRETORIO` vs outro) | respondida | `Path.cwd()` — raiz do projeto em runtime (onde o CLI/TUI é executado) |
| Q-002 | O logger deve expor `setLevel()` dinâmico em runtime ou só na inicialização? | respondida | Apenas na inicialização (configuração via `Config.Debug`); mudança de nível em runtime não é necessária no MVP |
| Q-003 | Formato do timestamp no JSON: ISO 8601 com timezone (`2026-09-10T15:30:45.123-03:00`) ou Unix epoch? | respondida | ISO 8601 com timezone (ex.: `2026-09-10T15:30:45.123-03:00`) — padrão da indústria, parsável, legível |
