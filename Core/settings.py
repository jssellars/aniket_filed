import json
import os


env = os.environ.get("PYTHON_ENV") or "local"
config_file = f"Config/Settings/app.settings.{env}.json"

with open(config_file) as f:
    config_as_dict = json.load(f)

if not isinstance(config_as_dict, dict):
    raise ValueError('Invalid app config JSON.')
