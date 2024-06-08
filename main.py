from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
import crud
import models
import schemas
import database
import utils

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.post("/upload_video/", response_model=schemas.Video)
async def upload_video(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    file_location = f"videos/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    file_size = utils.get_file_size(file_location)
    video = schemas.VideoCreate(name=file.filename, path=file_location, size=file_size, format="original")

    return crud.create_video(db=db, video=video)


@app.post("/convert_to_mp4/{video_id}", response_model=schemas.Video)
async def convert_video(video_id: int, db: Session = Depends(database.get_db)):
    video = crud.get_video(db=db, video_id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    input_path = video.path
    output_path = f"videos/{os.path.splitext(video.name)[0]}.mp4"

    utils.convert_to_mp4(input_path, output_path)
    video.path = output_path
    video.format = "mp4"
    video.name = output_path.split('/')[1]
    db.commit()
    db.refresh(video)

    return video


@app.get("/search_video/", response_model=list[schemas.Video])
async def search_video(name: str = None, db: Session = Depends(database.get_db)):
    if name:
        videos = crud.get_videos_by_name(db=db, name=name)
    else:
        videos = crud.get_videos(db=db)

    return videos
