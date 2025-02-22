from fastapi import APIRouter, HTTPException, status
import schemas, models
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from oauth2 import get_current_user

router = APIRouter()


# Create a Post
@router.post('/posts', response_model=schemas.PostPydantic)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Show all Post
@router.get('/posts', response_model=list[schemas.PostPydantic])
# @router.get('/posts', response_model=list[schemas.PostOut])
def get_all_posts(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # i have maek  User Posts Public filter(models.Post.owner_id == current_user.id).all()
    all_post = db.query(models.Post).all()

    return all_post


# Show Post By id
@router.get("/posts/{id}", response_model=schemas.PostPydantic)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    # I have all Users to view Other users Post that why i have comments it

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #     detail="You are not Allow to view other people post")

    return post


# Update Post

@router.put('/posts/{id}', response_model=schemas.PostPydantic)
def update(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db),
           current_user: schemas.UserSchemas = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with this ID: {id}")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post


# Delete A Post

@router.delete("/posts/{id}")
def delete(id: int, db: Session = Depends(get_db),
           current_user: schemas.UserSchemas = Depends(get_current_user)):
    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    delete_post = delete_post_query.first()
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with this ID {id} does not exit")

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    delete_post_query.delete(synchronize_session=False)
    db.commit()

    return {"Message": "Post Successfully deleted"}
