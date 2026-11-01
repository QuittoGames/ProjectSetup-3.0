# TODO — Correção de Inconsistências (Audit 2026-10-18)

**Relatório:** `.agents/reports/test-audit-projectsetup.json`  
**Agente:** unit-test-engineer  
**Modo:** BUILD/REVIEW  
**Total de achados:** 22 (3 critical, 4 high, 6 medium, 9 low)

---

## Prioridade CRITICAL

- [ ] **F1** — Corrigir comparação `is` encadeada em `ProjectFactory.py:50`  
  → `self._readmeService.isActive() is content is not None` → `isActive() and content is not None`  
  → **[A] Agent** — patch de 1 linha; requer teste de regressão  
  → **[S] Shared** — validar com probe P06

- [ ] **F2** — Corrigir chamada `tool.init_git_repository(gitRepoLink)` em `ProjectFactory.py:70`  
  → Adicionar argumento `path`: `tool.init_git_repository(gitRepoLink, str(project_path))`  
  → **[A] Agent** — patch de 1 linha; requer mock de tool para teste  
  → **[S] Shared** — validar com probe P05

- [ ] **F3** — Corrigir import de `GeminiClient` em `READMEservice.py:814` ou migrar para `AIClient`  
  → Decisão de design: manter GeminiClient legado ou refatorar para AIClient  
  → **[H] Human** — decisão de arquitetura  
  → **[A] Agent** — implementar após decisão

---

## Prioridade HIGH

- [ ] **F4** — Corrigir console script `ps3` no `pyproject.toml`  
  → Mudar `ps3 = projectsetup3.index:main` para `ps3 = projectsetup3.run:main`  
  → **[A] Agent** — patch de config; requer teste manual do script  
  → **[S] Shared** — validar com probe P03

- [ ] **F5** — Corrigir `ProjectService.create_project:59-60` para preservar tipos de exceção  
  → Trocar `raise Exception(...)` por re-levantar `ValueError`/`NotADirectoryError` originais ou criar exceção de domínio  
  → **[A] Agent** — refatoração de error handling  
  → **[S] Shared** — validar com probe P09

- [ ] **F6** — Reordenar `except` em `ProjectService.loadProjectConfiguration:73-78`  
  → Mover `except Exception:` para depois de `except ModuleNotFoundError:` e `except FileNotFoundError:`  
  → **[A] Agent** — reorder de 5 linhas; requer teste de edge case  
  → **[S] Shared** — validar com teste unitário

- [ ] **F7** — Decidir destino de `api/ProjectManager.py` legada  
  → Opções: (a) remover módulo, (b) refatorar completamente, (c) documentar como deprecated  
  → **[H] Human** — decisão de escopo  
  → **[A] Agent** — implementar após decisão

---

## Prioridade MEDIUM

- [ ] **F8** — Corrigir `tool.getIsntallCommand` para retornar string  
  → Substituir `lambda`/`None` por string de comando real (Windows/Linux)  
  → **[A] Agent** — refatoração de tool  
  → **[S] Shared** — validar com probe P04

- [ ] **F9** — Proteger acesso a `sys.argv[2]` em `CLIService.listDataProjects:101`  
  → Adicionar check `if len(sys.argv) < 3: print usage; return`  
  → **[A] Agent** — patch de 2 linhas  
  → **[S] Shared** — validar com probe P12

- [ ] **F10** — Normalizar entrada em `Config.dispatch_path`  
  → Strip leading dot antes de comparar: `ext = lang.lstrip('.')`  
  → **[A] Agent** — patch de 1 linha; requer teste TUI  
  → **[S] Shared** — validar com probe P11

- [ ] **F11** — Corrigir path em `tool.verify_modules:30-34`  
  → Mudar `src/core/Services/requirements/requirements.txt` para `projectsetup3/requirements/requirements.txt`  
  → **[A] Agent** — patch de 1 linha  
  → **[S] Shared** — validar com probe P13

- [ ] **F12** — Adicionar warning em `tool.type_to_extension` fallback  
  → Trocar `return '.txt'` por `warnings.warn(f'Unknown lang: {lang}'); return '.txt'`  
  → **[A] Agent** — patch de 1 linha; requer import de warnings  
  → **[S] Shared** — validar com probe P14

- [ ] **F13** — Resolver duplicatas em `AIClient`  
  → Opções: (a) remover sync versions, (b) renomear async (ex: `async_list_models`), (c) usar `@overload`  
  → **[H] Human** — decisão de design  
  → **[A] Agent** — implementar após decisão

---

## Prioridade LOW

- [ ] **F14** — Renomear `Config.getCofig` → `getConfig` + corrigir anotação `Debug: str` → `Debug: bool`  
  → **[A] Agent** — rename + type fix  
  → **[S] Shared** — validar com P10

- [ ] **F15** — Corrigir path de `Config.Fonts` para `projectsetup3/Fonts`  
  → **[A] Agent** — patch de config

- [ ] **F16** — Renomear `RESQ` → `SEARCH` ou corrigir comentário em `RegistredProjectType.py`  
  → **[H] Human** — decisão de naming

- [ ] **F17** — Atualizar `ps3cli.bat` path de `src\\CLI\\CLIService.py` → `projectsetup3.src.app.CLI.CLIService`  
  → **[A] Agent** — patch de 2 linhas

- [ ] **F18** — Mover `projectsetup3/test/`, `.github/`, `build/`, `dist/` para raiz do projeto  
  → **[H] Human** — decisão de estrutura  
  → **[A] Agent** — executar movimentação após decisão

- [ ] **F19** — Substituir `setx PATH` por PowerShell em `InstallService.setEnv`  
  → **[A] Agent** — refatoração de installer

- [ ] **F20** — Corrigir `History.run` daemon thread para thread síncrona ou queue  
  → **[A] Agent** — refatoração de threading  
  → **[S] Shared** — testar com múltiplas escritas

- [ ] **F21** — Renomear typos sistêmicos (basestruture, Registred, getCofig, Avaliable)  
  → **[H] Human** — decisão de escopo (afeta API pública)

- [ ] **F22** — Corrigir regex em `ProjectFactory.create:60` para testar basename  
  → `re.match(r'.+\\..+$', Path(full_path).name)`  
  → **[A] Agent** — patch de 1 linha

---

## Legenda

- **[H] Human** — requer decisão do developer (arquitetura, escopo, naming)
- **[A] Agent** — implementação pelo agente após autorização/decisão
- **[S] Shared** — agente implementa + human valida resultado

## Bloqueados

- **F3** aguarda decisão de design (GeminiClient vs AIClient)
- **F7** aguarda decisão de escopo (remover vs refatorar ProjectManager)
- **F13** aguarda decisão de design (sync/async API)
- **F16** aguarda decisão de naming
- **F18** aguarda decisão de estrutura de projeto
- **F21** aguarda decisão de escopo (refatoração global de nomes)

---

**Próximo passo:** Revisar este TODO, decidir nos itens bloqueados, e priorizar F1/F2 (críticos) para correção imediata.
