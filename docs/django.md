
## Usage with Django

1. Install dependencies:

```bash
pip install waitress whitenoise
```

2. Configure static and media files in `settings.py`:

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
```

3. Add `WhiteNoiseMiddleware` to your middleware in `settings.py`:

```python
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # other middlewares...
]
```

4. Create a `gui.py` file next to `manage.py`:

```python
from flaskwebgui import FlaskUI
from project_name.wsgi import application as app

if __name__ == "__main__":
    FlaskUI(app=app, server="django").run()
```

5. Run the desktop app:

```bash
python gui.py
```

---
