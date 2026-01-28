from dataclasses import dataclass,fields
from pathlib import Path
import os
import platform
from urllib.parse import quote
import json 
from typing import get_args

@dataclass
class Config:
    modules_local = ["data","modules","Intefaces","Languages","Enums","Class"]
    Debug:str = False

    appdata = Path(os.getenv("APPDATA")) if platform.system().lower() == "windows" else Path.home() / ".config" / "ProjectSetup3.0"
    BASE = Path(__file__).resolve().parent

    basesCodesPath: Path = appdata / "Languages"

    @staticmethod
    def _resolve_path(win_path: str) -> Path:
        """
        Function made with IA sorry
        Converte paths do Windows para Linux automaticamente.
        Windows: D:/Projects/Python -> Linux: /mnt/d/Projects/Python ou /media/user/DATA/Projects/Python
        """
        if platform.system() == "Windows":
            return Path(win_path)
        
        # No Linux, procura o ponto de montagem correto
        drive_letter = win_path[0].lower()  # Ex: 'd' de 'D:/Projects'
        rest_path = win_path[3:].replace('\\', '/')  # Remove 'D:/' e normaliza barras
        
        # Possíveis pontos de montagem no Linux
        possible_mounts = [
            Path(f"/mnt/{drive_letter}/{rest_path}"),  # Ex: /mnt/d/Projects/Python
            Path(f"/media/{os.getlogin()}/{drive_letter.upper()}/{rest_path}"),  # Ex: /media/quitto/D/Projects/Python
        ]
        
        # Busca montagens dinâmicas em /run/media
        if Path("/run/media").exists():
            for user_dir in Path("/run/media").iterdir():
                if user_dir.is_dir():
                    for mount in user_dir.iterdir():
                        if mount.is_dir() and mount.name.upper().startswith(drive_letter.upper()):
                            possible_mounts.insert(0, mount / rest_path)
        
        # Retorna o primeiro caminho que existe
        for mount_path in possible_mounts:
            if mount_path.exists() or mount_path.parent.exists():
                return mount_path
        
        # Fallback: usa /mnt como padrão
        return Path(f"/mnt/{drive_letter}/{rest_path}")

    DIRETORIO: Path = _resolve_path("D:/Projects/Python")
    DIRETORIO_WEB: Path = _resolve_path("D:/Projects/Web")
    DIRETORIO_CPP: Path = _resolve_path("D:/Projects/C++")

    BASECODEEDITOR:str = "vscode"

    GitAvaliable:bool = False  

    HistoryAvaliable:bool = True  

    READMEAvaliable:bool = False

    baseDiretoryHistory:Path = appdata / "History"

    Fonts: Path = BASE / "Fonts" if os.path.exists(BASE/ "Fonts") else None

    PROJECT_TYPES = {
        "PYTHON": {
            "files": ["requirements.txt", "pyproject.toml"],
            "extensions": [".py"],
        },
        "JAVA": {
            "files": ["pom.xml", "build.gradle", "build.gradle.kts"],
            "extensions": [".java"],
        },
        "SPRING": {
            "files": ["pom.xml", "build.gradle", "build.gradle.kts", "application.properties", "application.yml"],
            "extensions": [".java"],
        },
        "CSHARP": {
            "files": ["*.csproj", "*.sln"],
            "extensions": [".cs", ".csproj"],
        },
        "JAVASCRIPT": {
            "files": ["package.json"],
            "extensions": [".js"],
        },
        "TYPESCRIPT": {
            "files": ["package.json", "tsconfig.json"],
            "extensions": [".ts"],
        },
        "GO": {
            "files": ["go.mod"],
            "extensions": [".go"],
        },
        "RUST": {
            "files": ["Cargo.toml"],
            "extensions": [".rs"],
        },
        "CPP": {
            "files": ["CMakeLists.txt", "Makefile"],
            "extensions": [".cpp", ".hpp"],
        },
        "C": {
            "files": ["Makefile", "CMakeLists.txt"],
            "extensions": [".c"],
        },
        "SWIFT": {
            "files": ["Package.swift"],
            "extensions": [".swift"],
        },
        "KOTLIN": {
            "files": ["build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"],
            "extensions": [".kt"],
        },
        "RUBY": {
            "files": ["Gemfile"],
            "extensions": [".rb"],
        },
        "PHP": {
            "files": ["composer.json"],
            "extensions": [".php"],
        },
        "DART": {
            "files": ["pubspec.yaml"],
            "extensions": [".dart"],
        },
        "LUA": {
            "files": [],
            "extensions": [".lua"],
        },
        "ROBLOX_LUA": {
            "files": [],
            "extensions": [".luau"],
        },
        "R": {
            "files": ["DESCRIPTION", "renv.lock"],
            "extensions": [".r"],
        },
        "HASKELL": {
            "files": ["stack.yaml", "*.cabal"],
            "extensions": [".hs"],
        },
        "ELIXIR": {
            "files": ["mix.exs"],
            "extensions": [".ex"],
        },
        "SCALA": {
            "files": ["build.sbt"],
            "extensions": [".scala"],
        },
        "PERL": {
            "files": ["cpanfile", "Makefile.PL"],
            "extensions": [".pl"],
        },
        "SHELL": {
            "files": [],
            "extensions": [".sh"],
        },
        "POWERSHELL": {
            "files": [],
            "extensions": [".ps1"],
        },
        "JSON": {
            "files": [],
            "extensions": [".json"],
        },
        "YAML": {
            "files": [],
            "extensions": [".yaml"],
        },
        "MARKDOWN": {
            "files": [],
            "extensions": [".md"],
        },
        "TEX": {
            "files": [],
            "extensions": [".tex"],
        },
        "ASSEMBLY": {
            "files": [],
            "extensions": [".asm"],
        },
        "V": {
            "files": ["v.mod"],
            "extensions": [".v"],
        },
        "ZIG": {
            "files": ["build.zig"],
            "extensions": [".zig"],
        },
        "CRYSTAL": {
            "files": ["shard.yml"],
            "extensions": [".cr"],
        },
        "TOML": {
            "files": [],
            "extensions": [".toml"],
        },
        "INI": {
            "files": [],
            "extensions": [".ini"],
        },
        "DOCKERFILE": {
            "files": ["Dockerfile"],
            "extensions": ["Dockerfile"],
        },
        "MAKEFILE": {
            "files": ["Makefile"],
            "extensions": ["Makefile"],
        },
        "GROOVY": {
            "files": ["build.gradle", "build.gradle.kts"],
            "extensions": [".groovy"],
        },
        "COFFEESCRIPT": {
            "files": ["package.json"],
            "extensions": [".coffee"],
        },
        "ELM": {
            "files": ["elm.json"],
            "extensions": [".elm"],
        },
        "FSHARP": {
            "files": ["*.fsproj", "*.sln"],
            "extensions": [".fs"],
        },
        "OCAML": {
            "files": ["dune", "opam"],
            "extensions": [".ml"],
        },
        "CLOJURE": {
            "files": ["project.clj", "deps.edn"],
            "extensions": [".clj"],
        },
        "HAXE": {
            "files": ["*.hxml"],
            "extensions": [".hx"],
        },
        "RACKET": {
            "files": [],
            "extensions": [".rkt"],
        },
        "SQL": {
            "files": [],
            "extensions": [".sql"],
        },
        "WEB": {
            "files": ["index.html","style.css","js.js","script.js"],
            "extensions": [".html",".css",".js"],
        },
    }

    @staticmethod
    def dispatch_path(typeProject:str) -> Path:
        if typeProject.lower() == "web":
            return Path(Config.DIRETORIO_WEB)
        elif typeProject.lower() == "cpp":
            return Path(Config.DIRETORIO_CPP)
        return Path(Config.DIRETORIO)
    
    @staticmethod
    def get_editor_link(editor: str, project_path: Path) -> str:
        # Normaliza para URI (especialmente no Windows):
        # - caminho absoluto
        # - barras "/" ao invés de "\\"
        # - URL-encoding de espaços e caracteres especiais
        resolved = Path(project_path).expanduser().resolve()
        posix_path = resolved.as_posix()

        if len(posix_path) >= 2 and posix_path[1] == ":":
            posix_path = posix_path[0].lower() + posix_path[1:]

        encoded_path = quote(posix_path, safe="/:=")

        editors = {
            "vscode":   f"vscode://file/{encoded_path}",
            "cursor":   f"cursor://file/{encoded_path}",
            "vscodium": f"vscodium://file/{encoded_path}",
            "sublime":  f"subl://open?url=file://{encoded_path}",
            "pycharm":  f"pycharm://open?file={encoded_path}",
            "idea":     f"idea://open?file={encoded_path}",
            "webstorm": f"webstorm://open?file={encoded_path}",
        }

        return editors.get(editor.lower(), f"vscode://file/{encoded_path}")


    @classmethod  
    def getCofig(cls) -> dict:
        """Carrega configurações do arquivo JSON ou cria padrões"""
        config_dir = cls.appdata / "Config"
        config_file = config_dir / "config.json"

        config_dir.mkdir(parents=True, exist_ok=True)

        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON in config file: {e}")
            except Exception as e:
                print(f"[ERROR] Failed to load config: {e}")
        
        default_config = {
            "Debug": cls.Debug,
            "BASECODEEDITOR": cls.BASECODEEDITOR,
            "GitAvaliable": cls.GitAvaliable,
            "HistoryAvaliable": cls.HistoryAvaliable,
            "READMEAvaliable": cls.READMEAvaliable,
            "DIRETORIO": str(cls.DIRETORIO),
            "DIRETORIO_WEB": str(cls.DIRETORIO_WEB),
            "DIRETORIO_CPP": str(cls.DIRETORIO_CPP)
        }
    
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        
        return default_config

    
    @staticmethod
    def saveConfig(data_local:"Config") -> bool:
        try:
            config_dir = data_local.appdata / "Config"
            config_file = config_dir / "config.json"
            
            config_dir.mkdir(parents=True, exist_ok=True)
            
            dict_Config = {
                "Debug": data_local.Debug,
                "BASECODEEDITOR": data_local.BASECODEEDITOR,
                "GitAvaliable": data_local.GitAvaliable,
                "HistoryAvaliable": data_local.HistoryAvaliable,
                "READMEAvaliable": data_local.READMEAvaliable,
                "DIRETORIO": str(data_local.DIRETORIO),
                "DIRETORIO_WEB": str(data_local.DIRETORIO_WEB),
                "DIRETORIO_CPP": str(data_local.DIRETORIO_CPP)
            }

            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(dict_Config, f, indent=4, ensure_ascii=False)
            return True
        except OSError as E:
            print(f"[ERROR] OSError, Erro: {E}")
            return False
        except Exception as e:
            print(f"[ERROR] Erro ao salvar config: {e}")
            return False
    
    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        kwargs = {}

        for field in fields(cls):
            name = field.name

            if name not in data:
                continue

            value = data[name]
            ftype = field.type

            # Path support
            if ftype == Path or Path in get_args(ftype):
                value = Path(value)

            # int safe cast
            elif ftype == int:
                value = int(value)

            # bool safe cast
            elif ftype == bool:
                value = bool(value)

            kwargs[name] = value

        return cls(**kwargs)