import json
import os

from src.api.main import app  # Absolute import

# Get the OpenAPI schema using app from src.api.main
openapi_schema = app.openapi()

# Write to file in the correct relative location
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
