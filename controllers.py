from fastapi import Response
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

from models import Book
from schema import BookSchema, BookUpdateSchema

def def_get_all(response: Response, db : Session):

    result = db.query(Book).all()
    response.status_code = 200

    return {
            "status_code" : 200,
            "message" : "success",
            "data" : result,
            "error" : None
        }

def db_get_book_by_id(book_id: str, response : Response, db: Session):
    result = db.query(Book).filter(Book.id == book_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="No book found")

    response.status_code = 200

    return {
            "status_code" : 200,
            "message" : "success",
            "data" : result,
            "error" : None
        }

def db_add_book(details: BookSchema, response: Response, db : Session):
    details = details.model_dump()
    book = Book(**details)

    db.add(book)
    db.commit()

    db.refresh(book)

    response.status_code = 201

    return {
        "status_code": 201,
        "message": "success",
        "data": book,
        "error": None
    }

def db_update_book(book_details: BookUpdateSchema, response : Response,  book_id: str, db : Session):
    result = db.query(Book).filter(Book.id == book_id).first()

    if not result:
        raise HTTPException(404, detail="Book not found")

    for key, value in book_details.model_dump().items():
        if value is not None:
            setattr(result, key, value)

    db.commit()

    response.status_code = 200

    db.refresh(result)

    return {
        "status_code": 200,
        "message": "success",
        "data": result,
        "error": None
    }

def db_borrow_book(book_id: str, response: Response, db : Session):
    result = db.query(Book).filter(Book.id == book_id).first()

    if not result:
        raise HTTPException(404, detail="Book not found")

    if result.availability <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")

    setattr(result, "availability", result.availability - 1)

    db.commit()

    db.refresh(result)

    response.status_code = 200

    return {
        "status_code": 200,
        "message": "success",
        "data": result,
        "error": None
    }