# This is just a program to play about with the chinook database and try to retrieve information from more than one file
# at the same time. 
#
# This program uses the highest level of abstraction in SQLAlchemy's abstraction layer, Class based models, so it is above the 
#  command line like commands and the expression type commands.abs
# 

# Note that unlike the expresion level we did not need to import Table and MetaDat
from sqlalchemy import (
    create_engine, Column, Float, ForeignKey, Integer, String 
) 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# executing the instructions from our localhost "chinook" db
db = create_engine("postgresql:///chinook")

base = declarative_base()

# Next create the class-based models of the tables, this should happen before you create a new session
# create a class-based model for the "Artist" table
class Artist(base):
    __tablename__ = "Artist"
    ArtistId = Column(Integer, primary_key=True)
    Name = Column(String)

# create a class-based model for the "Album" table
class Album(base):
    __tablename__ = "Album"
    AlbumId = Column(Integer, primary_key=True)
    Title = Column(String)
    ArtistId = Column(Integer, ForeignKey("Artist.ArtistId"))

# create a class-based model for the "TRack" table
class Track(base):
    __tablename__ = "Track"
    TrackId = Column(Integer, primary_key=True)
    Name = Column(String)
    AlbumId = Column(Integer, ForeignKey("Album.AlbumId"))
    MediaTypeId = Column(Integer, primary_key=False)
    GenreId = Column(Integer, primary_key=False)
    Composer = Column(String)
    Milliseconds = Column(Integer, primary_key=False)
    Bytes = Column(Integer, primary_key=False)
    UnitPrice = Column(Float)


# instead of connecting to the database directly, we will ask for a session
# create a new instance of sessionmaker, then point to our engine (the db)
Session = sessionmaker(db)
# opens an actual session by calling the Session() subclass defined above
session = Session()

# creating the database using declaritive base subclass
base.metadata.create_all(db)


# Query 1 - select all the albums but instead of displaying ArtistId=51 
# display the artist name from Artist table
# albums = session.query(Album, Artist).filter(Album.ArtistId == Artist.ArtistId).all()
# for album in albums:
#    print(album.Album.AlbumId,album.Album.Title, album.Artist.Name, sep = " | ")
    

# Query 2: select all the tracks and display the Album ID and the Artist name
# tracks = session.query(Track, Album, Artist).filter(Track.AlbumId == Album.AlbumId).filter(Album.ArtistId == Artist.ArtistId).all()

# Query 3: select all the tracks and display the Album ID and the Artist name but only for Queen
tracks = session.query(Track, Album, Artist).filter(Track.AlbumId == Album.AlbumId).filter(
    Album.ArtistId == Artist.ArtistId).filter(Artist.Name == "Queen")

for track in tracks:
    print( 
        track.Track.Name, 
        track.Album.Title, 
        track.Artist.Name, 
        sep = ", ")