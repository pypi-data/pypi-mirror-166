from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TSVECTOR

Base = declarative_base()

class Person(Base):
    __tablename__ = 'Persons'

    id = Column(Integer, unique = True, primary_key = True)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    age = Column(Integer)
    gender = Column(String)
    nationality = Column(String)
    hasWatch = Column(Boolean)

    def __repr__(self):
        return f'Person: first_name:{self.first_name}'

class Presentation(Base):
    __tablename__ = "google_presentations"

    presentation_id = Column(Integer, primary_key=True, index=True)
    presentation_link = Column(String, unique=True)
    club_name = Column(String, unique=True)
    revision_id = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    slides = relationship('Slide',back_populates = 'presentation')

    def __repr__(self):
        return f'<Presentation club:{self.club_name} presentation_id:{self.presentation_id} link:{self.presentation_link}>'

class Slide(Base):
    __tablename__ = 'google_slides'

    slide_id = Column(Integer, primary_key = True)
    slide_link = Column(String, unique = True)
    presentation_id = Column(Integer, ForeignKey('google_presentations.presentation_id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    presentation = relationship('Presentation', back_populates = 'slides')
    textboxes = relationship('Textbox', back_populates = 'slide')

    def __repr__(self):
        return f'<Slide slide_id:{self.slide_id} presentation_id:{self.presentation_id} link:{self.slide_link}>'


class Textbox(Base):
    __tablename__ = 'google_slide_textboxes'

    textbox_id = Column(Integer, primary_key = True)
    textbox_link = Column(String, unique = True)
    slide_id = Column(Integer, ForeignKey('google_slides.slide_id'))
    text = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    ts = Column(TSVECTOR)

    slide = relationship('Slide', back_populates = 'textboxes')

    def __repr__(self):
        return f'<Textbox textbox_id:{self.textbox_id} slide_id:{self.slide_id} link:{self.textbox_link}>'