.PHONY: .all
all:
	# prevent running make without arguments from running the first target

.PHONY: uwsgi-nginx-flask
uwsgi-nginx-flask:
	# from tiangolo/uwsgi-nginx-flask:python3.7
	/start.sh

.PHONY: test
test:
	pytest --capture=no --disable-warnings -v tests
