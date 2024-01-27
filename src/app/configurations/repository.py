from uuid import uuid4
from src.app.models import ConfigurationModel


def fetch_configurations():
    items = [e.to_dict() for e in ConfigurationModel.scan().limit(10000)]
    return items

def add_configuration(configuration):
    configuration = ConfigurationModel(**configuration)
    configuration.save()

def update_configuration(configuration_id, data):
    data['name'] = configuration_id
    configuration = ConfigurationModel.get(name=configuration_id)
    configuration.update(**data)
    configuration.save()

def remove_configuration(configuration_id):
    configuration = ConfigurationModel.get(name=configuration_id)
    configuration.delete()