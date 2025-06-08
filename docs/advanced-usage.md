
## Advanced Usage

You can supply any web framework by passing a custom server function:

```python
def start_flask(**server_kwargs):
    app = server_kwargs.pop("app", None)
    server_kwargs.pop("debug", None)

    try:
        import waitress
        waitress.serve(app, **server_kwargs)
    except ImportError:
        app.run(**server_kwargs)

if __name__ == "__main__":
    FlaskUI(
        server=start_flask,
        server_kwargs={"app": app, "port": 3000, "threaded": True},
        width=800,
        height=600,
    ).run()
```

Example with [NiceGUI](https://nicegui.io/):

```python
from flaskwebgui import FlaskUI
from nicegui import ui

ui.label("Hello Super NiceGUI!")
ui.button("BUTTON", on_click=lambda: ui.notify("button was pressed"))

def start_nicegui(**kwargs):
    ui.run(**kwargs)

if __name__ in {"__main__", "__mp_main__"}:
    FlaskUI(
        server=start_nicegui,
        server_kwargs={"dark": True, "reload": False, "show": False, "port": 3000},
        width=800,
        height=600,
    ).run()
```

---

## Close Application Using a Route

You can close the app programmatically:

```python
from flaskwebgui import close_application

@app.route("/close", methods=["GET"])
def close_window():
    close_application()
```

Add a close link in your HTML:

```html
<a href="/close" class="exit" role="button">CLOSE</a>
```

---

## Prevent Users from Opening Browser Console

Add this script in your HTML to block F12 and right-click:

```html
<script>
    // Prevent F12 key
    document.onkeydown = function (e) {
        if (e.key === "F12") {
            e.preventDefault();
        }
    };

    // Prevent right-click
    document.addEventListener("contextmenu", function (e) {
        e.preventDefault();
    });
</script>
```

---
