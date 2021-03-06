from flask import Blueprint, render_template
from app import db
from models import Post, Tag

from flask import request, url_for, redirect
from .forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')

# http://localhost/blog/create
@posts.route('/create', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            print('Something went wrong', e)

        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)

# http://localhost.blog/first-post
@posts.route('/')
def index():
    q = request.args.get('q')

    posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all() if q \
        else Post.query.order_by(Post.created.desc())

    return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


# http://localhost.blog/tag/python
@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)
