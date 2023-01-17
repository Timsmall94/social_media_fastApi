from .. import model, schemas, utils
from fastapi import Depends, FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import List

router = APIRouter(
    prefix="/user",
    tags=['User']
)
#tags is used to Group our route in the Fastapi Swagger
#the prefix function help all our route which was "/post" to enable our code smaller
@router.post ('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_post ( user:schemas.UserCreate, db: Session =Depends(get_db)):
    Newuser = db.query(model.User).filter(model.User.email == user.email).first()
      
    if  Newuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"The user with Email {user.email} already exist")
    
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user=model.User(**user.dict())
   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_User(id:int, db: Session =Depends(get_db)):
    user= db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} not found")
    return user
    
@router.get('/', response_model=List[schemas.UserOut])
def get_all_user(db: Session = Depends(get_db)):
    all_user=db.query(model.User).all()
    return all_user
