import json
import os
import shutil
from pathlib import Path


db_vars = {
    "POSTGRES_USER": "roq-bot",
    "POSTGRES_PASSWORD": os.urandom(32).hex(),
    "POSTGRES_HOST": "postgresql",
    "POSTGRES_DB": "postgres",
}

bot_vars = {
    "DISCORD_TOKEN": "placeholder",
}
bot_vars.update(db_vars)


def main():
    env_dir = Path("env")
    if env_dir.exists():
        shutil.rmtree("./env")
    env_dir.mkdir()

    db_env = Path(env_dir, "db.env")
    bot_env = Path(env_dir, "bot.env")

    file_config_map = {
        db_env: [db_vars],
        bot_env: [bot_vars],
    }

    for file, config in file_config_map.items():
        with file.open("w") as f:
            for settings in config:
                for k, v in settings.items():
                    f.write(f"{k}={v if not isinstance(v, list) else json.dumps(v)}\n")
                f.write("\n")


if __name__ == "__main__":
    main()
