# main.py

from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# Email configuration (same as before)

# Initialize Jinja2Templates with the 'templates' directory
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    # Load the CSV file content
    with open("data.csv", mode="r") as csvfile:
        csv_content = list(csv.reader(csvfile))

    return templates.TemplateResponse("index.html", {"request": request, "csv_content": csv_content})

# ...

from fastapi import HTTPException, status

# ...

@app.post("/submit")
async def submit_form(input1: str = Form(...), input2: str = Form(...)):
    # Process the inputs
    result = {"input1": input1, "input2": input2}

    # Store the inputs in a CSV file
    with open("data.csv", mode="a", newline="") as csvfile:
        fieldnames = ["input1", "input2"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the CSV file is empty and write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the input values to the CSV file
        writer.writerow({"input1": input1, "input2": input2})

    # Redirect back to the main page after submitting the form
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# ...




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
