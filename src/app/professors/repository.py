from src.models import ProfessorModel

def fetch_professors_by_department(department_id):
    items = [e.to_dict() for e in ProfessorModel.query(departmentId=department_id).limit(10000)]
    return items

def fetch_professor(department_id, professor_id):
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    return professor.to_dict()

def add_professor(professor):
    professor = ProfessorModel(**professor)
    professor.save()

def update_professor(professor_id, data):
    department_id = data.get('departmentId')
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    professor.update(**data)
    professor.save()

def remove_professor(department_id, professor_id):
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    professor.delete()