from uuid import uuid4
from src.models import DepartmentModel, ProfessorModel


def fetch_departments():
    items = [e.to_dict() for e in DepartmentModel.scan().limit(10000)]
    return items

def fetch_department(department_id):
    department = DepartmentModel.get(id=department_id)
    return department.to_dict()

def add_department(department):
    department['id'] = str(uuid4())
    department = DepartmentModel(**department)
    department.save()

def update_department(department_id, data):
    data['id'] = department_id
    department = DepartmentModel.get(id=department_id)
    department.update(**data)
    department.save()

def remove_department(department_id):
    professors = ProfessorModel.query(departmentId=department_id).count()
    if(professors > 0):
        raise Exception('Departmento não pode ser deletado, pois há professores vinculados a ele.')
    department = DepartmentModel.get(id=department_id)
    department.delete()