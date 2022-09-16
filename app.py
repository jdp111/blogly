"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "Shoutitfromthemountaintopzarathustra"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def frontPage():
    table = User.query.order_by(User.last_name, User.first_name ).all()
    return render_template('Main.html', users = table)


@app.route('/users/new')
def userInPage():
    return render_template('NewUser.html')


@app.route('/users/new', methods = ['POST'])
def addNew():
    result = request.form
    first = result['first']
    last = result['last']
    image = result['image']
    
    if not first or not last:
        flash("must include first and last name")
        return redirect('/users/new')
    
    if (User.query.filter_by(first_name = first, last_name = last).all()):
        flash("user already exists")
        return redirect('/users/new')

    if not image:
        image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-Y5t0_YAP2Kak3u5WA-TFTzY1zOu3C5Bfjw&usqp=CAU'

    newUser = User(first_name = first, last_name = last, image_url = image)
    db.session.add(newUser)
    db.session.commit()

    return redirect('/')


@app.route('/users/<userID>')
def userpage(userID):
    Data = User.query.get_or_404(userID)
    posts = Data.post
    return render_template('user_page.html', userData = Data, id = userID, userPosts = posts)


@app.route('/users/<userID>/delete', methods = ['POST'])
def deleteUser(userID):
    userData = User.query.get_or_404(userID)

    db.session.delete(userData)
    db.session.commit()

    return redirect('/')


@app.route('/users/<userID>/edit', methods = ['POST'])
def editUser(userID):
    userData = User.query.get_or_404(userID)
    result = request.form
    first = result['first']
    last = result['last']
    image = result['image']

    userData.first_name = first
    userData.last_name = last
    userData.image_url = image

    db.session.commit()

    return redirect("/")


@app.route('/users/<userID>/edit')
def editUserPage(userID):
    Data = User.query.get_or_404(userID)
    return render_template('edit_user.html', userData = Data)


@app.route("/users/<userID>/posts/new", methods = ['POST'])
def addPost(userID):
    Data = User.query.get_or_404(userID)
    result = request.form
    newtitle = result['title']
    newcontent = result['content']
    
    if not newcontent or not newtitle:
        flash("Must include title and content")
        return redirect(f"/users/{userID}/posts/new")
    
    newPost = Post(title = newtitle, content = newcontent, user_id = userID)
    db.session.add(newPost)
    db.session.commit()

    Posts = Data.post
    return redirect(f"/users/{userID}")


@app.route('/users/<userID>/posts/new')
def newPost(userID):
    return render_template('new_post.html', userid = userID)


@app.route('/posts/<postID>')
def singlePost(postID):
    singlePost = Post.query.get_or_404(postID)
    return render_template('show_post.html', Post = singlePost, author = singlePost.user)


@app.route('/posts/<postID>/edit')
def editPost(postID):
    singlePost = Post.query.get_or_404(postID)
    return render_template('edit_post.html', post = singlePost)


@app.route('/posts/<postID>/edit', methods = ['POST'])
def confirmEdit(postID):
    result = request.form
    newtitle = result['title']
    newcontent = result['content']

    if not newcontent or not newtitle:
        flash("Must include title and content")
        return redirect(f"/posts/{postID}/edit")
    

    singlePost = Post.query.get_or_404(postID)

    singlePost.title = newtitle
    singlePost.content = newcontent
    db.session.commit()
    return redirect(f"/posts/{postID}")


@app.route('/posts/<postID>/delete',methods = ['POST'])
def deletePost(postID):
    postData = Post.query.get_or_404(postID)
    userID = postData.user.id
    db.session.delete(postData)
    db.session.commit()
    return redirect(f"/users/{userID}")
    