# main.py

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# Email configuration (same as before)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    # Load the CSV file content
    with open("data.csv", mode="r") as csvfile:
        csv_content = list(csv.reader(csvfile))

    return templates.TemplateResponse("index.html", {"request": request, "csv_content": csv_content})

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

    # Send email with the updated CSV file
    send_email()

    return JSONResponse(content=result, status_code=200)

def send_email():
    # Load the CSV file content
    with open("data.csv", mode="r") as csvfile:
        csv_content = csvfile.read()

    # Email content (same as before)

    # Connect to the email server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, "abc@c.com", msg.as_string())

