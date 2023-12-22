format:
	black .
	mypy --install-types --explicit-package-bases --ignore-missing-imports .
	pylint --rcfile=${HOME}/.pylintrc .