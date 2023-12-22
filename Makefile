format:
	black .
	mypy --config-file ./formatting_configs/mypy.ini .
	pylint --rcfile=./formatting_configs/.pylintrc .