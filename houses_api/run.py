"""Run the flask api"""
from api.app import create_app
from api.config import DevelopmentConfig


application = create_app(config_object=DevelopmentConfig)

# xTODO: add __init__ in the main api module
if __name__ == "__main__":
    application.run()
