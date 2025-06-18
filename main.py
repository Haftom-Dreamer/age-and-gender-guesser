from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["username"]
        return guess(name)
    return render_template("form.html")

def guess(name):
    try:
        agify_url = "https://api.agify.io"
        genderize_url = "https://api.genderize.io"

        age_response = requests.get(agify_url, params={"name": name})
        gender_response = requests.get(genderize_url, params={"name": name})

        age_response.raise_for_status()
        gender_response.raise_for_status()

        age_data = age_response.json()
        gender_data = gender_response.json()

        guessed_age = age_data.get("age", "unknown")
        guessed_gender = gender_data.get("gender", "unknown")

        return render_template(
            "form.html",
            na=name.title(),
            age=guessed_age,
            gender=guessed_gender.title() if guessed_gender else "Unknown"
        )
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)