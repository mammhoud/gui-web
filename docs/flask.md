
## Usage with Flask

Create a simple Flask app (e.g., `main.py`):

```python
from flask import Flask, render_template
from flaskwebgui import FlaskUI

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/home", methods=['GET'])
def home():
    return render_template('some_page.html')

if __name__ == "__main__":
    # For normal debugging in browser:
    # app.run()

    # To run as a desktop app with gui-web:
    FlaskUI(app=app, server="flask").run()
```

> For better performance in production, consider installing and using `waitress`.

---

## Usage with Flask-SocketIO

Example `main.py` with SocketIO support:

```python
from flask import Flask, render_template
from flask_socketio import SocketIO
from flaskwebgui import FlaskUI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/home", methods=['GET'])
def home():
    return render_template('some_page.html')

if __name__ == '__main__':
    FlaskUI(
        app=app,
        socketio=socketio,
        server="flask_socketio",
        width=800,
        height=600,
    ).run()
```

---
