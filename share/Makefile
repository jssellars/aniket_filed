all:
	# prevent running make without arguments from running the first target

.PHONY: uwsgi-nginx-flask
uwsgi-nginx-flask:
	# from tiangolo/uwsgi-nginx-flask:python3.7
	/start.sh

.PHONY: rabbit_worker
rabbit_worker:
	python3 rabbit_worker.py

.PHONY: sync_job
sync_job:
	python3 sync_job.py
