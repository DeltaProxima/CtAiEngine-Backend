from fastapi import FastAPI, File, UploadFile, HTTPException,Depends,Form
from typing import List, Optional
import uuid
import aiofiles
from agent import *
from prompt import road_walkability_prompt
from sqlalchemy.orm import sessionmaker,Session
from database import Base, SessionLocal
from models import RoadImages
import sqlite3
import base64
import httpx
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
async def upload_image(lat: str=Form(...), long: str=Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Generate a unique filename
    file_extension = file.filename.split(".")[-1]
    file.filename = str(uuid.uuid4())+"." + file_extension
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    
    # Save the uploaded file
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Save the image to the database
    image = RoadImages(road_image=file.filename, latitude=lat, longitude=long)
    db.add(image)
    db.commit()
    db.refresh(image)
    
    return {"filename": file.filename, "latitude": lat, "longitude": long}

