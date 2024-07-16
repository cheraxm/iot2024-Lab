import profile
from urllib import response
from dotenv import load_dotenv
from sqlalchemy import update
from sqlalchemy import delete
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.post("/profiles")
async def create_profile(profile: dict, response: Response, db: Session = Depends(get_db)):
    newprofile = models.Profile(id=profile["id"], firstname=profile["firstname"], lastname=profile["lastname"],
                nickname=profile["nickname"], dob=profile["dob"], stu_id=profile['stu_id'], gender=models.GenderChoice[profile['gender'].upper()])
    db.add(newprofile)
    db.commit()
    db.refresh(newprofile)
    response.status_code = 201
    return newprofile

@router_v1.get("/profiles")
async def get_profiles(db: Session = Depends(get_db)):
    return db.query(models.Profile).all()

@router_v1.put('/profiles/{id}')
async def update_profile(id: int, profile:dict, response: Response, db: Session = Depends(get_db)):
    profiledb = models.Profile
    try:
        stmt = update(profiledb).where(profiledb.id==id).values(
            firstname=profile["firstname"], 
            lastname=profile["lastname"],
            nickname=profile["nickname"], 
            dob=profile["dob"], 
            stu_id=profile['stu_id'], 
            gender=models.GenderChoice[profile['gender'].upper()]
        )
        db.execute(stmt)
        db.commit()
        response.status_code = 201
        return {
            'message' : 'Update successfully'
        }
    except Exception as e:
        print("No profile with this id")
        response.status_code = 500
        return {
            'message': str(e)
        }
    

@router_v1.delete("/profiles/{id}")
async def delete_profile(id: int ,response: Response, db: Session = Depends(get_db)):
    profiledb = models.Profile
    try:
        stmt = delete(profiledb).where(profiledb.id==id)
        db.execute(stmt)
        db.commit()
        response.status_code = 201
        return {
            'message' : 'Update successfully'
        }
    except Exception as e:
        print("No profile with this id")
        response.status_code = 500
        return {
            'message': str(e)
        }




# @router_v1.patch('/books/{book_id}')
# async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
#     pass

# @router_v1.delete('/books/{book_id}')
# async def delete_book(book_id: int, db: Session = Depends(get_db)):
#     pass

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
