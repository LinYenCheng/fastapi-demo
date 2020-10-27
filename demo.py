from fastapi import FastAPI

app = FastAPI()

@app.get('/book/{book_id}')
def get_book_by_id(book_id: int):
    return {
        'book_id': book_id
    }

# --------------------------------------------------
# How about using query parameter
# --------------------------------------------------


@app.get('/get_book')
def get_book_by_id_via_query(book_id: int):
    return {
        'book_id': book_id
    }

# --------------------------------------------------
# Let's mix them up, and add an Enum
# --------------------------------------------------

from enum import Enum

class QueryModeEnum(Enum):
    AUTHOR = 'author'
    CUSTOMER = 'customer'

@app.get('/book/{book_id}/with_mode')
def get_book_by_id_mix(book_id: int, query_mode: QueryModeEnum):
    return {
        'book_id': book_id,
        'query_mode': query_mode,
    }


# --------------------------------------------------
# How about some validation
# --------------------------------------------------

from fastapi import Path

@app.get('/book/{book_id}/with_validation')
def get_book_by_id_with_validation(book_id: int = Path(..., ge=1)):
    return {
        'book_id': book_id
    }

# --------------------------------------------------
# And some extra documents
# --------------------------------------------------
@app.get('/book/{book_id}/with_validation_and_some_extra_documnet')
def get_book_by_id_with_validation_and_some_extra_documnet(
    book_id: int = Path(
        ..., ge=1, 
        title='BOOK ID',
        description='`hey, we also support markdown`\n* 1\n* 2\n * 3\n',
        example=5,
    )):
    return {
        'book_id': book_id
    }

# --------------------------------------------------
# How to describe your response
# --------------------------------------------------
from pydantic import BaseModel, Field

class BookCategory(str, Enum):
    comics = 'comics'
    cooking = 'cooking'
    
class Book(BaseModel):
    bid: int = Field(..., ge=1, title='book id', description='`markdown`', example=5)
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    category: BookCategory

@app.get('/book/{book_id}/with_response_model', response_model=Book)
def get_book_by_id_with_validation_and_some_extra_documnet(
    book_id: int = Path(..., ge=1, example=5)
):
    # return {'book_id': book_id}

    return {
        'bid': book_id,
        'name': 'name of bid {}'.format(book_id),
        'price': 39.95,
        'category': 'cooking'
    }


# --------------------------------------------------
# Can we use BaseModel as input? 
# --------------------------------------------------
@app.post('/book', response_model=Book)
def get_book_by_id_with_validation_and_some_extra_documnet(
    payload: Book
):
    payload.name += ' suffix'
    return payload

# --------------------------------------------------
# Redirect home to docs
# --------------------------------------------------
from fastapi.responses import RedirectResponse

@app.get('/', include_in_schema=False)
def home():
    return  RedirectResponse('/docs')