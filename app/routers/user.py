from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOp)
def create_user(newUser: schemas.UserCreate, db : Session = Depends(get_db)):

    #Hash Password
    hashed_passowrd = utils.hashPassword(newUser.password)
    newUser.password = hashed_passowrd

    newUser= models.User(**newUser.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

@router.get('/{id}', response_model=schemas.UserOp)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    
    return user