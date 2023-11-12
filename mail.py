# main.py

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# Email configuration
email_address = "your_email@gmail.com"  # Replace with your email address
email_password = "your_email_password"   # Replace with your email password
smtp_server = "smtp.gmail.com"
smtp_port = 587

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

    # Email content
    subject = "Updated CSV File"
    body = "The CSV file has been updated. See the attached file for details."

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = "abc@c.com"  # Replace with the recipient email address
    msg['Subject'] = subject

    # Attach CSV file
    attachment = MIMEText(csv_content)
    attachment.add_header('Content-Disposition', 'attachment', filename="data.csv")
    msg.attach(attachment)

    # Attach email body
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the email server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, "abc@c.com", msg.as_string())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

