from uuid import uuid4
from src.app.disciplines.models import DisciplineModel
from src.app.professors.models import ProfessorModel, ProfessorDisciplineModel


def fetch_disciplines(organization_id):
    items = [e.to_dict() for e in DisciplineModel.query(organizationId=organization_id).limit(10000)]
    return items

def fetch_discipline(organization_id, discipline_id):
    discipline = DisciplineModel.get(organizationId=organization_id, id=discipline_id)
    return discipline.to_dict()

def add_discipline(organization_id, discipline):
    discipline['id'] = str(uuid4())
    discipline = DisciplineModel(**discipline)
    discipline.save()

def update_discipline(organization_id, discipline_id, data):
    data['id'] = discipline_id
    discipline = DisciplineModel.get(organizationId=organization_id, id=discipline_id)
    discipline.update(**data)
    discipline.save()

def remove_discipline(organization_id, discipline_id):
    professors = ProfessorDisciplineModel.ByDiscipline.query(disciplineId=discipline_id).count()
    if(professors > 0):
        raise Exception('Disciplina não pode ser deletada, pois há professores vinculados a ela.')
    discipline = DisciplineModel.get(organizationId=organization_id, id=discipline_id)
    discipline.delete()