from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, TimeoutError
from models import Book
from schema import BookSchema, BookUpdateSchema
from database_conn import db_session

from exception_handlers import BookIntegrityException, BookDataException
from exception_handlers import BookOperationalException, BookTimeOutException

book_router = APIRouter()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()



# Get all books
@book_router.get("/books")
def get_all_books(response : Response, db: Session = Depends(get_db)):
    try:

        result = db.query(Book).all()
        response.status_code = 200
        return {
            "status_code" : 200,
            "message" : "success",
            "data" : result,
            "error" : None
        }

    except IntegrityError as e:
        raise BookIntegrityException(str(e.orig))

    except OperationalError as e:
        raise BookOperationalException(str(e.orig))

    except DataError as e:
        raise BookDataException(str(e.orig))

    except TimeoutError as e:
        raise BookTimeOutException("Took longer than expected")



# Get book by id
@book_router.get("/books/{book_id}")
def get_book_by_id(book_id: str, response : Response, db: Session = Depends(get_db)):
    try:
        result = db.query(Book).filter(Book.id == book_id).first()

        if not result:
            raise HTTPException(status_code=404, detail="No book found")

        response.status_code = 200

        result = db.query(Book).filter(Book.id == book_id).first()

        return {
            "status_code" : 200,
            "message" : "success",
            "data" : result,
            "error" : None
        }

    except OperationalError as e:
        raise BookOperationalException(str(e.orig))

    except DataError as e:
        raise BookDataException(str(e.orig))

    except TimeoutError as e:
        raise BookTimeOutException("Took longer than expected")



# Add a book
@book_router.post("/books")
def add_book(details: BookSchema, response: Response, db : Session = Depends(get_db)):
    try:
        
        details = details.model_dump()
        book = Book(**details)

        db.add(book)
        db.commit()
        
        response.status_code= 201
        
        return {
            "status_code" : 201,
            "message" : "success",
            "data" : book,
            "error" : None
        }


    except IntegrityError as e:
        raise BookIntegrityException(str(e.orig))

    except OperationalError as e:
        raise BookOperationalException(str(e.orig))

    except DataError as e:
        raise BookDataException(str(e.orig))

    except TimeoutError as e:
        raise BookTimeOutException("Took longer than expected")



# Update a specific book
@book_router.put("/books/{book_id}/update")
def update_book(*,book_details: BookUpdateSchema,  book_id: str, db : Session = Depends(get_db), res: Response):
    try:
        result = db.query(Book).filter(Book.id == book_id).first()

        if not result:
            raise HTTPException(404, detail="Book not found")

        for key, value in book_details.model_dump().items():
            if value is not None:
                setattr(result, key, value)

        db.commit()

        res.status_code = 200

        result = db.query(Book).filter(Book.id == book_id).first()

        return {
            "status_code" : 200,
            "message" : "success",
            "data" : result,
            "error" : None
        }


    except IntegrityError as e:
        raise BookIntegrityException(str(e.orig))

    except OperationalError as e:
        raise BookOperationalException(str(e.orig))

    except DataError as e:
        raise BookDataException(str(e.orig))

    except TimeoutError as e:
        raise BookTimeOutException("Took longer than expected")



# Update book count
@book_router.patch("/book/{book_id}/availability")
def availability(book_id: str, res: Response, db : Session = Depends(get_db)):

    try:
        result = db.query(Book).filter(Book.id == book_id).first()

        if not result:
            raise HTTPException(404, detail="Book not found")

        setattr(result, "availability", result.availability-1)

        db.commit()

        return {
            "status_code" : 200,
            "message" : "success",
            "data" : result,
            "error" : None
        }



    except IntegrityError as e:
        raise BookIntegrityException(str(e.orig))

    except OperationalError as e:
        raise BookOperationalException(str(e.orig))

    except DataError as e:
        raise BookDataException(str(e.orig))

    except TimeoutError as e:
        raise BookTimeOutException("Took longer than expected")