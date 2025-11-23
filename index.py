from tool import tool
import asyncio
from pathlib import Path
from Config import Config
from modules.Languages.PythonProject import PythonProject

data_local = Config()

def Start():
    tool.menu()
    print("test")
    Projecttest = PythonProject(special=False)
    Projecttest.openBaseCodeJson()
    Projecttest.create(Path(r"D:\Projects\Python\ProjectSetup-3.0\test"))

async def main():
    try:
        from Config import Config
        data_local = Config()

        await tool.add_path_modules(Config.modules_local)
        if data_local.Debug:
            tool.verify_modules()
    except StopAsyncIteration as E:
        print(f"[ERROR] Erro StopAsycnInteration, Erro: {E}")

if __name__ == "__main__":
    asyncio.run(main())
    Start()     