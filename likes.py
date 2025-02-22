from fastapi import APIRouter, Depends, HTTPException, FastAPI, Response, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import Like
from oauth2 import get_current_user

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: Like, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {like.post_id} does not exit")

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id,
                                              models.Like.user_id == current_user.id)
    found_like = like_query.first()

    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.name} has already like post")

        new_like = models.Like(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": " Successfully like post"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have like post to remove")

        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": " Successfully Delete like from post"}
