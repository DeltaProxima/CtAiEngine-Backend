from fastapi import FastAPI, File, UploadFile, HTTPException,Depends,Form
from typing import List, Optional
import uuid
import aiofiles
from agent import model, parser
from prompt import road_walkability_prompt
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.orm import sessionmaker,Session
from database import Base, SessionLocal
from models import RoadImages
import json
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
    # # Save the uploaded file
    # async with aiofiles.open(file_location, 'wb') as out_file:
    #     content = await file.read()
    #     await out_file.write(content)

    # Save the image to the database
    # image = RoadImages(road_image=file.filename, latitude=lat, longitude=long)
    # db.add(image)
    # db.commit()
    # db.refresh(image)

    # Asking GPT to desribe the image
    system_message = SystemMessage(content=road_walkability_prompt)
    human_message = HumanMessage(
        content=[
             {"type": "text", "text": "The image to be graded is given below"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    response = model.invoke([system_message,human_message])
    try:
        output = json.loads(response.content)
        #### Save the output to the database
        # image.overall_score = output["overall_score"]
        # image.negative_components = output["negative_components"]
        # image.actionable_recommendations = output["actionable_recommendations"]
        # db.commit()
        return {"filename": file.filename, "latitude": lat, "longitude": long, "response": output["overall_score"], "negative_components": output["negative_components"], "actionable_recommendations": output["actionable_recommendations"]}
    except Exception as e:
        print(response.content)
        print(str(e))
        raise HTTPException(status_code=500, detail="Parsing Failed")
    
    

