setup:
				virtualenv --python=/usr/bin/python env
				env/bin/pip install --target=./enum enum34
				env/bin/pip install --target=./workflow Alfred-Workflow
				rm -rf ./env
