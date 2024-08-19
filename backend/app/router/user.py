from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from app.utils import hashPassword, verifyPassword

router = APIRouter(
    tags=["users"],
    prefix= "/users"
)


@router.post('/', response_model= schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hashPassword(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login', response_model= schemas.Token)
async def login(req: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verifyPassword(user.password, req.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
    
@router.get('/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

