from tool import tool
import asyncio
from pathlib import Path
from Config import Config
from modules.Languages.PythonProject import PythonProject

data_local = Config()

def Start():
    tool.menu()
    print("test")
    Projecttest = PythonProject()
    Projecttest.openBaseCodeJson()
    Projecttest.create(Path(r"D:\Projects\Python\ProjectSetup-3.0\test"), "test")

async def main():
    try:
        from Config import Config
        data_local = Config()

        await tool.add_path_modules(data_local)
        if data_local.Debug:
            await tool.verify_modules()
    except StopAsyncIteration as E:
        print(f"[ERROR] Erro StopAsycnInteration, Erro: {E}")

if __name__ == "__main__":
    asyncio.run(main())
    Start()     