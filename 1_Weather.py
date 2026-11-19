
from pathlib import Path
import runpy

app_file = Path(__file__).with_name("app.py")

if not app_file.exists():
    raise FileNotFoundError("app.py not found in repository root")

runpy.run_path(str(app_file), run_name="__main__")
