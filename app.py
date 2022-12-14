"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag

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
    result = request.form
    newtitle = result['title']
    newcontent = result['content']
    
    if not newcontent or not newtitle:
        flash("Must include title and content")
        return redirect(f"/users/{userID}/posts/new")

    newPost = Post(title = newtitle, content = newcontent, user_id = userID)
    db.session.add(newPost)
    db.session.commit()

    tags = Tag.query.all()
    
    for key, value in result.items():
        
        if value == "on":
            tagID = Tag.query.get(key).id
            newRelation = PostTag(post_id = newPost.id, tag_id =tagID)
            db.session.add(newRelation)
        
    db.session.commit()

    return redirect(f"/users/{userID}")


@app.route('/users/<userID>/posts/new')
def newPost(userID):
    tagOptions = Tag.query.all()
    return render_template('new_post.html', userid = userID, tags = tagOptions)


@app.route('/posts/<postID>')
def singlePost(postID):
    singlePost = Post.query.get_or_404(postID)
    tagList = singlePost.tag

    return render_template('show_post.html', Post = singlePost, author = singlePost.user, tags =tagList )


@app.route('/posts/<postID>/edit')
def editPost(postID):
    singlePost = Post.query.get_or_404(postID)
    tagList = Tag.query.all()
    return render_template('edit_post.html', post = singlePost, tags = tagList)


@app.route('/posts/<postID>/edit', methods = ['POST'])
def confirmEdit(postID):
    result = request.form
    newtitle = result['title']
    newcontent = result['content'] 
    
    if not newcontent or not newtitle:
        flash("Must include title and content")
        return redirect(f"/posts/{postID}/edit")
    
    previousTags = PostTag.query.filter_by(post_id = postID).all()

    for tag in previousTags:
        db.session.delete(tag)
    db.session.commit()

    tags = Tag.query.all()
    
    for key, value in result.items():
        
        if value == "on":
            tagID = Tag.query.get(key).id
            newRelation = PostTag(post_id = postID, tag_id =tagID)
            db.session.add(newRelation)
        
    db.session.commit()
   

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


#add a page for tags
@app.route('/tags')
def getTags():
    tagList = db.session.query(Tag.id, Tag.name).all()
    return render_template('/tag_pages/all_tags.html', tags = tagList)


@app.route('/tags/new')
def addTag():
    return render_template('/tag_pages/add_tag.html')


@app.route('/tags/new', methods = ['POST'])
def submitTag(): 
    tagName = request.form['tag_name']
    newTagObj = Tag(name = tagName)
    db.session.add(newTagObj)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<tagID>')
def showtagInfo(tagID):
    oneTag = Tag.query.get_or_404(tagID)
    relatedPosts = oneTag.post
    return render_template('/tag_pages/single_tag.html', postData = relatedPosts, tag = oneTag)


@app.route('/tags/<tagID>/edit', methods = ['POST'])
def submitEdit(tagID):
    newTag = request.form['tag_name']

    if not newTag:
        flash("tag must not be blank")
        redirect(f"/tags/{tagID}/edit")

    oldTag = Tag.query.get_or_404(tagID)
    oldTag.name = newTag
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<tagID>/edit')
def EditTag(tagID):
    oldTag = Tag.query.get_or_404(tagID)
    return render_template('/tag_pages/edit_tag.html', tag = oldTag )

@app.route('/tags/<tagID>/delete', methods = ['POST'])
def deleteTag(tagID):
    oldTag = Tag.query.get_or_404(tagID)
    db.session.delete(oldTag)
    db.session.commit()
    return redirect('/tags')