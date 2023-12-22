format:
	black .
	mypy --config-file ./formatting_configs/mypy.ini .
	pylint --rcfile=./formatting_configs/.pylintrc .

run_db:
	docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres