from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, TimeoutError
from schema import BookSchema, BookUpdateSchema
from database_conn import db_session

from controllers import (
    def_get_all,
    db_get_book_by_id,
    db_add_book,
    db_update_book,
    db_borrow_book
    )

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

        return def_get_all(response,db)

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
        return db_get_book_by_id(book_id, response, db)

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
        return db_add_book(details, response, db)


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
def update_book(book_details: BookUpdateSchema, response: Response,  book_id: str, db : Session = Depends(get_db)):
    try:
        return db_update_book(book_details, response, book_id, db)


    except IntegrityError as e:
        raise BookIntegrityException(str(e.orig))

    except OperationalError as e:
        raise BookOperationalException(str(e.orig))

    except DataError as e:
        raise BookDataException(str(e.orig))

    except TimeoutError as e:
        raise BookTimeOutException("Took longer than expected")



# Update book count
@book_router.patch("/book/{book_id}/borrow")
def borrow_book(book_id: str, response: Response, db : Session = Depends(get_db)):

    try:
        return db_borrow_book(book_id, response, db)

    except IntegrityError as e:
        raise BookIntegrityException(str(e.orig))

    except OperationalError as e:
        raise BookOperationalException(str(e.orig))

    except DataError as e:
        raise BookDataException(str(e.orig))

    except TimeoutError as e:
        raise BookTimeOutException("Took longer than expected")
