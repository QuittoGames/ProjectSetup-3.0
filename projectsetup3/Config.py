from dataclasses import dataclass
from pathlib import Path
import os
import platform

@dataclass
class Config:
    modules_local = ["data","modules","Intefaces","Languages","Enums","Class"]
    Debug:str = False

    appdata = Path(os.getenv("APPDATA")) if platform.system().lower() == "windows" else Path.home() / ".config" / "ProjectSetup"
    BASE = Path(__file__).resolve().parent

    basesCodesPath: Path = appdata / "PROJECTSETUP-3.O" / "Languages"

    DIRETORIO: Path = Path("D:/Projects/Python")
    DIRETORIO_WEB: Path = Path("D:/Projects/Web")
    DIRETORIO_CPP: Path = Path("D:/Projects/C++")

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
    
    def get_editor_link(editor: str, project_path: Path) -> str:
        editors = {
            "vscode":   f"vscode://file/{project_path}",
            "cursor":   f"cursor://file/{project_path}",
            "vscodium": f"vscodium://file/{project_path}",
            "sublime":  f"subl://open?url=file://{project_path}",
            "pycharm":  f"pycharm://open?file={project_path}",
            "idea":     f"idea://open?file={project_path}",
            "webstorm": f"webstorm://open?file={project_path}",
        }

        return editors.get(editor.lower(), f"vscode://file/{project_path}")
