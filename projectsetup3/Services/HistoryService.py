import json
import threading
from pathlib import Path
from projectsetup3.Config import Config

class HistoryService:
    @staticmethod
    def getHistory() -> dict:
        path = Config.baseDiretoryHistory / "history.json"
        if not path.exists():
            return {"projects": []}

        with path.open("r", encoding="UTF-8") as f:
            return json.load(f)


    @staticmethod
    def _write(history: dict):
        path = Config.baseDiretoryHistory / "history.json"
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="UTF-8") as f:
            json.dump(history, f, indent=4)

    @staticmethod
    def run(history: dict):
        threading.Thread(
            target=HistoryService._write,
            args=(history,),
            daemon=True
        ).start()
