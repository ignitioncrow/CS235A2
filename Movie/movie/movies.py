from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import Movie.adapters.repository as repo
import Movie.movie.services as services

from Movie.authentication.authentication import login_required



# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies_by_rank', methods=['GET'])
def movies_by_rank():
    target_rank = request.args.get('rank')
    movie_to_show_comments = request.args.get('view_comments_for')

    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_rank is None:
        target_rank = first_movie['rank']
    else:
        target_rank = int(target_rank)

    if movie_to_show_comments is None:
        movie_to_show_comments = -1
    else:
        movie_to_show_comments = int(movie_to_show_comments)

    movies, previous_rank, next_rank = services.get_movie_by_rank(target_rank, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        if previous_rank is not None:
            prev_movie_url = url_for('movies_bp.movies_by_rank', rank=previous_rank)
            first_movie_url = url_for('movies_bp.movies_by_rank', rank=first_movie['rank'])

        if next_rank is not None:
            next_movie_url = url_for('movies_bp.movies_by_rank', rank=next_rank)
            last_movie_url = url_for('movies_bp.movies_by_rank', rank=last_movie['rank'])

        for movie in movies:
            movie['view_comment_url'] = url_for('movies_bp.movies_by_rank', rank=target_rank, view_comments_for=movie['rank'])
            movie['add_comment_url'] = url_for('movies_bp.comment_on_movie', movie=movie['rank'])

        return render_template(
            'news/articles.html',
            title='Movies',
            movies=movies,
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_comments_for_movie=movie_to_show_comments)

    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new comment.
        services.add_comment(movie_id, form.comment.data, username, repo.repo_instance)

        # Retrieve the article in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movies_bp.movies_by_rank', rank=movie['rank'], view_comments_for=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the article id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'news/comment_on_article.html',
        title='Edit movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.comment_on_movie'),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    movie_id = HiddenField("Movie rank")
    submit = SubmitField('Submit')

