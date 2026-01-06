# Uso Das Nerd Fonts Na Aplciaçao

## 🇧🇷 Português (Brasil)
---

## 🐧 Linux — Aplicando a fonte via código

Em ambientes Linux, alguns terminais avançados (como **Kitty**, **Alacritty**, **WezTerm**) permitem que o Rich carregue fontes externas através do parâmetro `font=`.

### Como usar no Linux

Se o diretório `Fonts` existir:

```python
from rich.console import Console
from config import Config

console = Console(font=str(Config.Fonts / "UbuntuSansNerdFont-Regular.ttf"))
```

O Rich tentará renderizar o texto usando a fonte fornecida pelo arquivo.

### Requisitos

* Terminal Linux deve suportar fonte embutida
* Fonte Nerd Font deve estar instalada ou disponível no diretório `Fonts`

---

## Windows — Fonte deve ser configurada no terminal

No Windows, **nenhum código Python consegue mudar a fonte do terminal**.
O parâmetro `font=` do Rich **não funciona** em Windows Terminal, CMD ou PowerShell.

### Como usar no Windows

Você deve configurar a fonte manualmente:

1. Abra **Windows Terminal**
2. Vá em **Configurações**
3. Escolha o perfil (PowerShell, CMD etc.)
4. Acesse a aba **Aparência**
5. Selecione a fonte:

```
UbuntuSans Nerd Font
```

6. Salve e reinicie o terminal

Depois disso, seus ícones Nerd Font aparecerão normalmente no Rich.

---

## 🧩 Sobre o `Config.Fonts`

Seu `Config.py` localiza automaticamente o diretório `Fonts` se ele existir:

```python
Fonts: Path = BASE / "Fonts" if os.path.exists(BASE / "Fonts") else None
```

Use assim para passar para o Rich no Linux:

```python
Console(font=str(Config.Fonts / "UbuntuSansNerdFont-Regular.ttf"))
```

No Windows, apenas ignore o parâmetro `font=` e deixe o terminal exibir os glifos.

---

# 🇺🇸 English Version

This document explains how to configure Nerd Fonts with the Python `Rich` library, depending on whether you are using **Linux** or **Windows**.

---

## 🐧 Linux — Apply the font programmatically

On Linux, some advanced terminals (like **Kitty**, **Alacritty**, **WezTerm**) allow Rich to load external font files using the `font=` parameter.

### Usage on Linux

If the `Fonts` directory exists:

```python
from rich.console import Console
from config import Config

console = Console(font=str(Config.Fonts / "UbuntuSansNerdFont-Regular.ttf"))
```

Rich will try to render text using that font file.

### Requirements

* Terminal must support embedded fonts
* The Nerd Font file must be installed or available in the `Fonts` directory

---

## 🪟 Windows — Font must be set in the terminal

On Windows, **no Python code can change the terminal font**.
The Rich `font=` argument **does not work** in Windows Terminal, CMD, or PowerShell.

### ✔️ How to use Nerd Fonts on Windows

You must set the font manually:

1. Open **Windows Terminal**
2. Go to **Settings**
3. Select your profile (PowerShell, CMD, etc.)
4. Open **Appearance**
5. Select the font:

```
UbuntuSans Nerd Font
```

6. Save and restart the terminal

After that, Nerd Font icons will display correctly in Rich.

---

## About `Config.Fonts`

Your `Config.py` locates the `Fonts` directory automatically:

```python
Fonts: Path = BASE / "Fonts" if os.path.exists(BASE / "Fonts") else None
```

Use it like this on Linux:

```python
Console(font=str(Config.Fonts / "UbuntuSansNerdFont-Regular.ttf"))
```

On Windows, just ignore the `font=` parameter—you must set the font on the terminal itself.

---

Se quiser, posso adicionar exemplos ou uma seção de troubleshooting.

---

## 📘 Uso de Logos e Ícones — Project Setup 3

### 🇧🇷 Instruções para o usuário

O **Project Setup 3** utiliza ícones Nerd Fonts para melhorar a interface visual no terminal. Para que tudo funcione corretamente:

### Como usar os ícones

* Os ícones exibidos nos menus e logs vêm de fontes **Nerd Fonts**.
* Eles só aparecem corretamente se o terminal estiver usando uma fonte compatível.

### 🐧 Linux

* O programa pode aplicar a fonte automaticamente via código quando o terminal permite.
* Se o seu terminal não suportar fontes embutidas, instale a Nerd Font no sistema.

### 🪟 Windows

* No Windows, o programa **não consegue mudar a fonte do terminal automaticamente**.
* O usuário precisa configurar manualmente a fonte Nerd Font no Windows Terminal.

### ✔️ Depois de configurar a fonte

* Todos os ícones (como os usados nos menus: "", "", etc.) vão aparecer corretamente.
* Nada adicional precisa ser feito pelo usuário dentro do Project Setup 3.

---

## 🇺🇸 Icons & Logo Usage — Project Setup 3

### English instructions for users

**Project Setup 3** uses Nerd Font icons to improve terminal UI. For them to display correctly:

### How icon rendering works

* Icons come from **Nerd Fonts**.
* They only display correctly if your terminal uses a Nerd Font.

### 🐧 Linux

* Some terminals allow the program to load fonts automatically.
* Otherwise, install a Nerd Font in your Linux system.

### 🪟 Windows

* Windows terminals **cannot** be changed programmatically.
* You must manually set a Nerd Font in Windows Terminal.

### ✔️ After setup

* All icons ("", "", etc.) will appear normally.
* No extra steps are required inside Project Setup 3.
