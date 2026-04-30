# Building a FastAPI application with Python

import os
from fastapi import FastAPI, Response

# Create an instance of the FastAPI application
app = FastAPI()

@app.get("/") # Define a route for the root URL
def home():
    return {"message": "Welcome to the FastAPI application!",
            "swagger ui": "/docs",
            "endpoints": ["/about", "/csv"]}

@app.get("/about") # Define a route/endpoint for the /about URL
def about():
    return {
        "course" : "Python Full Stack Developer",
        "instructor" : "Jo$h",
        "description" : "Learn Python programming from scratch to building full-stack applications."
    }

@app.get("/csv")
def csv():
    csv_content = "name,age,city\nAlice,30,New York\nBob,25,Los Angeles\nCharlie,35,Chicago"
    return Response(content=csv_content, media_type="text/plain")



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )