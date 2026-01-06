# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

block_cipher = None

# Diretório base do projeto
base_dir = Path(SPECPATH)

# Coletar todos os arquivos de dados necessários
datas = [
    # Incluir pasta appdata com todos os arquivos JSON de linguagens
    (str(base_dir / 'appdata'), 'appdata'),
    # Incluir pasta Fonts
    (str(base_dir / 'Fonts'), 'Fonts'),
    # Incluir LICENSE se necessário
    (str(base_dir / 'LICENSE'), '.'),
]

# Coletar todos os módulos Python
hiddenimports = [
    'rich',
    'rich.console',
    'rich.panel',
    'rich.text',
    'rich.box',
    'rich.table',
    'rich.tree',
    'rich.padding',
    'rich.align',
    'projectsetup3',
    'projectsetup3.cli',
    'projectsetup3.Config',
    'projectsetup3.tool',
    'projectsetup3.index',
    'projectsetup3.Services',
    'projectsetup3.Services.ArrowsService',
    'projectsetup3.Services.CLIService',
    'projectsetup3.Services.ProjectManagerService',
    'projectsetup3.modules',
    'projectsetup3.modules.Class',
    'projectsetup3.modules.Class.BaseProject',
    'projectsetup3.modules.Class.Icons',
    'projectsetup3.modules.Enums',
    'projectsetup3.modules.Enums.ProjectType',
]

a = Analysis(
    ['run.py'],
    pathex=[str(base_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ProjectSetup3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Adicione um ícone .ico aqui se desejar
)
