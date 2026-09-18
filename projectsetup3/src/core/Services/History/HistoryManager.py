from dataclasses import dataclass
from pathlib import Path
from projectsetup3.src.core.models.History import History
import datetime


@dataclass
class HistoryManager:
    def add_History(
        self,
        name: str,
        language,
        gitRepoLink: str | None,
        project_path: Path,
    ) -> None:
        history = History.getHistory()
        history["projects"].append(
            {
                "name": name,
                "language": language.value if language else None,
                "path": str(project_path.resolve()),
                "git": bool(gitRepoLink),
                "gitRepo": gitRepoLink,
                "created_at": datetime.datetime.now().isoformat(),
            }
        )

        History.run(history)
