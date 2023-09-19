import json
from app import db, app, DB_FILE
from models import User, Club, Tag
import os

#creates the user josh
def create_user():
    user = User(username='josh', password='hashed_password') 
    db.session.add(user)
    db.session.commit()

#loads in data from the clubs.json
def load_data():
    with open('clubs.json', 'r') as f:
        clubs = json.load(f)
    
    for club in clubs:
            new_club = Club(name=club['name'], description=club['description'], code=club['code'])
            db.session.add(new_club)

            for tag_name in club['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                
                #create tag if it doesnt exist
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag) 
                new_club.tags.append(tag)
    
    db.session.commit()
    

if __name__ == '__main__':
    # Delete any existing database before bootstrapping a new one.
    LOCAL_DB_FILE = "instance/" + DB_FILE
    if os.path.exists(LOCAL_DB_FILE):
        os.remove(LOCAL_DB_FILE)

    with app.app_context():
        db.create_all()
        create_user()
        load_data()
