from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import sys
import io
import os
import subprocess

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open('index.html', 'r') as file:
        content = file.read()
    return content

@app.get("/index.js", response_class=HTMLResponse)
async def index():
    with open('index.js', 'r') as file:
        content = file.read()
    return content

@app.post("/new-notebook", response_class=HTMLResponse)
async def new_notebook(
    notebook_name: str = Form(...),
):
    command = ['python', 'notebook.py']
    os.makedirs(notebook_name, exist_ok=True)
    env = os.environ.copy()
    env['NOTEBOOK_NAME'] = notebook_name
    process = subprocess.Popen(command, env=env)

    with open('notebook.html', 'r') as file:
        content = file.read()
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
