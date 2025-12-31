from dataclasses import dataclass
from pathlib import Path
import os
import platform
from urllib.parse import quote

@dataclass
class Config:
    modules_local = ["data","modules","Intefaces","Languages","Enums","Class"]
    Debug:str = False

    appdata = Path(os.getenv("APPDATA")) if platform.system().lower() == "windows" else Path.home() / ".config" / "ProjectSetup"
    BASE = Path(__file__).resolve().parent

    basesCodesPath: Path = appdata / "PROJECTSETUP-3.O" / "Languages"

    DIRETORIO: Path = Path("C:/Users/gustavoquitto-ieg/Project/Projects/Python")
    DIRETORIO_WEB: Path = Path("C:/Users/gustavoquitto-ieg/Project/Projects/Web")
    DIRETORIO_CPP: Path = Path("C:/Users/gustavoquitto-ieg/Project/Projects/C++")

    BASECODEEDITOR:str = "vscode"

    GitAvaliable:bool = False  

    HistoryAvaliable:bool = True

    if HistoryAvaliable:baseDiretoryHistory:Path = appdata / "PROJECTSETUP-3.O" / "History"

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
