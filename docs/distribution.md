## Distribution

Package your app as a standalone executable using **PyInstaller** or **PyVan**:

```bash
pyinstaller -w -F main.py
```

After packaging, move your templates, static files, etc. into the `dist` folder or include them via `--add-data` flag:

```bash
pyinstaller --name your-app-name --add-data "templates:templates" --add-data "static:static" gui.py
```

For Linux desktop app distribution, explore:

* [cacao-accounting-flatpak](https://github.com/mammhoud/cacao-accounting-flatpak)
* [cacao-accounting-snap](https://github.com/mammhoud/cacao-accounting-snap)


