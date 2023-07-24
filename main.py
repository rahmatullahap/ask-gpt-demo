import os
import uvicorn
import pytest


def start():
    """Launched with `poetry run start` at root level"""
    port = int(os.environ.get('PORT')) if os.environ.get('PORT') is not None else 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

def test():
    pytest.main(["-v", "-s", "--capture=no"])
