from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import sys
import io
import os

# Create an instance of InteractiveShell
app = FastAPI()

subDir = os.environ.get('NOTEBOOK_NAME')
os.makedirs(subDir, exist_ok=True)
os.chdir(subDir)

shell = InteractiveShell.instance()

class Cell(BaseModel):
    code: str

class Output(BaseModel):
    result: str
    stdout: str

@app.post("/run")
async def run(cell: Cell):
    running_code = cell.code

    with capture_output() as captured:
        # runs !pip install <pkg>
        result = shell.run_cell(running_code)

    return Output(
        result = str(result.result),
        stdout = captured.stdout
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print("here")
    print(os.path.join('./', file.filename))
    file_path = os.path.join('./', file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return { "filename": file.filename, "saved_to": file_path }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
