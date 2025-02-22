from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db
import posts, users
from router import auth
import likes

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/')
def read_root():
    return {"Message": "Welcome to FastAPI with Postgres sql"}


@app.get("/users/")
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
