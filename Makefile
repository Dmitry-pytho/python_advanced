run:
	FLASK_APP=app.py FLASK_DEBUG=1 flask run

lint:
	flake8 app.py
