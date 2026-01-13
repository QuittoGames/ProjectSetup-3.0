<div align="center">

# 🚀 ProjectSetup 3.0

**Gerador automático de estruturas de projetos para 40+ linguagens**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Rich](https://img.shields.io/badge/UI-Rich-cyan.svg)](https://github.com/Textualize/rich)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()
[![AI](https://img.shields.io/badge/AI-Gemini-orange.svg?logo=google)]()
[![Beta](https://img.shields.io/badge/Status-Beta%20Features-yellow.svg)]()

Cria a estrutura base dos seus projetos automaticamente.  
Personalizável via JSON, funciona no terminal.

[Instalação](#-instalação) • [Como usar](#-como-usar) • [Linguagens](#-linguagens-suportadas) • [Features BETA](#-features-beta) • [Launchers](#-launchers-multiplataforma)

</div>

---

## 💡 O que é?

Uma ferramenta CLI que automatiza a criação de projetos. Você define templates em JSON e ela cria toda a estrutura pra você.

**Exemplo:**
```bash
ps3cli . python meu-projeto
```

Isso cria automaticamente:
```
meu-projeto/
├── src/
│   ├── index.py
│   ├── tool.py
│   └── data.py
├── .gitignore
└── README.md
```

---

## ⚡ Por que usar?

- Poupa tempo na criação de projetos novos
- Estrutura organizada desde o início
- Templates personalizáveis via JSON
- Suporte para 40+ linguagens
- Interface visual no terminal
- Launchers multiplataforma (Windows & Linux)
- Histórico automático de projetos criados
- Geração inteligente de README com IA (BETA)

---

## 🚀 Instalação

```bash
git clone https://github.com/QuittoGames/ProjectSetup-3.0.git
cd ProjectSetup-3.0
```

### Método 1: Usando os Launchers (Recomendado)

**Windows:**
```batch
ps3.bat
```

**Linux/macOS:**
```bash
chmod +x ps3.sh
./ps3.sh
```

Os launchers instalam automaticamente todas as dependências!

### Método 2: Manual

```bash
cd projectsetup3
pip install -r requirements/requirements.txt
python -m projectsetup3
```

---

## 💻 Como usar

### Via CLI

```bash
# Sintaxe: ps3cli <path> <linguagem> <nome>
ps3cli . python meu-app
ps3cli D:/Projects javascript minha-api
ps3cli . rust game
```

### Interface Visual

```bash
python -m projectsetup3
```

Abre um menu interativo com navegação por setas.

### Via Python

```python
from projectsetup3.Services.ProjectManagerService import ProjectManagerService
from pathlib import Path

ProjectManagerService.create_project(
    name="meu-projeto",
    language="python",
    path=Path("./projetos")
)
```

---

## 🌐 Linguagens Suportadas (40+)

<details open>
<summary><b>Linguagens Populares</b></summary>

- **Python** - requirements.txt, src/, .gitignore
- **JavaScript** - package.json, node_modules/, ESLint
- **TypeScript** - tsconfig.json, dist/, tipos
- **Java** - Maven/Gradle, src/main/java/
- **Rust** - Cargo.toml, src/main.rs
- **Go** - go.mod, estrutura idiomática
- **Ruby** - Gemfile, estrutura Rails
- **PHP** - composer.json, Laravel/Symfony
- **Swift** - Package.swift, iOS/macOS
- **C#** - .csproj, .sln, .NET
- **C/C++** - CMakeLists.txt, Makefile

</details>

<details>
<summary><b>Ver todas as 40+ linguagens</b></summary>

- Assembly, Clojure, CoffeeScript, Crystal, Dart
- Dockerfile, Elixir, Elm, F#, Groovy
- Haskell, Haxe, INI, Kotlin, Lua
- Makefile, Markdown, OCaml, Perl, PowerShell
- R, Racket, Roblox Lua, Scala, Shell
- SQL, TeX, TOML, V, Web, YAML, Zig

</details>

---

## 🎨 Personalize seus Templates

Cada linguagem tem um arquivo JSON que define a estrutura do projeto.

**Exemplo:** `python.json`

```json
{
    ".gitignore": "__pycache__/\n*.pyc\nvenv/",
    "src/index.py": "print('Hello World')",
    "README.md": "# Meu Projeto"
}
```

Quando você roda o comando, ele:
1. Lê o JSON da linguagem
2. Cria cada arquivo com o conteúdo especificado
3. Organiza nas pastas corretas

---

## 🔧 Adicionando um Novo Tipo de Projeto

### Passo 1: Crie o Template JSON

Crie um arquivo em `appdata/Languages/nome.json`:

```json
{
    ".gitignore": "node_modules/\n.env",
    
    "src/server.js": "const express = require('express');\nconst app = express();\n\napp.listen(3000);",
    
    "src/routes/users.js": "const router = require('express').Router();\n\nmodule.exports = router;",
    
    "package.json": "{\n  \"name\": \"___PROJECTNAME__\",\n  \"version\": \"1.0.0\"\n}",
    
    ".env.example": "PORT=3000\nDB_URL=mongodb://localhost"
}
```

**Dicas do JSON:**
- Use `/` para criar pastas: `"src/routes/users.js"` cria `src/routes/`
- Use `___PROJECTNAME__` para substituir pelo nome do projeto
- Arquivos sem `/` vão para a raiz do projeto

### Passo 2: Registre no Sistema

Edite `modules/Enums/ProjectType.py` e adicione seu tipo:

```python
class ProjectType(Enum):
    PYTHON = ".py"
    JAVA = ".java"
    # ... outros tipos ...
    
    # Adicione aqui:
    MINHA_API = ".js"  # ou extensão relevante
```

**Importante:** O nome no Enum deve corresponder ao nome do arquivo JSON (em minúsculas).

### Passo 3: Teste

```bash
ps3cli . minha_api meu-projeto
```

### Exemplo Completo: Adicionando Svelte

**1. Crie:** `appdata/Languages/svelte.json`
```json
{
    ".gitignore": "node_modules/\n.svelte-kit/\nbuild/",
    "src/routes/+page.svelte": "<h1>Hello Svelte!</h1>",
    "svelte.config.js": "export default {};",
    "package.json": "{\n  \"name\": \"___PROJECTNAME__\",\n  \"type\": \"module\"\n}"
}
```

**2. Registre:** Em `ProjectType.py`
```python
SVELTE = ".svelte"
```

**3. Use:**
```bash
ps3cli . svelte meu-app-svelte
```

---

## 📚 Exemplo de Uso

```bash
ps3cli . python meu-projeto
```

Cria automaticamente:
```
meu-projeto/
├── src/
│   ├── index.py
│   ├── tool.py
│   └── data.py
├── .gitignore
└── README.md
```

---

## 📖 Casos de Uso

```bash
# Prototipagem rápida
ps3cli . python prototipo-ia

# Projetos em diretórios específicos
ps3cli D:/Projects/Java java sistema-vendas
```

---

## ⚙️ Configuração

Edite `Config.py` para personalizar:

```python
DIRETORIO = Path("D:/MeusProjetos/Python")
DIRETORIO_WEB = Path("D:/MeusProjetos/Web")
BASECODEEDITOR = "vscode"

# Features opcionais (ative manualmente)
HistoryAvaliable = True      # Histórico de projetos criados
READMEAvaliable = True        # Geração automática de README via IA (BETA)
GitAvaliable = False          # Integração com Git
```

---

## 🧪 Features BETA

### 📋 Histórico de Projetos

O ProjectSetup mantém um histórico automático de todos os projetos criados.

**Ativação:**
```python
# Em Config.py
HistoryAvaliable = True
```

**Localização do histórico:**
- **Windows:** `%APPDATA%\PROJECTSETUP-3.O\History\history.json`
- **Linux:** `~/.config/ProjectSetup/PROJECTSETUP-3.O/History/history.json`

**Estrutura do histórico:**
```json
{
  "projects": [
    {
      "name": "meu-projeto",
      "language": "python",
      "path": "D:/Projects/Python/meu-projeto",
      "created_at": "2026-01-13T10:30:00"
    }
  ]
}
```

### 🤖 Geração Automática de README com IA (BETA)

> **⚠️ OBS:** Esta feature ainda **NÃO está integrada no ps3cli**. Por enquanto, a geração de README com IA só funciona através da **interface visual** (`python -m projectsetup3`).

**ATENÇÃO:** Feature em desenvolvimento e requer configuração manual.

#### O que faz?

Gera automaticamente um README.md profissional usando a API do Google Gemini, incluindo badges, descrição, instalação, uso e estrutura do projeto.

#### Configuração

**1. Obtenha uma API Key do Google Gemini**
   - Acesse: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
   - Crie e copie sua chave

**2. Configure o arquivo `.env`**

Crie o arquivo `.env` em `projectsetup3/`:
```env
GEMINI_API_KEY=sua_chave_api_aqui
```

> **⚠️ IMPORTANTE:** O arquivo `.env` deve estar em `ProjectSetup-3.0/projectsetup3/`

**3. Ative a feature no `Config.py`:**
```python
READMEAvaliable = True
```

#### Como Usar

Execute a interface visual:
```bash
python -m projectsetup3
```

Durante a criação do projeto:
1. O sistema pergunta se você quer gerar README automaticamente
2. Você fornece uma breve descrição do projeto
3. A IA gera um README.md completo e profissional

#### Conteúdo Gerado

O README inclui automaticamente:
- Título e badges (linguagem, versão, licença)
- Descrição profissional baseada no seu input
- Seções de funcionalidades, instalação e uso
- Estrutura de pastas e tecnologias
- Guia de contribuição e licença MIT

#### Limitações

⚠️ **Não disponível em builds .exe** - Funciona apenas via código fonte Python  
⚠️ **Modelo padrão:** `gemini-2.5-flash` (personalize em `Services/GeminiClient.py`)

#### Problemas Comuns

**Erro: "GEMINI_API_KEY não encontrada"**
- Confirme que o `.env` está em `projectsetup3/.env`
- Verifique o formato: `GEMINI_API_KEY=sua_chave` (sem aspas)

**Erro: "Resposta vazia do Gemini"**
- Verifique sua conexão com internet
- Valide se a API Key é válida
- Confirme se não excedeu o limite de requisições gratuitas

---

## 🖥️ Launchers Multiplataforma

O ProjectSetup 3.0 inclui scripts de inicialização para Windows e Linux que:

- Detectam e validam Python 3.8+
- Ativam ambiente virtual automaticamente (se existir)
- Instalam dependências automaticamente
- Configuram o ambiente corretamente
- Tratam erros de forma elegante

### 🪟 Windows - `ps3.bat`

**Uso:**
```batch
ps3.bat
```

**O que o script faz:**
1. Detecta a versão do Python instalada
2. Ativa o venv (se existir em `venv/Scripts/activate.bat`)
3. Instala dependências de `projectsetup3/requirements/requirements.txt`
4. Adiciona o módulo ao PYTHONPATH
5. Executa `python -m projectsetup3`
6. Exibe mensagens de erro ou sucesso

**Exemplo de saída:**
```
[INFO] Project root: D:\Projects\Python\ProjectSetup-3.0
[INFO] Python 3.11.0 detectado
[INFO] Ativando venv...
[INFO] Instalando todas dependencias...
[INFO] Iniciando ProjectSetup 3.0...
```

### 🐧 Linux/macOS - `ps3.sh`

**Uso:**
```bash
chmod +x ps3.sh  # Apenas na primeira vez
./ps3.sh
```

**O que o script faz:**
1. Detecta `python3` no PATH
2. Verifica a versão do Python
3. Ativa o venv (se existir em `venv/bin/activate`)
4. Instala dependências via `pip install --user`
5. Instala o pacote local em modo editável (`pip install -e .`)
6. Executa o ProjectSetup
7. Retorna ao diretório original

**Exemplo de saída:**
```
[INFO] Project root: /home/user/ProjectSetup-3.0
[INFO] Python 3.11.0 detectado
[INFO] Usando Python global
[INFO] Instalando todas dependencias de requirements.txt...
[INFO] Iniciando ProjectSetup 3.0...
```

### Recursos

- Validação automática de Python 3.8+
- Suporte a ambientes virtuais (venv)
- Instalação automática de dependências
- Tratamento de erros
- Compatível com Windows, Linux e macOS

### 📝 Personalização

Você pode modificar os scripts para:
- Alterar mensagens
- Adicionar validações customizadas
- Mudar o comportamento de instalação
- Adicionar flags de debug

**Exemplo - Adicionar modo verbose no ps3.sh:**
```bash
# No final do script
if [[ "$1" == "--verbose" ]]; then
  python3 -m projectsetup3 -v
else
  python3 -m projectsetup3 "$@"
fi
```

---

## 🛠️ Comandos

```bash
# Criar projeto
ps3cli <path> <linguagem> <nome>

# Exemplo
ps3cli . python meu-app

# Interface visual
python -m projectsetup3

# Executar com launchers
ps3.bat             # Windows
./ps3.sh            # Linux/macOS
```

### 📊 Visualizando o Histórico

Se `HistoryAvaliable = True` no Config.py:

**Windows:**
```batch
type %APPDATA%\PROJECTSETUP-3.O\History\history.json
```

**Linux/macOS:**
```bash
cat ~/.config/ProjectSetup/PROJECTSETUP-3.O/History/history.json
```
ps3cli list web     # Projetos Web
ps3cli list .       # Diretório atual
```

---

## 🤝 Contribuir

Para adicionar uma linguagem:

1. Fork o projeto
2. Crie `appdata/Languages/sua-linguagem.json`
3. Teste com `ps3cli . sua-linguagem teste`
4. Pull Request

### ⚠️ Nota sobre Builds Executáveis

As features BETA (geração de README com IA e histórico) **não estão disponíveis em builds .exe**. Elas funcionam apenas quando o projeto é executado via código fonte Python.

**Motivo:** Dependências de IA e configurações dinâmicas não são incluídas nas builds compiladas por questões de tamanho e segurança.

Para usar essas features:
1. Clone o repositório
2. Execute via `ps3.bat` (Windows) ou `ps3.sh` (Linux)
3. Ou use `python -m projectsetup3`

---

## 📝 Licença

MIT License

---

## 👤 Autor

**QuittoGames**  
GitHub: [@QuittoGames](https://github.com/QuittoGames)

---

##  Créditos

- [Rich](https://github.com/Textualize/rich) - Interface no terminal
- Comunidade Python

---

<div align="center">

**[🔝 Voltar ao Topo](#-projectsetup-30)**

> **“E tudo o que fizerem, seja em palavra ou em ação, façam em nome do Senhor Jesus.”**  
> — *Colossenses 3:17*

</div>
