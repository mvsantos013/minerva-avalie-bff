from uuid import uuid4
from src.app.departments.models import DepartmentModel
from src.app.professors.models import ProfessorModel


def fetch_departments(organization_id):
    items = [e.to_dict() for e in DepartmentModel.query(organizationId=organization_id).limit(10000)]
    return items

def fetch_department(organization_id, department_id):
    department = DepartmentModel.get(organizationId=organization_id, id=department_id)
    return department.to_dict()

def add_department(organization_id, department):
    department['id'] = str(uuid4())
    department = DepartmentModel(organizationId=organization_id, **department)
    department.save()

def update_department(organization_id, department_id, data):
    data['id'] = department_id
    department = DepartmentModel.get(organizationId=organization_id, id=department_id)
    department.update(**data)
    department.save()

def remove_department(organization_id, department_id):
    professors = ProfessorModel.query(departmentId=department_id).count()
    if(professors > 0):
        raise Exception('Departmento não pode ser deletado, pois há professores vinculados a ele.')
    department = DepartmentModel.get(organizationId=organization_id, id=department_id)
    department.delete()