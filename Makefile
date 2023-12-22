format:
	black .
	mypy --config-file ./formatting_configs/mypy.ini .
	pylint --rcfile=./formatting_configs/.pylintrc .


run-server:
	export DATABASE_URL=postgresql://postgres:password@localhost:5432/postgres
	docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres