from typing import Optional, Any, Union
from venv import create
from fastapi import FastAPI, status, HTTPException
import uvicorn
from sqlalchemy import inspect
from contextlib import contextmanager
from pprint import pprint

from biosearch.FastAPI.models import Base, Person, Presentation, Slide, Textbox
from biosearch.FastAPI.schemas import PersonSerializer, PresentationSerializer, SlideSerializer, TextboxSerializer
from biosearch.FastAPI.database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@contextmanager
def create_db():
    """ Provide transactional scope around a series of operations """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

@app.get('/')# ?name=world
def example(name : Optional[str] = 'default'):
    return {'Optional name':f'Hello {name}'}

@app.get('/persons', response_model = list[PersonSerializer], status_code = status.HTTP_200_OK)
def retrieve_persons():
    with create_db() as db:
        people = db.query(Person).all()
    # print(inspect(people).expired)
    # pprint(people)
    return people


@app.get('/person/{id}', response_model = PersonSerializer, status_code = status.HTTP_200_OK)
def retrieve_person_by_id(id : int):
    with create_db() as db:
        retrieved_person =db.query(Person).filter(Person.id == id).first()
    
    if retrieved_person == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Resource not found')

    return retrieved_person 

@app.post('/person', response_model = PersonSerializer, status_code = status.HTTP_201_CREATED)
def create_new_person(person:PersonSerializer):
    with create_db() as db:
        new_person = Person(
            first_name = person.first_name,
            last_name = person.last_name,
            age = person.age,
            gender = person.gender,
            nationality = person.nationality,
            hasWatch = person.hasWatch
        )
        db.add(new_person)

    return new_person

@app.put('/person/{id}', response_model = PersonSerializer, status_code = status.HTTP_202_ACCEPTED)
def update_person(id: int, person: PersonSerializer):
    with create_db() as db:
        retrieved_person = db.query(Person).filter(Person.id == id).first()
        print(retrieved_person)
        list_attributes = ['first_name', 'last_name', 'age', 'gender', 'nationality', 'hasWatch']
        for attr in list_attributes:
            new_value = getattr(person, attr)
            setattr(retrieved_person, attr, new_value)
        
    return retrieved_person

@app.delete('/person/{id}')
def delete_person(id:int):
    with create_db() as db:
        retrieved_person = db.query(Person).filter(Person.id == id).first()
        if retrieved_person == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Requested person could not be deleted')
        db.delete(retrieved_person)
    return retrieved_person


@app.get("/google-presentations", response_model=list[PresentationSerializer])
def get_presentations():
    with create_db() as db:
        presentations = db.query(Presentation).all()
    return presentations

@app.get('/google-slides/{presentation_id}', response_model = list[Union[SlideSerializer, TextboxSerializer]])
def get_slides(presentation_id : int, slide_id : Union[int, None] = None): # ? add the ability to enter skills
    with create_db() as db: # ! extension
        if slide_id == None:
            slides = db.query(Slide).filter(Slide.presentation_id == presentation_id).all()

        else: # isinstance(slide_id, int) == True
            print(slide_id)
            slides = db.query(Textbox).filter(Textbox.slide_id == slide_id).all()

    return slides

if __name__ == '__main__':
    uvicorn.run('main:app', reload = True)