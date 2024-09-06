import os
import secrets
import string

import requests
import typer
import yaml
from rich import print
from typing_extensions import Annotated

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
users_app = typer.Typer()
sentence_app = typer.Typer()
app.add_typer(
    users_app, name="user", short_help="User commands", help="Commands to work with users",
)
app.add_typer(
    sentence_app, name="sentence", short_help="Sentence commands", help="Commands to work with sentences"
)


def _read_config():
    name = "cli_config.yaml"
    if not os.path.exists(name):
        print(f"Config file not found, please create `{name}` in the current directory")
        raise typer.Abort()
    with open(name, 'r') as f:
        return yaml.safe_load(f)


def _request(method, path, success_msg, err_msg, json=None, data=None, config=_read_config()):
    response = requests.request(
        method,
        config["host"] + path,
        json=json,
        data=data,
        headers=_headers(config),
    )
    if response.status_code != 200:
        print(f"{err_msg}: {response.status_code} {response.text}")
        raise typer.Abort()
    if success_msg:
        print(success_msg)
    return response


def _headers(config):
    if not (username := config["admin_username"]):
        print("Admin username not found in config")
        raise typer.Abort()
    if not (password := config["admin_password"]):
        print("Admin password not found in config")
        raise typer.Abort()
    response = requests.post(
        config["host"] + "/user/authorize",
        json={"username": username, "password": password},
    )
    if response.status_code != 200:
        print(f"Error authorizing user, check username and password: {response.status_code} {response.text}")
        raise typer.Abort()

    return {
        "Authorization": f"Bearer {response.json()['access_token']}",
        "Content-Type": "application/json",
    }


def _generate_strong_password(length=32):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


@users_app.command("create")
def create_user(
        username: Annotated[str, typer.Option("--username", "-u", help="Username to create")] = None,

        password: Annotated[str, typer.Option("--password", "-p",
                                              help="Password to create. If not provided, will be generated")] = None,
        confirm: Annotated[bool, typer.Option("--yes", "-y", help="Skip confirmation")] = False
):
    """
    Create a new user with provided username and password
    """
    username = username or typer.prompt("Enter username")
    if not password:
        password = _generate_strong_password()
        print(
            f"Generated strong password:\n\n[bold]{password}[/bold]\n\n"
            f"use [italic]-p[/italic] or [italic]--password[/italic] to set your own password"
        )

    if not (
            confirm
            or
            typer.confirm(f"Create user `{username}` with password `{password}`?", default=True, abort=True)
    ):
        raise typer.Abort()

    _request(
        "post",
        "/user/create",
        json={"username": username, "password": password},
        success_msg=f"Created user `{username}`",
        err_msg="Error creating user"
    )


@users_app.command("report")
def get_user_report(username: Annotated[str, typer.Argument(help="Username to get report")] = None):
    """
    Get user report by username
    """
    username = username or typer.prompt("Enter username")
    response = _request(
        "get",
        f"/user/report/{username}",
        success_msg=None,
        err_msg="Error getting user report"
    )
    print(response.json())


@users_app.command("reward")
def reward_user(
        username: Annotated[str, typer.Option("--username", "-u", help="User to reward")] = None,
        amount: Annotated[int, typer.Option("--amount", "-a", help="Amount to reward")] = None,
        confirm: Annotated[bool, typer.Option("--yes", "-y", help="Skip confirmation")] = False
):
    """
    Reward user with provided amount
    """
    username = username or typer.prompt("Enter username")
    amount = amount or typer.prompt("Enter amount", type=int)
    if amount < 1:
        raise typer.BadParameter("Amount should be greater than 0")

    if not (
            confirm
            or
            typer.confirm(f"Reward user `{username}` with {amount}?", default=True, abort=True)
    ):
        raise typer.Abort()

    _request(
        "post",
        f"/user/paid/",
        json={"amount": amount, "username": username},
        success_msg=f"Rewarded user `{username}` with {amount}",
        err_msg="Error rewarding user"
    )


@sentence_app.command("ls")
def list_sentences(
        reviewer: Annotated[str, typer.Option("--reviewer", "-r", help="Filter by reviewer's username")] = None,
        error_type: Annotated[str, typer.Option("--error-type", "-e", help="Filter by error type")] = None,
        include_all: Annotated[bool, typer.Option("--all", "-a", help="Enable to include all sentences")] = False,
        today: Annotated[bool, typer.Option("--today", "-t", help="Enable to filter by today's sentences")] = False
):
    """
    List sentences with optional filters
    """
    response = _request(
        "get",
        "/sentence/json",
        json={
            "by_reviewer": reviewer,
            "error_type": error_type,
            "include_all": include_all,
            "today": today
        },
        success_msg=None,
        err_msg="Error getting sentences"
    )
    print(response.json())


@sentence_app.command("get")
def sentence_by_id(id: Annotated[int, typer.Argument(help="Sentence id to retrieve")] = None):
    """
    Get sentence by id
    """
    id = id or typer.prompt("Enter sentence id", type=int)
    response = _request(
        "get",
        f"/sentence/{id}",
        json=None,
        success_msg=None,
        err_msg="Error getting sentence"
    )
    print(response.json())


@sentence_app.command("add")
def add_sentence(
        path: Annotated[str, typer.Argument(help="Path to JSON file with sentences")] = "sentences.json"
):
    """
    Upload sentences from JSON file to the platform
    """
    if not os.path.exists(path):
        print(f"File with sentences is not found by path `{path}`")
        raise typer.Abort()
    else:
        with open(path, "r") as f:
            _request(
                "post",
                "/sentence",
                json=None,
                data=f,
                success_msg="Sentences added",
                err_msg="Error adding sentences"
            )


if __name__ == "__main__":
    app()
