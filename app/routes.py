from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import NewBardForm, loginForm, EventForm, VenueForm, registerForm
from app import db
from app.models import Bard, BardToEvent, Event, Venue
from datetime import datetime
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

        flash('Created new Bard: {}'.format(
            form.name.data))
        final_form = NewBardForm()
        render_template('newBards.html', title='New Bard', form=final_form)

    return render_template('newBards.html', title='New Bard', form=form)

@app.route('/event', methods=['GET', 'POST'])
def event():
    venueList= db.session.query(Venue).filter(Venue.id)
    eventList = db.session.query(Event).filter(Event.id)
    allEvents = [i.id for i in eventList]
    lastEvent = len(allEvents) + 1
    allVenues = [(i.id, i.village) for i in venueList]
    bardList = db.session.query(Bard).filter(Bard.id)
    allBards = [(i.id, i.name) for i in bardList]


    form = EventForm()
    form.venue.choices = allVenues
    form.bard.choices = allBards
    if form.validate_on_submit():
        event = Event(eventname=form.name.data, venueID=form.venue.data, startTime=form.date.data)
        db.session.add(event)
        db.session.commit()

        bard = BardToEvent(bardID=form.bard.data, eventID=lastEvent)
        db.session.add(bard)
        db.session.commit()


        #date = Event(startTime=form.startTime.data)
        #db.session.add(date)
        #db.session.commit()

        flash('Created new Event: {}'.format(
            form.name.data))
        final_form = EventForm()
        render_template('event.html', title='Event', form=final_form)

    return render_template('event.html', title='Event', form=form)

@app.route('/venue', methods=['GET', 'POST'])
def venue():
    form = VenueForm()
    if form.validate_on_submit():
        venue = Venue(village=form.village.data, kingdom=form.kingdom.data)
        db.session.add(venue)
        db.session.commit()


        flash('Created new Venue: {}'.format(
            form.village.data, form.kingdom.data))
        final_form = VenueForm()
        render_template('venue.html', title='New Venue', form=final_form)

    return render_template('venue.html', title='New Venue', form=form)



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
    b1.set_password("Marillion")
    b2 = Bard(name="Tom O Sevenstrings", description="No one plays quite like me. I know hundreds of songs.")
    b3 = Bard(name="The Blue Bard", description="My hair is bright blue and I know a tune or two.")
    b4 = Bard(name="Symon Silvertongue", description="I am not merely a reciter of tunes. I am an accomplished lyricist.")
    b5 = Bard(name="Shylock the Shy", description="I prefer to play alone.")
    db.session.add_all([b1, b2, b3, b4, b5])
    db.session.commit()
    e1 = Event(eventname="The Great Tourney", venueID=1, startTime=datetime(1604, 3, 5))
    e2 = Event(eventname="Bilbo's 111th Birthday", venueID=2, startTime=datetime(3001, 9, 22))
    e3 = Event(eventname="Frodo's Birthday", venueID=2, startTime=datetime(3001, 9, 22))
    e4 = Event(eventname="Joffrey's Wedding", venueID=1, startTime=datetime(1207, 3, 9))
    e5 = Event(eventname="Manwe's Great Feast", venueID=3, startTime=datetime(1006, 3, 19))
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = Bard.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = registerForm()
    if form.validate_on_submit():
        bard = Bard(name=form.name.data, description=form.description.data)
        bard.set_password(form.password.data)
        bardCheck = Bard.query.filter_by(name=form.name.data).first()
        if bardCheck is not None:
            flash('username taken')
            return redirect(url_for('register'))
        #return redirect(url_for('login'))
        db.session.add(bard)
        db.session.commit()

        login_user(bard, remember=form.remember_me.data)
        flash('You are now registered as {}'.format(
            form.name.data))
        final_form = registerForm()
        render_template('register.html', title='Register', form=final_form)

    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))