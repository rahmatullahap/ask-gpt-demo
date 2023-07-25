# Ask GPT Demo

This repository contains a simple ask gpt with FastAPI application.

## Running the app

1. Install Poetry:

   ```shell
    pipx install poetry

1. Install Dependencies:

    ```shell
    poetry install
    poetry env use python3.9.6
    poerty env use /Users/pranatadesta/.pyenv/versions/3.9.6/bin/python3.9

1. Set environtment on .env file:

    ```shell
    OPENAI_API_KEY=<YOUR API KEY>

1. Run app:

    ```shell
    poetry run start

1. Test app:

    ```shell
    poetry run pytest