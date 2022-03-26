from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm
from flask_login.utils import login_required
from flask_login import current_user

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'



@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    sform = SortForm()
    if sform.validate_on_submit():
        if sform.order.data == 1:
            posts = Post.query.order_by(Post.happiness_level.desc())
        elif sform.order.data == 2:
            posts = Post.query.order_by(Post.likes.desc())
        elif sform.order.data == 3:
            posts = Post.query.order_by(Post.title.desc())
        elif sform.order.data == 4:
            posts = Post.query.order_by(Post.timestamp.desc())
    if sform.displayonlyme.data == True:
            posts = Post.query.order_by(current_user.get_user_posts())

    return render_template('index.html', title="Smile Portal", posts=posts.all(), posttotal=posts.count(), form = sform)


@bp_routes.route('/postsmile', methods=['GET', 'POST'])
@login_required
def postsmile():
    pform = PostForm()
    if pform.validate_on_submit():
        newPost = Post(title = pform.title.data, body = pform.body.data, tags = pform.tag.data, user_id = current_user.id)
        db.session.add(newPost)
        db.session.commit()
        flash('Post "' + newPost.title + '" is created')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form = pform)

@bp_routes.route('/like/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    thepost = Post.query.filter_by(id=post_id).first()
    thepost.likes += 1
    db.session.commit()
    return redirect(url_for('routes.index'))


@bp_routes.route('/delete/<post_id>', methods=['DELETE', 'POST'])
@login_required
def deletepost(post_id):
    dpost = Post.query.filter_by(id=post_id)
    