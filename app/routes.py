from flask import render_template, flash, redirect
from app import app
from app.forms import NewBardForm
from app import db
from app.models import Bard, BardToEvent, Event, Venue
import random


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/bards')
def bards():

    bardList = Bard.query.all()

    return render_template('bards.html', bardList=bardList)





@app.route('/bard/<name>')
def bard(name):
    bard = Bard.query.filter_by(name=name).first()
    return render_template('bard.html', bard=bard)


@app.route('/newBards', methods=['GET', 'POST'])
def newBards():
    form = NewBardForm()
    if form.validate_on_submit():
        bard = Bard(name=form.name.data, description=form.bardDescription.data)
        db.session.add(bard)
        db.session.commit()

        venue = Venue(village=form.villageName.data, kingdom=form.kingdom.data)
        db.session.add(venue)
        db.session.commit()

        event = Event(eventname=form.eventName.data, venueID=venue.id)
        db.session.add(event)
        db.session.commit()

        bardToEvent = BardToEvent(bardID=bard.id, eventID=event.id)
        db.session.add(bardToEvent)
        db.session.commit()


        flash('Created new Bard: {}'.format(
            form.name.data, form.villageName.data))
        final_form = NewBardForm()
        render_template('newBards.html', title='New Bard', form=final_form)

    return render_template('newBards.html', title='New Bard', form=form)

@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   db.session.commit()

@app.route('/populate_db')
def populate_db():
    b1 = Bard(name="Marillion", description="I'm drunk but talented and know many sad lays.")
    b2 = Bard(name="Tom O Sevenstrings", description="No one plays quite like me. I know hundreds of songs.")
    b3 = Bard(name="The Blue Bard", description="My hair is bright blue and I know a tune or two.")
    b4 = Bard(name="Symon Silvertongue", description="I am not merely a reciter of tunes. I am an accomplished lyricist.")
    b5 = Bard(name="Shylock the Shy", description="I prefer to play alone.")
    db.session.add_all([b1, b2, b3, b4, b5])
    db.session.commit()
    e1 = Event(eventname="The Great Tourney", venueID=1)
    e2 = Event(eventname="Bilbo's 111th Birthday", venueID=2)
    e3 = Event(eventname="Frodo's Birthday", venueID=2)
    e4 = Event(eventname="Joffrey's Wedding", venueID=1)
    e5 = Event(eventname="Manwe's Great Feast", venueID=3)
    db.session.add_all([e1, e2, e3, e4, e5])
    db.session.commit()
    be1 = BardToEvent(bardID=b1.id, eventID=e1.id)
    be2 = BardToEvent(bardID=b1.id, eventID=e5.id)
    be3 = BardToEvent(bardID=b2.id, eventID=e1.id)
    be4 = BardToEvent(bardID=b4.id, eventID=e1.id)
    be5 = BardToEvent(bardID=b3.id, eventID=e4.id)
    be6 = BardToEvent(bardID=b2.id, eventID=e3.id)
    be7 = BardToEvent(bardID=b3.id, eventID=e5.id)
    db.session.add_all([be1, be2, be3, be4, be5, be6, be7])
    db.session.commit()
    v1 = Venue(village="King's Landing", kingdom="Westeros")
    v2 = Venue(village="The Shire", kingdom="Middle Earth")
    v3 = Venue(village="Valinor", kingdom="Arda")
    db.session.add_all([v1, v2, v3])
    db.session.commit()
    return render_template('base.html', title='Populate DB')