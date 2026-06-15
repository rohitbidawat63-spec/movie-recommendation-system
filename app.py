from flask import Flask, render_template, request
import pickle
import webbrowser
import requests
app = Flask(__name__)
movies = pickle.load(open('data.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values

API_KEY = "d09eb084"
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data = requests.get(url).json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return ""



def fetch_poster(movie_name):

    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

        data = requests.get(url).json()

        return data.get("Poster")

    except:
        return ""




def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movie_list:


        movie_title = movies.iloc[i[0]].title


        recommendations.append({
        "title": movie_title,
        "poster": fetch_poster(movie_title)
})

       
    return recommendations

@app.route('/',methods = ['GET','POST'])
def home():

    recommendations = []

    if request.method == 'POST':

        selected_movie = request.form['movie']

        recommendations = recommend(selected_movie)

    return render_template(
        'index.html',
        movies=movie_list,
        recommendations=recommendations
    )
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)