test:
	pytest .

lint:
	pylint houses_pipeline
	pylint houses_api

install_pipeline_develop:
	pip install -e ./houses_pipeline
