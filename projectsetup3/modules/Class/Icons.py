from dataclasses import dataclass

# Nerd Fonts Beta

@dataclass
class Icons:
    @staticmethod
    def getIconMenu(name: str) -> str:
        icons = {
            "new_project": "",
            "modules": "",
            "settings": "",
            "exit": ""
        }
        return icons.get(name, "")