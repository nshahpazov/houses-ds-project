test:
	pytest .

lint:
	pylint houses_pipeline
	pylint houses_api

install_pipeline_develop:
	pip install -e ./houses_pipeline

clean:
	@echo "Cleaning up $(project_name)"
	@rm -rf *.egg-info
	@rm -rf $(raws_to_remove)
	@rm -rf data/**/*.csv
	@rm -rf logs/*.log*