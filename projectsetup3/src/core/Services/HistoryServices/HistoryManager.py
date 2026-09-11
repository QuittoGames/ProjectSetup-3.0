from dataclasses import dataclass
from pathlib import Path
from core.Services.egine.HistoryServices.History import History
import datetime

@dataclass
class HistoryManager:
    def add_History(self,name:str,gitRepoLink:Path,project_path:Path) -> None:
        history = History.getHistory()
        history["projects"].append({
            "name": name,
            "language": self.language.value if self.language else None,
            "path": str(project_path.resolve()),
            "git": bool(gitRepoLink),
            "gitRepo": gitRepoLink,
            "created_at": datetime.datetime.now().isoformat()
        })

        History.run(history)
