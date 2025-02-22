from fastapi import APIRouter, Depends, status, HTTPException
import utils, models, schemas
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


# Create user
@router.post('/users', response_model=schemas.UsersOutPydantic, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UsersPydantic, db: Session = Depends(get_db)):
    # hashing Password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get User By ID

@router.get("/users/{id}", response_model=schemas.UsersOutPydantic)
def user_by_id(id: str, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} does not exit! ")
    return user
