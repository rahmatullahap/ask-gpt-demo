# Ask GPT Demo

This repository contains a simple ask gpt with FastAPI application.

## Running the app

1. Install Poetry:

   ```shell
   pipx install poetry

1. Install Dependencies:

    ```shell
    poetry install

1. Set environtment on .env file:

    ```shell
    OPENAI_API_KEY=<YOUR API KEY>

1. Run app:

    ```shell
    uvicorn app.main:app --reload