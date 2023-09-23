from dotenv import load_dotenv

from pb24exporter.cli import cli

if __name__ == "__main__":
    load_dotenv()
    cli()
