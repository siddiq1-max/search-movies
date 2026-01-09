from flask import Flask, render_template, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

def init_db():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            year TEXT,
            rating TEXT
        )
    """)
    con.commit()
    con.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    movie = request.args.get("movie")

    if not movie:
        return jsonify({"error": "Please enter a movie name"})

    try:
        url = f"https://api.tvmaze.com/search/shows?q={movie}"
        res = requests.get(url).json()

        if not res:
            return jsonify({"error": "No movie found"})

        show = res[0]["show"]

        title = show["name"]
        year = show["premiered"][:4] if show["premiered"] else "N/A"
        rating = show["rating"]["average"] if show["rating"]["average"] else "N/A"
        poster = show["image"]["medium"] if show["image"] else ""

        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("INSERT INTO movies(title,year,rating) VALUES(?,?,?)",
                    (title, year, str(rating)))
        con.commit()
        con.close()

        return jsonify({
            "title": title,
            "year": year,
            "rating": rating,
            "poster": poster
        })

    except:
        return jsonify({"error": "Server error"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

