# Image Processing Lab

## Project files
- `app.py`: Flask routes and application startup.
- `backend.py`: OpenCV image processing operations and helper functions.
- `requirements.txt`: Python dependencies.
- `templates/index.html`: Frontend HTML, CSS, and JavaScript.

## Run locally (Windows / PyCharm)
1. Open a terminal in this folder.
2. Install dependencies:
   `python -m pip install -r requirements.txt`
3. Start the website:
   `python app.py`
4. Open `http://127.0.0.1:5000/lab`.

## PythonAnywhere notes
Upload `app.py`, `backend.py`, `requirements.txt`, and the `templates` folder.
Install the requirements in a virtual environment, then configure the WSGI file to import:
`from app import app as application`
Set the virtualenv path in the Web tab and click Reload.

The application accepts uploads up to 12 MB. Confirm that all dependencies install successfully on your selected hosting plan.
