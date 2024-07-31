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
async def update_profiles(id: int, profile:dict, response: Response, db: Session = Depends(get_db)):
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
    
@router_v1.get("/menus")
async def get_menus(db:Session = Depends(get_db)):
    return db.query(models.Menu).all()

@router_v1.post('/createmenu')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    addmenu = models.Menu(
        menu_name=menu['menu_name'],
        img_url=menu['img_url'],
        price=menu['price'],
        rating=menu['rating'],
    )
    db.add(addmenu)
    db.commit()
    db.refresh(addmenu)
    response.status_code = 201
    return addmenu

@router_v1.get('/menus/{menu_id}')
async def get_menu(menu_id: int, db: Session = Depends(get_db)):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

@router_v1.put('/editmenu/{id}')
async def update_profile(id: int, menu:dict, response: Response, db: Session = Depends(get_db)):
    menudb = models.Menu
    try:
        stmt = update(menudb).where(menudb.id==id).values(
            menu_name=menu['menu_name'],
            img_url=menu['img_url'],
            price=menu['price'],
            rating=menu['rating'],
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

@router_v1.delete("/deletemenu/{id}")
async def delete_menus(id: int, response: Response, db: Session = Depends(get_db)):
    try:
        # Query the Menu entry to ensure it exists
        menu = db.query(models.Menu).filter(models.Menu.id == id).first()
        if not menu:
            response.status_code = 404
            return {
                'message': 'Menu not found'
            }

        # Delete the Menu entry which will also delete related Order entries due to cascading
        db.delete(menu)
        db.commit()

        response.status_code = 200
        return {
            'message': 'Delete successfully'
        }
    except Exception as e:
        db.rollback()
        print(f"Error deleting menu: {e}")
        response.status_code = 500
        return {
            'message': str(e)
        }

@router_v1.get("/ordermenu")
async def get_order_menus(db:Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.post("/createorder")
async def create_order(menu: dict, response: Response, db: Session = Depends(get_db)):
    newOrder = models.Order(menu_id=menu['menu_id'], count=menu['count'])
    db.add(newOrder)
    db.commit()
    db.refresh(newOrder)
    response.status_code = 201
    return newOrder

@router_v1.put('/updateorder')
async def update_menu(order: dict, response: Response, db: Session = Depends(get_db)):
    menudb = models.Order
    try:
        stmt = update(menudb).where(menudb.menu_id==order['menu_id']).values(
            count=menudb.count+order['count']
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

@router_v1.delete("/ordermenu/{id}")
async def delete_menu(id: int ,response: Response, db: Session = Depends(get_db)):
    menudb = models.Order
    try:
        stmt = delete(menudb).where(menudb.id==id)
        db.execute(stmt)
        db.commit()
        response.status_code = 201
        return {
            'message' : 'Delete successfully'
        }
    except Exception as e:
        print("No menu with this id")
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
