import json
import shutil
from pathlib import Path
import os

db_name = os.urandom(32).hex()

db_vars = {
    "DB_NAME": f"{db_name}.db",
    "SQLITE_URI": f"sqlite+aiosqlite:///./db/{db_name}.db",
}

bot_vars = {
    "DISCORD_TOKEN": "placeholder",
    "PREFIX": "&",
    "SNIPE_CACHE_SIZE": 8,
    "GUILD_ID": -1,
    "DEFAULT_COGS": ["abc", "xyz"],
    "ADMIN_ROLES": [-1, -1],
    "GAG_ROLES": {"ball": -1, "uwu": -1},
    "BADWORDS_ROLE": -1,
    "PEACE_ROLE": -1,
    "SUB_ROLE": -1,
    "DOM_ROLE": -1,
    "SWITCH_ROLE": -1,
    "TECH_ROLE": -1,
    "TECH_CHANNEL": -1,
    "NOSPEECH_ROLE": -1,
    "NONSFW_ROLE": -1,
    "NOMEDIA_ROLE": -1,
    "NOREACTIONS_ROLE": -1,
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
                    f.write(
                        f"{k}={v if not isinstance(v, list) or not isinstance(v, dict) else json.dumps(v)}\n"
                    )
                f.write("\n")


if __name__ == "__main__":
    main()
