# Building a FastAPI application with Python

from fastapi import FastAPI

# Creat an instance of the FastAPI application
app = FastAPI()

# Study different API methods
@app.get("/") # means defining the root for the API (URL)
def home():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/about")
def about():
    return {
        "course": "Python Full Stack developer",
        "instructor": "Josh",
        "description": "This course covers Python programming, web development, and more."
    }