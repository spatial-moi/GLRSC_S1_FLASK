import os
import load_dotenv
from src.__init__ import create_app

load_dotenv.load_dotenv()
app = create_app(os.getenv("CONFIG_MODE"))



if __name__ == "__main__":
    app.run(debug=True)
