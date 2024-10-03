from fastapi import FastAPI, File, UploadFile, HTTPException,Depends,Form
from typing import List, Optional
import uuid
import aiofiles
from agent import model
from prompt import road_walkability_prompt
from langchain_core.messages import HumanMessage
from sqlalchemy.orm import sessionmaker,Session
from database import Base, SessionLocal
from models import RoadImages
import sqlite3
import httpx
import base64
import os



app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_FOLDER = "./uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/upload-image/")
async def upload_image( file: UploadFile ,lat: str=Form(...), long: str=Form(...), db: Session = Depends(get_db)):
    # Generate a unique filename
    file_extension = file.filename.split(".")[-1]
    file.filename = str(uuid.uuid4())+"." + file_extension
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"

    # extract content out of the file
    data = await file.read()
    image_data = base64.b64encode(data).decode("utf-8")    
    # Save the uploaded file
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Save the image to the database
    image = RoadImages(road_image=file.filename, latitude=lat, longitude=long)
    db.add(image)
    db.commit()
    db.refresh(image)

    # Asking GPT to desribe the image
    message = HumanMessage(
        content=[
            {"type": "text", "text": "describe the road quality in this image"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    response = model.invoke([message])
    
    return {"filename": file.filename, "latitude": lat, "longitude": long, "response": response.content}

