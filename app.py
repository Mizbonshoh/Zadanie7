from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

resume_data = {}
load_dotenv()

def fetch_resume_data():
    """Запрашивю свои данные с GitLab Skillbox API"""
    api_url = "https://gitlab.skillbox.ru/api/v4/user"
    headers = {"PRIVATE-TOKEN": os.getenv("API_TOKEN")}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return {
            "id": user_data.get("id"),
            "name": user_data.get("name"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "web_url": user_data.get("web_url"),
            "created_at": user_data.get("created_at"),
            "roles": user_data.get("current_sign_in_ip"),
        }
    return {"error": "Не удалось получить данные"}


@app.route("/")
def index():
    """Главная страница с резюме"""
    return render_template("resume.html", data=resume_data)


if __name__ == "__main__":
    resume_data = fetch_resume_data()
    app.run(debug=True, host='0.0.0.0', use_reloader=False)