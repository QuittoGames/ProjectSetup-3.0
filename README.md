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

- ⚡ Poupa tempo na criação de projetos novos
- 📁 Estrutura organizada desde o início
- 🎨 Templates personalizáveis via JSON
- 🌍 Suporte para 40+ linguagens
- 💻 Interface visual no terminal
- 🖥️ Launchers multiplataforma (Windows & Linux)
- 📜 Histórico automático de projetos criados
- 🤖 Geração inteligente de README com IA (BETA)

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
<summary><b>🔥 Linguagens Populares</b></summary>

- 🐍 **Python** - requirements.txt, src/, .gitignore
- 🟨 **JavaScript** - package.json, node_modules/, ESLint
- 🔷 **TypeScript** - tsconfig.json, dist/, tipos
- ☕ **Java** - Maven/Gradle, src/main/java/
- 🦀 **Rust** - Cargo.toml, src/main.rs
- 🐹 **Go** - go.mod, estrutura idiomática
- 💎 **Ruby** - Gemfile, estrutura Rails
- 🐘 **PHP** - composer.json, Laravel/Symfony
- 🍎 **Swift** - Package.swift, iOS/macOS
- 🟣 **C#** - .csproj, .sln, .NET
- ➕ **C/C++** - CMakeLists.txt, Makefile

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

## 📚 Exemplos Rápidos

### Python

```bash
ps3cli . python data-science
```
```
data-science/
├── src/
│   ├── index.py
│   ├── tool.py
│   └── data.py
├── .gitignore
└── README.md
```

### JavaScript/Node.js

```bash
ps3cli . javascript minha-api
```
```
minha-api/
├── index.js
├── package.json
└── .gitignore
```

### TypeScript

```bash
ps3cli . typescript react-app
```
```
react-app/
├── src/
│   └── index.ts
├── package.json
├── tsconfig.json
└── .gitignore
```

### Rust

```bash
ps3cli . rust cli-tool
```
```
cli-tool/
├── src/
│   └── main.rs
├── Cargo.toml
└── .gitignore
```

---

## 📖 Casos de Uso

**Prototipagem:**
```bash
ps3cli . python prototipo-ia
```

**Projetos maiores:**
```bash
ps3cli D:/Projects/Java java sistema-vendas
```

**Aprendizado:**
```bash
ps3cli . rust aprendendo-rust
```

**Scripts:**
```bash
ps3cli . python automacao
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

**⚠️ ATENÇÃO:** Esta feature está em **BETA** e requer configuração manual.

#### Como Funciona

O ProjectSetup pode gerar automaticamente um README.md profissional usando a API do Google Gemini.

#### Requisitos

1. **API Key do Google Gemini**
   - Obtenha sua chave em: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. **Arquivo `.env` configurado**

#### Configuração Passo a Passo

**1. Ative a feature no `Config.py`:**
```python
READMEAvaliable = True
```

**2. Crie o arquivo `.env` dentro da pasta `projectsetup3/`:**

> **⚠️ OBS IMPORTANTE:** O arquivo `.env` deve estar localizado em:  
> `ProjectSetup-3.0/projectsetup3/.env`

**3. Adicione sua API Key no `.env`:**
```env
GEMINI_API_KEY=sua_chave_api_aqui
```

**Exemplo de `.env`:**
```env
# Google Gemini API Configuration
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Como Usar

Quando você cria um projeto com esta feature ativa, o sistema:

1. Pergunta se você quer gerar um README automaticamente
2. Solicita uma breve descrição do projeto
3. Usa a IA para gerar um README.md completo e profissional

**Exemplo de uso:**
```bash
ps3cli . python meu-projeto-ia
# Sistema pergunta: "Gerar README automaticamente? (s/n)"
# Você responde: s
# Sistema pergunta: "Descreva seu projeto:"
# Você responde: "Uma API REST para gerenciar tarefas"
# README.md é gerado automaticamente!
```

#### Conteúdo Gerado

O README gerado inclui:
- ✅ Título com emoji
- ✅ Badges (linguagem, versão, licença)
- ✅ Descrição profissional
- ✅ Seção de funcionalidades
- ✅ Instalação e uso
- ✅ Estrutura de pastas
- ✅ Tecnologias utilizadas
- ✅ Como contribuir
- ✅ Licença MIT

#### Limitações

⚠️ **Esta feature NÃO está disponível em builds .exe**  
Apenas funciona quando executado via Python source code.

**Modelos disponíveis:**
- Padrão: `gemini-2.5-flash`
- Personalize em: `Services/GeminiClient.py`

#### Troubleshooting

**Erro: "GEMINI_API_KEY não encontrada no .env"**
- Verifique se o arquivo `.env` está em `projectsetup3/.env`
- Confirme que a chave está no formato: `GEMINI_API_KEY=sua_chave`
- Não use aspas na chave

**Erro: "Resposta vazia do Gemini"**
- Verifique sua conexão com a internet
- Confirme que a API Key é válida
- Verifique se não excedeu o limite de requisições

---

## 🖥️ Launchers Multiplataforma

O ProjectSetup 3.0 inclui scripts de inicialização para Windows e Linux que:

- ✅ Detectam e validam Python 3.8+
- ✅ Ativam ambiente virtual automaticamente (se existir)
- ✅ Instalam dependências automaticamente
- ✅ Configuram o ambiente corretamente
- ✅ Tratam erros de forma elegante

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

### 🔧 Recursos dos Launchers

**Tratamento de Erros:**
- Validação de Python instalado
- Verificação de arquivos necessários
- Mensagens claras de erro
- Códigos de saída apropriados

**Flexibilidade:**
- Funciona com ou sem venv
- Instala dependências automaticamente
- Mantém o contexto do diretório do usuário

**Cross-platform:**
- `ps3.bat` - Windows (NT/10/11)
- `ps3.sh` - Linux, macOS, WSL, Git Bash

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

## 🛠️ Comandos Úteis

```bash
# Criar projeto
ps3cli <path> <linguagem> <nome> [git-repo]

# Exemplos
ps3cli . python meu-app                    # No diretório atual
ps3cli D:/Projects python meu-app          # Path específico
ps3cli . python app https://github.com/... # Com Git

# Ver todas as linguagens
python -m projectsetup3

# Listar projetos existentes
ps3cli list py      # Projetos Python
ps3cli list web     # Projetos Web
ps3cli list .       # Diretório atual

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
