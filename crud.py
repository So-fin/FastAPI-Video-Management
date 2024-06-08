from sqlalchemy.orm import Session

import models
import schemas


def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()


def get_videos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Video).offset(skip).limit(limit).all()


def get_videos_by_name(db: Session, name: str):
    return db.query(models.Video).filter(models.Video.name == name).all()


def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(name=video.name, path=video.path, size=video.size, format=video.format)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
