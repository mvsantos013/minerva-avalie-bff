import pandas as pd
from src.app.models import DepartmentModel, DisciplineModel
from src.app.utils import slugify

def fetch_departments():
    items = [e.to_dict() for e in DepartmentModel.scan().limit(10000)]
    return items

def fetch_department(department_id):
    department = DepartmentModel.get(id=department_id)
    return department.to_dict()

def add_department(department):
    department = DepartmentModel(**department)
    department.save()

def add_department_from_csv(file):
    df = pd.read_csv(file)
    if(sorted(df.columns) != sorted(['name'])):
        raise Exception('Invalid CSV file.')
    df['id'] = df['name'].apply(slugify)
    rows = df.to_dict('records')
    DepartmentModel.put_batch(*rows)

def update_department(department_id, data):
    data['id'] = department_id
    department = DepartmentModel.get(id=department_id)
    department.update(**data)
    department.save()

def remove_department(department_id):
    disciplines = DisciplineModel.query(departmentId=department_id).count()
    if(disciplines > 0):
        raise Exception('Departmento não pode ser deletado, pois há disciplinas vinculadas a ele.')
    department = DepartmentModel.get(id=department_id)
    department.delete()