
## Configurations

The main `FlaskUI` class parameters:

| Parameter         | Type              | Description                                   |
| ----------------- | ----------------- | --------------------------------------------- |
| `server`          | `str` or callable | Server start function or preset server string |
| `server_kwargs`   | `dict`            | Keyword args passed to server start function  |
| `app`             | Any               | WSGI or ASGI app instance                     |
| `port`            | `int`             | Specify port; otherwise a free port is chosen |
| `width`           | `int`             | Window width                                  |
| `height`          | `int`             | Window height                                 |
| `fullscreen`      | `bool`            | Start app maximized/fullscreen                |
| `on_startup`      | callable          | Function before starting browser and server   |
| `on_shutdown`     | callable          | Function after browser and server shutdown    |
| `extra_flags`     | `List[str]`       | Additional flags for browser command          |
| `browser_path`    | `str`             | Path to browser executable                    |
| `browser_command` | `List[str]`       | Custom browser launch command                 |
| `socketio`        | Any               | SocketIO instance for Flask-SocketIO          |
| `app_mode`        | `bool`            | Launch browser in app mode (no address bar)   |
| `browser_pid`     | `int`             | PID of launched browser process               |

---
