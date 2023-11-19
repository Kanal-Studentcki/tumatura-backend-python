import argparse
import os


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(usage="%(prog)s [MODULE]", description="TBD")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version 0.1.0")
    parser.add_argument("module")
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    match args.module:
        case "bot":
            from src.modules.discord_bot import client

            discord_client = client.DiscordClient()
            discord_client.run(os.environ["DISCORD_BOT_TOKEN"])
        case "api":
            from src.modules.api import api

            api.run()

        case _:
            raise ValueError("Unknown module")


if __name__ == "__main__":
    main()
