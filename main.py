from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root')
def root() -> str:
    return "Hello, student!!!"


@app.post('/post', response_model=Timestamp, summary='Get Post')
def get_post():
    new_timestamp = Timestamp(id=len(post_db), timestamp=datetime.now().hour)
    post_db.append(new_timestamp)
    return Timestamp(id=new_timestamp.id, timestamp=new_timestamp.timestamp)


@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dogs():
    return list(dogs_db.values())


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if dog.pk in [x.pk for x in list(dogs_db.values())]:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    else:
        dogs_db[len(dogs_db)] = dog
    return dog


@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dog_by_pk(pk: int):
    for d in list(dogs_db.values()):
        if d.pk == pk:
            return d


@app.patch('/dog', response_model=Dog, summary='Update Dog')
def create_dog(dog: Dog):
    if dog.pk in [x.pk for x in list(dogs_db.values())]:
        for d in dogs_db:
            if dogs_db[d].pk == dog.pk:
                dogs_db[d] = dog
    else:
        pass
    return dog
