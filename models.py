from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    author_foreign = db.relationship('Posts', backref='author_user') 
    comments_foreign = db.relationship('Comments', backref='user_comment')
    notes_foreign = db.relationship('Notes', backref='user_notes')
    story_foreign = db.relationship('Story', backref='user_story') 
    events_foreign = db.relationship('Events', backref='user_events')
    profile_foreign = db.relationship('Profile', backref='user_profile')
    messages_foreign = db.relationship('Global_Messages', backref='user_messages')
    birthdays_foreign = db.relationship('Birthdays', backref='user_birthday') 
    followers_foreign = db.relationship('Followers', backref='user_followers')                                 
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    publication = db.Column(db.String(20), nullable=False)
    comments_foreign = db.relationship('Comments', backref='posts_comment') 
    reports_foreign = db.relationship('Reports', backref='posts_reports') 
class Comments(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
class Notes(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(100), nullable=False)
class Story(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
class Reports(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  
    reason = db.Column(db.String(100), nullable=False) 
class Events(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
class Profile(db.Model):     
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.String(100), nullable=False) 
class Website_Feedback(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
class Global_Messages(db.Model):     
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    messages_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
class Birthdays(db.Model):  
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    birthday_date = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20), nullable=False)
class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)