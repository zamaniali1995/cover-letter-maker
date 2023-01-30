create-env:
	@echo "---- Creating Conda Env ----"
	@conda env create -f ./environment.yaml

delete-env:
	@echo "---- Deleting Conda Env ----"
	@conda env remove --name test-env

create-package:
	@echo "---- Creating a package ----"
	@pip3 install -e .

run-server:
	@echo "---- Running Server ----"
	@python3 app/run.py