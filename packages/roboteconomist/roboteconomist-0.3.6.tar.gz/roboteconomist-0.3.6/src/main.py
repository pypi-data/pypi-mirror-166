import typer
from rich import print

from src.auditor import Auditor

app = typer.Typer()


def get_outcome_from_user() -> str:

    print("[bold red]Please describe your outcome. For example, you might type: ")  # noqa: E501
    print("- [green] research [/green]")
    print("- [green] political participation [/green]")
    print("- [green] trade volume [/green]")
    print("- [green] college graduation rates [/green]")
    return typer.prompt("Please describe your outcome ")


def get_instrument_from_user() -> str:
    print("[bold red]Please describe your instrument. For example, you might type: ")  # noqa: E501
    print("- [green] weather [/green]")
    print("- [green] election day rain [/green]")
    print("- [green] draft lottery [/green]")
    print("- [green] judge fixed effects [/green]")
    return typer.prompt("Please describe your instrument ")


@app.command()
def IV() -> None:

    proposed_instrument: str = get_instrument_from_user()
    proposed_outcome: str = get_outcome_from_user()

    graph_spec: str = "src/dags/nber.rulebased.extractions.jsonl.nxdigraph.json"
    auditor = Auditor(graph_specification=graph_spec)
    auditor.search_for_iv_violations(proposed_instrument=proposed_instrument,
                                     proposed_outcome=proposed_outcome)


if __name__ == "__main__":

    app()
