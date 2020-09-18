from flask import render_template
from app import app
import random


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/bards')
def bards():
    bardList = [
        {"singer": "Marillion",
         "description": "I'm drunk but talented and know many sad lays."},
        {"singer": "Tom O Sevenstrings",
         "description": "No one plays quite like me. I know hundreds of songs."},
        {"singer": "The Blue Bard",
         "description": "My hair is bright blue, and I know a tune or two."},
        {"singer": "Symon Silvertongue",
         "description": "I am not merely a reciter of tunes. I am an accomplished lyricist."}
    ]

    return render_template('bards.html', bardList=bardList)




@app.route('/bard')
def bard():
    bard = {"singer": "Marillion",
            "description": "I'm drunk but talented and know many sad lays.",
            "place": "The Greasy Spoon",
            "placeDescription": "Get some nice ham and bread at the Greasy Spoon and hear Marillion sing. (Do not order the soup.  It is unspeakable.)"}


    return render_template('bard.html', bard=bard)
@app.route('/newBards')
def newBards():
    construction = {"create": "Create a new bard",
                    "const": "Page under construction."}

    return render_template('newBards.html', construction=construction)