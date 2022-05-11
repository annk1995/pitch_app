from . import main
from .. import db
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Pitch, Comment, UpVote, DownVote
from .forms import PitchForm, CommentForm


@main.route('/')
@login_required
def index():
    return render_template("index.html", user=current_user)


@main.route('/new_pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        content = form.content.data
        user_id = current_user._get_current_object().id
        new_pitch_obj = Pitch(title=title, category=category, content=content, user_id=user_id)
        db.session.add(new_pitch_obj)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('new_pitch.html', form=form)


@main.route('/pitches')
@login_required
def pitches():
    pitches = Pitch.query.all()
    for pitch in pitches:
        print(pitch.content)
    return render_template('display_pitch.html', pitches=pitches)


@main.route('/comment/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    comments = Comment.query.filter_by(pitch_id=pitch_id)
    pitch = Pitch.query.get(pitch_id)
    user_id = current_user._get_current_object().id
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment_obj = Comment(comment=comment, user_id=user_id, pitch_id=pitch_id)
        db.session.add(new_comment_obj)
        db.session.commit()
        return redirect(url_for('main.new_comment', pitch_id=pitch_id))
    return render_template('comment.html', comments=comments, pitch=pitch, form=form)


@main.route('/like/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    new_upvote = UpVote(pitch=pitch, upvote=1)
    db.session.add(new_upvote)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/dislike/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    new_downvote = DownVote(pitch=pitch, downvote=1)
    db.session.add(new_downvote)
    db.session.commit()
    return redirect(url_for('main.index'))

# @main.route('/_post_vote/<pitch_id>/<action_vote>', methods=['POST', 'GET'])
# @login_required
# def _post_vote(pitch_id, action_vote):
#     pitch = Pitch.query.filter_by(id=pitch_id).first_or_404()
#     vote = PostVote.query.filter_by(user=current_user, pitch=pitch).first()
#     if vote:
#         if vote.upvote != bool(int(action_vote)):
#             vote.upvote = bool(int(action_vote))
#             db.session.commit()
#             return redirect(url_for('app.main.new_pitch', pitch_id=pitch.id))
#         else:
#             flash('You already vote for this post')
#             return redirect(url_for('app.main._post_vote', action_vote=action_vote, pitch_id=pitch.id))
#
#     vote = PostVote(user=current_user, pitch=pitch, upvote=bool(int(action_vote)))
#     db.session.add(vote)
#     db.session.commit()
#     flash('Thx for voting')
#     return redirect(url_for('app.main.new_pitch', pitch_id=pitch.id))