from uuid import uuid4
from src.app.organizations.models import OrganizationModel
from src.app.departments.models import DepartmentModel


def fetch_organizations():
    items = [e.to_dict() for e in OrganizationModel.scan().limit(10000)]
    return items

def fetch_organization(organization_id):
    organization = OrganizationModel.get(id=organization_id)
    return organization.to_dict()

def add_organization(organization):
    organization['id'] = str(uuid4())
    organization = OrganizationModel(**organization)
    organization.save()

def update_organization(organization_id, data):
    data['id'] = organization_id
    organization = OrganizationModel.get(id=organization_id)
    organization.update(**data)
    organization.save()

def remove_organization(organization_id):
    departments = DepartmentModel.query(organizationId=organization_id).count()
    if(departments > 0):
        raise Exception('Organizationo não pode ser deletada, pois há departamentos vinculados a ela.')
    organization = OrganizationModel.get(id=organization_id)
    organization.delete()