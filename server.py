import os
import load_dotenv
from src.__init__ import create_app

load_dotenv.load_dotenv()
app = create_app(os.getenv("CONFIG_MODE"))


# — bind 0.0.0.0:$PORT

@app.route("/api", methods=["GET"])
def index():
    return {
        "Server Home": "API"
    }


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
