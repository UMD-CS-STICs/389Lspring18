SHELL = /bin/bash

.PHONY: package deploy clean freeze-requirements install-pip-packages zip-deployment-package

# Temporary folder to contruct deployment package in.
FOLDER=deployment

### Makefile Commands ###

# Run `make package` to generete a fresh deployment package.
package: clean create-deployment-folder zip-deployment-package

# Run `make deploy` to automatically deploy your deployment package for you.
deploy: package
	# Name of Lambda functions to deploy to.
	for f in "user-profile-post" "user-profile-get" "user-profile-get-all" "user-profile-delete" "user-profile-put" "user-profile-delete-all"; do \
		aws lambda update-function-code --function-name "$${f}" --zip-file fileb://${FOLDER}_package.zip; \
	done;
	make clean

# Run `make test-handlers` to verify the Lambda handlers work.
test-handlers: start-local-dynamo run-tests stop-local-dynamo

# Run `make test-end-to-end` to test your API end-to-end.
test-end-to-end:
	python test_e2e.py

test: test-handlers test-end-to-end


### Makefile Helpers ###

start-local-dynamo:
	docker run -d -p 8000:8000 dwmkerr/dynamodb

run-tests:
	python test_handlers.py; :

stop-local-dynamo:
	docker stop `docker ps -q --filter ancestor='dwmkerr/dynamodb'`

clean:
	rm -rf ${FOLDER} ${FOLDER}_package.zip

create-deployment-folder:
	mkdir -p ${FOLDER}
	# List of files you want included in the deployment package,
	# excluding pip packages which will automatically be included.
	for f in "users_handlers.py"; do \
		cp $$f ${FOLDER}; \
	done;

freeze-requirements:
	pip freeze > ${FOLDER}/requirements.txt

install-pip-packages:
	cd ${FOLDER} && docker run -e RUNTIME=python3 -v `pwd`:/data myrmex/lambda-packager

zip-deployment-package:
	cd ${FOLDER} && zip -r ../${FOLDER}_package.zip *
