# main.py

from fastapi import FastAPI
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import csv

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}


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

    return JSONResponse(content=result, status_code=200)

