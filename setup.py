from setuptools import setup, find_packages
# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# twine upload * -u __token__ -p pypi-token

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="gui-web",
    version="1.2.2",
    packages=find_packages(where="."),
    description="Create desktop applications with Flask/Django/FastAPI!",
    include_package_data=True,
    license="MIT",
    py_modules=["gui-web"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "colorlog>=6.9.0",
        "dynaconf>=3.2.11",
        "psutil>=7.0.0",
        "structlog>=25.4.0",
        "waitress>=3.0.2",
        "whitenoise>=6.9.0",
    ],
    entry_points={
        "console_scripts": [
            "webgui = web_gui.main:main",  # runs `main()` from `web_gui/main.py`
        ],
    },
)
