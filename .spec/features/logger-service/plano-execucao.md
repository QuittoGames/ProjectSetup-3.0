# Plano de execução — logger-service

> gerado por `onp-spec plano` em 2026-09-10 23:38 — NÃO edite à mão;
> mudou tasks.md ou a config? Regenere: `onp-spec plano logger-service`

## Resumo — o que vai acontecer

- **8 tarefa(s) pendente(s)**: 8 em 3 faixa(s) paralela(s) + 0 sequencial(is)
- **1 faixa = 1 worktree + 1 branch + 1 janela de contexto limpa** — faixas não compartilham nenhum arquivo entre si
- prefere outra seleção ou uma após a outra? Regenere com `onp-spec plano logger-service --paralelizar T-xxx,T-yyy` ou `--sequencial`
- tudo acontece na branch de trabalho `spec/logger-service`; levar para a main é decisão sua

## Faixas e ondas

### Onda 1 — faixa-1 ∥ faixa-2 ∥ faixa-3

#### faixa-1 — branch `spec/logger-service-faixa-1` — worktree `../onp-worktrees/ProjectSetup-3.0-logger-service-faixa-1`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-001 | Implementar LoggerService singleton com get_logger(category) | `(default)` | medium | `projectsetup3/src/core/Services/Egine/Logger/LoggerService.py` |
| T-002 | Configurar handlers: JSON stdout + RichHandler (TUI) + StreamHandler (CLI) | `(default)` | medium | `projectsetup3/src/core/Services/Egine/Logger/LoggerService.py` |
| T-003 | File handler condicional (Config.Debug) → logs/nLog.log | `(default)` | medium | `projectsetup3/src/core/Services/Egine/Logger/LoggerService.py` |
| T-004 | Níveis: INFO default, DEBUG quando Config.Debug=True | `(default)` | medium | `projectsetup3/src/core/Services/Egine/Logger/LoggerService.py` |
| T-005 | Formatter JSON estruturado para stdout | `(default)` | medium | `projectsetup3/src/core/Services/Egine/Logger/LoggerService.py` |
| T-006 | Context manager timer() para performance logging | `(default)` | medium | `projectsetup3/src/core/Services/Egine/Logger/LoggerService.py` |

#### faixa-2 — branch `spec/logger-service-faixa-2` — worktree `../onp-worktrees/ProjectSetup-3.0-logger-service-faixa-2`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-007 | Testes unitários cobrindo AC-001 a AC-011 | `(default)` | medium | `tests/unit/test_logger_service.py` |

#### faixa-3 — branch `spec/logger-service-faixa-3` — worktree `../onp-worktrees/ProjectSetup-3.0-logger-service-faixa-3`

| tarefa | título | modelo | esforço | arquivos |
|---|---|---|---|---|
| T-008 | Integração: expor LoggerService nos serviços legados | `(default)` | medium | `projectsetup3/src/core/Services/Egine/ProjectFactory.py`, `projectsetup3/src/CLI/CLIService.py` |

## Gestão de branches e commits

1. branch de trabalho `spec/logger-service` criada do ponto atual (se ainda não existir)
2. cada faixa nasce dela como branch própria e roda no seu worktree — **1 tarefa = 1 commit** (`T-xxx feature: título`)
3. terminou a onda → merge `--no-ff` de cada faixa de volta, na ordem; conflito interrompe a faixa e pede resolução humana
4. faixa mesclada → worktree removido, branch apagada, tarefa marcada `[concluida]` no tasks.md
5. gate final na branch de trabalho: `onp-spec verify logger-service` + `onp-spec audit --ci` — **exit 0 ou não está pronto**

## Como executar

### ▶ Execução — OpenCode headless (opencode run)

```bash
bash .spec/features/logger-service/executar-tarefas.sh
```

Cada faixa roda `opencode run` com **janela de contexto limpa**, no seu worktree, com
`--model` já definido por tarefa (formato provider/model) e `--auto` para permissões do headless (configurável em OPENCODE_FLAGS). Os prompts exatos estão
embutidos no script — quer rodar uma faixa na mão, é só copiá-los de lá.
Logs: `../onp-worktrees/ProjectSetup-3.0-logger-service-logs/`.

**Confirmação de custos — antes de executar**: os modelos por tarefa estão
nas tabelas acima; o agente CONFIRMA com o usuário se estão dentro da
licença/cota dele (modelo forte + esforço alto torra tokens). No opencode
o modelo é `provider/model` — modelo vazio significa "default configurado".

**Esforço no OpenCode**: fica registrado no plano, mas NÃO vira flag — o
nível de raciocínio é o `--variant` do CLI (específico do provider, ex.:
high, max) ou a config do modelo no opencode.json. A coluna "esforço"
acima é informativa; para controlar o raciocínio, use `--variant` ou o
modelo. Para gastar menos: `onp-spec plano logger-service --esforco baixo`
(tudo) ou por tarefa `onp-spec tarefa logger-service T-xxx --modelo <provider/model>` — e regenere o plano.

### 📣 Acompanhamento — tabela + resumo no chat (a cada 1 min)

O script roda em **background**: o agente AVISA o usuário antes de iniciar e,
enquanto roda, posta no chat a cada ~1 minuto a **tabela de andamento** (qual
tarefa está rodando, qual não está, o que concluiu/falhou) junto com o
**resumo geral de andamento** (escrito por IA; sem IA, o motor resume). Ao
final, o usuário recebe o resumo completo da execução. A qualquer momento:

```bash
onp-spec resumo logger-service --tabela   # a tabela de andamento
onp-spec resumo logger-service            # o resumo em texto
```

