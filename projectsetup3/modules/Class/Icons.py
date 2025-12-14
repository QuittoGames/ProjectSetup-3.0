from dataclasses import dataclass

# Nerd Fonts Beta

@dataclass
class Icons:
    @staticmethod
    def getIconMenu(name: str) -> str:
        icons = {
            "new_project": "",
            "modules": "",
            "settings": "",
            "exit": ""
        }
        return icons.get(name, "")
    
    @staticmethod
    def getIconProject(project_type: str) -> str:
        icons = {
            "python": "🐍",
            "web": "🌐",
            "cpp": "⚙️",
            "java": "☕",
            "c#": "🎯",
            "rust": "🦀",
            "javascript": "📜",
            "ruby": "💎",
            "php": "🐘",
            "unity": "🎮",
            "default": "📁"
        }
        return icons.get(project_type.lower(), icons["default"])