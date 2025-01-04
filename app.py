from flask import Flask, request, redirect, render_template, session
from flask_migrate import Migrate
from models import db, User, Posts, Comments, Notes, Story, Reports, Events
from models import Profile, Website_Feedback, Global_Messages, Birthdays, Followers
app = Flask(__name__) 
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'secret_key' 
db.init_app(app)  
migrate = Migrate(app, db)
# Routes
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    data = User.query.all()
    return render_template('login.html', data=data)

@app.route('/authenticate', methods=["POST"])
def login_check():
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    user = User.query.filter_by(user_name=user_name).first()  
    if user and user.password == password:
        session['user_id'] = user.id 
        return redirect('/home') 
    return redirect('/login')

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')

@app.route('/post_create_account', methods=["POST"])
def post_create_account():
    user_name = request.form.get("user_name")
    email = request.form.get("email")
    password = request.form.get("password")
    if user_name and email and password:
        new_user = User(user_name=user_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
    return redirect('/login')

@app.route('/delete_user/<int:id>')
def delete_user(id):
    erase_user = User.query.get(id)
    if erase_user:
        Profile.query.filter_by(user_id=id).delete()
        Notes.query.filter_by(user_id=id).delete()
        Story.query.filter_by(story_id=id).delete()
        Global_Messages.query.filter_by(messages_id=id).delete()
        Comments.query.filter_by(user_id=id).delete()
        Reports.query.filter_by(post_id=id).delete()
        Posts.query.filter_by(author=id).delete()
        Followers.query.filter_by(user_id=id).delete()
        Birthdays.query.filter_by(user_id=id).delete()
        Events.query.filter_by(user_id=id).delete()
        db.session.delete(erase_user)
        db.session.commit()
    return redirect('/')

@app.route('/logout')  
def logout():
    session.clear()
    return redirect('/login')

@app.route('/home')
def home():
    data = Posts.query.all()
    current_user = User.query.get(session.get('user_id'))  
    return render_template('home.html', data=data, current_user=current_user)

@app.route('/create_blog_post')
def create_post():
    user_id = session.get('user_id') 
    if user_id:
        current_user = User.query.get(session.get('user_id'))  
        return render_template('create_blog_post.html', current_user=current_user)
    return redirect('/login')

@app.route('/post_blog_post', methods=["POST"])
def blog_post():
    title = request.form.get("title")           
    content = request.form.get("content")       
    author = request.form.get("author")  
    publication = request.form.get("publication") 
    if title and content and publication and author: 
        new_post = Posts(title=title, content=content, author=author, publication=publication)  
        db.session.add(new_post)
        db.session.commit()    
    return redirect('/home')

@app.route('/delete_post/<int:id>')
def post_delete(id):
    delete_post = Posts.query.get(id)
    if delete_post:
        Comments.query.filter_by(post_id=id).delete()
        Reports.query.filter_by(post_id=id).delete()
        db.session.delete(delete_post)
        db.session.commit()
    return redirect('/home')

@app.route('/update_user/<int:id>')
def update_user(id):
    data = User.query.get(id)
    if data:
        return render_template('update_user.html', data=data)
    return redirect('/login')

@app.route('/user_update/<int:id>', methods=["POST"])
def post_update_user(id):
    data = User.query.get(id)
    if data:
        data.email = request.form.get("email")
        data.password = request.form.get("password")
        db.session.commit()
    return redirect('/login')

@app.route('/post_details/<int:id>')
def post_details(id):
    post = Posts.query.get(id)
    comments = Comments.query.filter_by(post_id=id).all()  
    return render_template('details.html', post=post, comments=comments)

@app.route('/update_post/<int:id>')
def update_post(id):
    data = Posts.query.get(id)
    if data:
        return render_template('update_post.html', data=data)
    return redirect('/home')

@app.route('/post_update/<int:id>', methods=["POST"])
def post_update_blog_post(id):
    data = Posts.query.get(id)
    if data:
        data.title = request.form.get("title")
        data.content = request.form.get("content")
        data.publication = request.form.get("publication")
        db.session.commit()
    return redirect('/home')

@app.route('/post_comment/<int:post_id>', methods=["POST"])
def post_comment(post_id):
    content = request.form.get("content")
    user_id = session.get('user_id')
    if content and user_id:
        new_comment = Comments(content=content, user_id=user_id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(f'/post_details/{post_id}')  

@app.route('/comment/<int:post_id>')
def comment(post_id):
    return render_template('comment.html', post_id=post_id)

@app.route('/delete_comment/<int:comment_id>/<int:post_id>')
def delete_comment(comment_id, post_id):
    comment = Comments.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return redirect(f'/post_details/{post_id}') 

@app.route('/notes')
def notes(): 
    user_id = session.get('user_id')
    if user_id:
        data = Notes.query.filter_by(user_id=user_id).all()
        return render_template('notes.html', data=data)
    return redirect('/login')

@app.route('/delete_note/<int:id>')
def delete_note(id):
    note = Notes.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect('/notes')

@app.route('/post_notes', methods=["POST"])
def post_notes():
    content = request.form.get("content")
    user_id = session.get('user_id')
    if content and user_id:
        new_notes = Notes(content=content, user_id=user_id)
        db.session.add(new_notes)
        db.session.commit()
    return redirect('/notes')

@app.route('/story')
def story():
    data = Story.query.all()  
    return render_template('story.html', data=data)

@app.route('/delete_story/<int:id>')
def delete_story(id):
    story = Story.query.get(id)
    if story:
        db.session.delete(story)
        db.session.commit()
    return redirect('/story')

@app.route('/post_story', methods=["POST"])
def post_story():
    content = request.form.get("content")
    user_id = session.get('user_id')
    if content and user_id:
        new_story = Story(content=content, story_id=user_id)  
        db.session.add(new_story)
        db.session.commit()
    return redirect('/story')

@app.route('/report_post/<int:post_id>')
def report_post(post_id):
    post = Posts.query.get(post_id)
    data = Reports.query.filter_by(post_id=post_id).all()
    return render_template('reports.html', post=post, data=data)

@app.route('/submit_report/<int:post_id>', methods=["POST"])
def submit_report(post_id):
    reason = request.form.get("reason")
    if reason:
        new_report = Reports(post_id=post_id, reason=reason)
        db.session.add(new_report)
        db.session.commit()
    return redirect(f'/report_post/{post_id}')

@app.route('/event')  
def events():       
    data = Events.query.all()  
    return render_template('events.html', data=data)

@app.route('/delete_events/<int:id>')
def delete_events(id):
    events = Events.query.get(id)
    if events:
        db.session.delete(events)
        db.session.commit()
    return redirect('/event')

@app.route('/post_events', methods=["POST"])
def post_events():
    title = request.form.get("title")
    user_id = session.get('user_id')
    description = request.form.get("description") 
    if title and user_id and description:
        new_events = Events(title=title, description=description, user_id=user_id)
        db.session.add(new_events)
        db.session.commit()
    return redirect('/event')

@app.route('/feedback')
def feedback():
    user_id = session.get('user_id')
    if user_id:
        data = Website_Feedback.query.all()  
        return render_template('feedback.html', data=data)
    return redirect('/feedbacks')

@app.route('/post_feedback', methods=["POST"])
def post_feedback():
    content = request.form.get("content")
    if content:
        new_feedback = Website_Feedback(content=content)
        db.session.add(new_feedback)
        db.session.commit()
    return redirect('/feedback')

@app.route('/chat')
def chat():
    data = Global_Messages.query.all()  
    return render_template('chat.html', data=data)  

@app.route('/delete_message/<int:id>')
def delete_message(id):
    message = Global_Messages.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
    return redirect('/chat')

@app.route('/post_chat_message', methods=['POST'])
def post_chat_message():
    content = request.form.get('content')
    user_id = session.get('user_id')
    if content and user_id:
        new_message = Global_Messages(content=content, messages_id=user_id)
        db.session.add(new_message)
        db.session.commit()
    return redirect('/chat') 

@app.route('/profile')  
def profiles():           
    user_id = session.get('user_id')
    if user_id:
        data = Profile.query.filter_by(user_id=user_id).first()
        current_user = User.query.get(user_id) 
        return render_template('profile.html', data=data, current_user=current_user)
    return redirect('/profile')

@app.route('/post_bio', methods=["POST"])
def post_bio():
    user_id = session.get('user_id')
    bio = request.form.get("bio")
    if user_id and bio: 
        new_profile = Profile(user_id=user_id, bio=bio) 
        db.session.add(new_profile)
        db.session.commit()
    return redirect('/profile')

@app.route('/update_profile')
def update_profile():
    user_id = session.get('user_id')
    if user_id:
        profile = Profile.query.filter_by(user_id=user_id).first()
        return render_template('update_profile.html', profile=profile)
    return redirect('/profile')

@app.route('/post_update_profile', methods=["POST"])
def post_update_profile():
    user_id = session.get('user_id')
    data = Profile.query.filter_by(user_id=user_id).first()
    if user_id and data:
        data.bio = request.form.get("bio")
        db.session.commit()
    return redirect('/profile')

@app.route('/birthdays')  
def birthdays():           
    user_id = session.get('user_id')
    if user_id:
        data = Birthdays.query.filter_by(user_id=user_id).first()
        current_user = User.query.get(user_id) 
        return render_template('birthdays.html', data=data, user=current_user)
    return redirect('/birthdays')  

@app.route('/update_birthday')
def update_birthday():
    user_id = session.get('user_id')
    birthday = Birthdays.query.filter_by(user_id=user_id).first()
    if birthday:
        return render_template('update_birthday.html', birthday=birthday)
    return redirect('/birthdays') 

@app.route('/post_update_birthday', methods=["POST"])
def post_update_birthday():
    user_id = session.get('user_id')
    birthday = Birthdays.query.filter_by(user_id=user_id).first()
    if birthday:
        birthday.title = request.form.get("title")
        birthday.birthday_date = request.form.get("birthday_date")
        db.session.commit()
    return redirect('/birthdays')

@app.route('/post_birthdays', methods=["POST"])
def post_birthdays():
    title = request.form.get("title")
    user_id = session.get('user_id')
    birthday_date = request.form.get("birthday_date")
    if title and user_id and birthday_date:
        new_birthday = Birthdays(title=title, birthday_date=birthday_date, user_id=user_id)
        db.session.add(new_birthday)
        db.session.commit()
    return redirect('/birthdays')

@app.route('/followers')
def followers():
    user_id = session.get('user_id')
    if user_id:
        data = Followers.query.filter_by(user_id=user_id).all()
        return render_template('followers.html', data=data)
    return redirect('/login')

@app.route('/delete_follower/<int:id>')
def delete_follower(id):
    follower = Followers.query.get(id)
    if follower:
        db.session.delete(follower)
        db.session.commit()
    return redirect('/followers')

@app.route('/post_followers', methods=["POST"])
def post_followers():
    user_name = request.form.get("user_name")  
    user_id = session.get('user_id')
    valid_user = User.query.filter_by(user_name=user_name).first() 
    existing_follower = Followers.query.filter_by(user_id=user_id, user_name=user_name).first()
    if user_name and user_id and valid_user and not existing_follower:
        new_follower = Followers(user_id=user_id, user_name=user_name)
        db.session.add(new_follower)
        db.session.commit()
    return redirect('/followers')

if __name__ == '__main__':
    app.run()