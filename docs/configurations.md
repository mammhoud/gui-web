## Configurations

The main `settings.yaml` env variables and their defaults (based on your YAML snippet):

| Parameter         | Type              | Description                                                                                        | Default Example           |
| ----------------- | ----------------- | -------------------------------------------------------------------------------------------------- | ------------------------- |
| `server`          | `str` or callable | Server start function or preset server string, e.g., `"django"` or a callable that runs the server | `"django"`                |
| `server_kwargs`   | `dict`            | Keyword arguments passed to the server start function                                              | `{}` (optional)           |
| `app`             | Any               | WSGI or ASGI app instance (e.g., `"test.wsgi.application"`)                                        | `"test.wsgi.application"` |
| `port`            | `int`             | Port number on which the server listens                                                            | `3003`                    |
| `width`           | `int`             | Window width in pixels                                                                             | `1020`                    |
| `height`          | `int`             | Window height in pixels                                                                            | `720`                     |
| `fullscreen`      | `bool`            | Whether to start the app in fullscreen or maximized window mode                                    | `true`                    |
| `on_startup`      | `callable`        | Optional function executed before starting the browser and server                                  | `null` (or `None`)        |
| `on_shutdown`     | `callable`        | Optional function executed after browser and server shutdown                                       | `null` (or `None`)        |
| `extra_flags`     | `List[str]`       | Extra command line flags passed to the browser executable                                          | `["--disable-gpu"]`       |
| `browser_path`    | `str` or None     | Path to the browser executable to launch (e.g., Microsoft Edge path)                               | `null` (or `None`)        |
| `browser_command` | `List[str]`       | Custom browser launch command list, overrides default command if specified                         | Not specified             |
| `socketio`        | Any or None       | SocketIO instance, if using Flask-SocketIO integration                                             | `null` (or `None`)        |
| `app_mode`        | `bool`            | If true, launches browser in app mode (no address bar, minimal UI)                                 | `true`                    |
| `browser_pid`     | `int` or None     | Process ID of the launched browser, set internally after launch                                    | `null` (or `None`)        |
| `profile_dir`     | `str` or None     | Browser profile directory path, if needed                                                          | `null` (or `None`)        |
| `exit_after`      | `int` or None     | Number of seconds to wait before exiting the app after startup (used for auto-close scenarios)     | `15`                      |

---

### Notes:

* `server` can be a string like `"django"` for a preset, or a callable function to start a custom server.
* `app` typically points to your WSGI or ASGI app instance, e.g., `"test.wsgi.application"`.
* `extra_flags` helps pass browser-specific flags, like `--disable-gpu` to avoid GPU issues.
* `app_mode` enables kiosk-style browser windows without address bars.
* `exit_after` can be useful for testing or demo apps that should close automatically.
* `on_shutdown` is often overridden in Python code for graceful cleanup.

---

this file could be at base_dir of the web project 
