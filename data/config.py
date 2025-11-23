from dataclasses import dataclass ,field

@dataclass
class Config:
    FILES_PROGETS: list = field(default_factory=lambda: ["index", "data", "tool"])

    FILE_COFIG_VSCODE: list = field(default_factory=lambda: ["extetion", "task"])
    
    FILES_PROGETS_WEB: dict = field(default_factory=lambda: {
        "index": ".html",
        "style": ".css",
        "js": ".js"
    })

    DIRETORIO:str = r"D:\Projects\Python"

    DIRETORIO_WEB:str = r"D:\Projects\Web"

    DIRETORIO_CPP:str = r"D:\Projects\C++"
    
    MESAGE_SCRIPT:str = "#Project created successfully!"

    VSCODE_COFIG_CPP:bool = True
