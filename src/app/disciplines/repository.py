from uuid import uuid4
from src.app.models import DisciplineModel


def fetch_disciplines(department_id):
    items = [e.to_dict() for e in DisciplineModel.query(departmentId=department_id).limit(10000)]
    return items

def fetch_discipline(department_id, discipline_id):
    discipline = DisciplineModel.get(departmentId=department_id, id=discipline_id)
    return discipline.to_dict()

def add_discipline(department_id, discipline):
    discipline['id'] = str(uuid4())
    discipline = DisciplineModel(**discipline)
    discipline.save()

def update_discipline(department_id, discipline_id, data):
    data['id'] = discipline_id
    discipline = DisciplineModel.get(departmentId=department_id, id=discipline_id)
    discipline.update(**data)
    discipline.save()

def remove_discipline(department_id, discipline_id):
    discipline = DisciplineModel.get(departmentId=department_id, id=discipline_id)
    discipline.delete()