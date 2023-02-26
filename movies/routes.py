import requests
from flask import redirect, render_template, url_for

from movies import app, db
from movies.forms import AddMovieForm, RateMovieForm
from movies.models import Movies

MOVIE_DB_API_KEY = "9efe0b4c-51dc-4f25-a5e8-111b841944d1"
MOVIE_DB_SEARCH_URL = "https://kinopoiskapiunofficial.tech/api/v2.2/films"

headers = {
    "X-API-KEY": MOVIE_DB_API_KEY
}


@app.route("/")
def home():
    all_movies = Movies.query.order_by(Movies.rating.desc()).all()
    index = 0
    for movie in all_movies:
        movie.ranking = index + 1
        index += 1
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit/<int:value>", methods=["GET", "POST"])
def edit(value):
    update_form = RateMovieForm()
    movie_to_update = Movies.query.filter_by(id=value).first()
    if update_form.validate_on_submit():
        movie_to_update.rating = update_form.rating.data
        movie_to_update.review = update_form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=update_form, movie=movie_to_update)


@app.route("/delete/<int:value>")
def delete(value):
    movie_to_delete = Movies.query.filter_by(id=value).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        movie_title = add_form.movie_title.data
        search_params = {
            "keyword": movie_title,
        }
        resp = requests.get(url=MOVIE_DB_SEARCH_URL, headers=headers, params=search_params)
        search_data = resp.json()["items"]
        return render_template("select.html", data=search_data)
    return render_template("add.html", form=add_form)


@app.route("/find/<int:value>")
def find_movie(value):
    movie_id = value
    movie_api_url = f"{MOVIE_DB_SEARCH_URL}/{movie_id}"
    resp = requests.get(url=movie_api_url, headers=headers)
    search_data = resp.json()
    new_movie = Movies(
        title=search_data["nameRu"],
        year=search_data["year"],
        description=search_data["description"],
        img_url=search_data["posterUrl"]
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("edit", value=new_movie.id))
