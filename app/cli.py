from fastapi_cli.cli import app, dev


@app.command()
def main(name: str):
    dev()
