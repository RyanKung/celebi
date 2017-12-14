run:
	python -m celebi
test:
	python -m tests --log-level INFO --test-timeout 120
up:
	cd Docker; docker-compose up
