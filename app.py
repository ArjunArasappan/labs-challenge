from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import hashlib

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

from models import *


#helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_fields(data_dic, fields):
    for st in fields: 
        if st not in data_dic.keys() :
            return True
        if data_dic[st].strip() == '':
            return True
    return False


#routes

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api', methods=['GET'])
def clubs_api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

#1. get clubs
@app.route('/api/clubs', methods=['GET'])
def get_clubs():
    clubs = Club.query.all()
    result = []
    for club in clubs:
        tags = [tag.name for tag in club.tags]
        club_dict = {
            "code": club.code,
            "name": club.name,
            "id": club.id,
            "description": club.description,
            "tags": tags,
            "favorite_count": len(club.users)
        }
        result.append(club_dict)
    return jsonify(result), 200

#2. upload file for a club
@app.route('/api/clubs/<string:club_code>/upload', methods=['POST'])
@login_required
def upload_file_for_club(club_code):
    club = Club.query.filter_by(code=club_code).first()
    if not club:
        return jsonify({"error": "Club code doesn't exist!"}), 404

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 404

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file."}), 404

    # Check if a file with the same name already exists for the club
    existing_file = File.query.filter_by(club_code=club_code, filename=file.filename).first()
    
    if existing_file:
        return jsonify({"error": "File exists!"}), 404

    if file and allowed_file(file.filename):
        new_file = File(
            club_code=club.code,
            filename=file.filename,
            data=file.read(),
            mimetype=file.mimetype
        )
        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message": "File uploaded successfully!", "file_id": new_file.id}), 200
    return jsonify({"error": "Filename error"}), 404



#3. retrieve file for a club
@app.route('/api/clubs/<string:club_code>/uploads/<string:file_name>', methods=['GET'])
@login_required
def uploaded_file_for_club(club_code, file_name):
    club = Club.query.filter_by(code=club_code).first()
    if not club:
        return jsonify({"error": "Club code doesn't exist."}), 404

    file_record = File.query.filter_by(filename=file_name, club_code=club.code).first()
    if not file_record:
        return jsonify({"error": "File not found!"}), 404

    response = app.response_class(file_record.data, content_type=file_record.mimetype)
    response.headers["Content-Disposition"] = f"attachment; filename={file_record.filename}"
    return response, 201


#4. get info on a user
@app.route('/api/user/<username>', methods=['GET'])
@login_required
def get_user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify({ 'username': user.username }), 200

#5. search for clubs with substring
@app.route('/api/clubs/search/<string:query>', methods=['GET'])
def search_clubs(query):
    clubs = Club.query.filter(Club.name.ilike(f"%{query}%")).all()
    return jsonify([club.name for club in clubs])

#6. create new club
@app.route('/api/clubs', methods=['POST'])
@login_required
def add_club():
    data = request.get_json()
    
    if check_fields(data, ['name', 'description', 'code']):
        return jsonify({'error': 'Missing or empty fields.'}), 404
    
    club = Club.query.filter_by(name=data['name']).first()
    
    if club:
        return jsonify({'error': 'club name already exists'}), 409
    
    new_club = Club(name=data['name'], description=data['description'], code=data['code'])
    db.session.add(new_club)
    db.session.commit()
    return jsonify({'message': 'Club added!'}), 201

#7. favorite a club
@app.route('/api/clubs/<string:club_name>/favorite', methods=['POST'])
@login_required
def favorite_club(club_name):
    user = current_user
    
    club = Club.query.filter_by(name=club_name).first()
    
    if not club:
        return jsonify({'error': 'Club does not exist.'}), 404
    
    if user in club.users:
        return jsonify({'error': 'Club already checked as favorite.'}), 404
    
    club.users.append(user)
    db.session.commit()
    return jsonify({'message': 'Club checked as favorite.'})

#8. update club name and description
@app.route('/api/clubs/<string:club_name>', methods=['PUT'])
@login_required
def modify_club(club_name):
    
    data = request.get_json()
    print(club_name)
    
    if check_fields(data, ['description']):
        return jsonify({'error': 'missing fields'}), 404
    
    club = Club.query.filter_by(name = club_name).first()
    
    if not club:
        return jsonify({'error': 'Club name does not exist.'}), 404
    
    print(club_name)
    
    club.name = club_name
    club.description = data.get('description')
    db.session.commit()
    
    return jsonify({'message': 'Club description updated!'})

#9. get all tags and clubs with each tag
@app.route('/api/tags', methods=['GET'])
def show_tags():
    tags = Tag.query.all()
    return jsonify({tag.name: len(tag.clubs) for tag in tags})


#login functions

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def hash_password(password):
    m = hashlib.sha256()
    m.update(bytes(password, 'utf-8'))
    return m.digest()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if check_fields(data, ['username', 'password']):
        return jsonify({'error': 'missing fields'}), 404
    
    hashed_pw = hash_password(data['password'])
    
    username = User.query.filter_by(username=data['username']).first()
    if not username:
        new_user = User(username=data['username'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully.'}), 201
    else:
        return jsonify({'message': 'Already Registered.'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if check_fields(data, ['username', 'password']):
        return jsonify({'error': 'missing fields'}), 404
    
    user = User.query.filter_by(username=data['username']).first()
 
    if not user or not (user.password == hash_password(data['password'])):
        return jsonify({'error': 'Login failed. Check username or password.'}), 404
    
    login_user(user)
    return jsonify({'message': 'Logged in successfully.'}), 200

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():

    logout_user()
    return jsonify({'message': 'Logged out successfully.'}), 201
