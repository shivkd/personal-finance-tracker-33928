import json
import sys
from pathlib import Path

# Try to ensure src is in sys.path for CLI execution as __main__ (not just module)
src_path = Path(__file__).resolve().parents[2] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from src.api.main import app  # Absolute import for Docker, CLI-safe
except ModuleNotFoundError as e:
    # Fallback: try relative import if running in "src/api" directly (not expected for Docker)
    if __package__ is None and Path.cwd().name == "api":
        from main import app
    else:
        raise e

# Get the OpenAPI schema using app from src.api.main
openapi_schema = app.openapi()

# Write to file in the correct relative location (always relative to backend root)
output_dir = Path(__file__).resolve().parents[2] / "interfaces"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "openapi.json"

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
