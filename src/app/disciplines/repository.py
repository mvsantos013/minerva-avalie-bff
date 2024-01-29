import boto3
import json
import pandas as pd
from uuid import uuid4
from flask import request as req
from datetime import datetime, timezone
from src.constants import SERVICE_NAME, ENV
from src.app.models import (DisciplineModel, DisciplineProfessorModel, ProfessorModel, 
    DisciplineTestimonialModel, ProfessorTestimonialModel, DepartmentModel,
    DisciplineRatingModel, ProfessorRatingModel, DisciplineRatingSummaryModel, ReportedDisciplineTestimonialModel)


def fetch_disciplines(department_id):
    items = [e.to_dict() for e in DisciplineModel.query(departmentId=department_id).limit(10000)]
    return items

def fetch_discipline(department_id, discipline_id):
    discipline = DisciplineModel.get(departmentId=department_id, id=discipline_id)
    return discipline.to_dict()

def fetch_discipline_professors(department_id, discipline_id):
    id = f'{department_id}:{discipline_id}'
    disciplines_professors = DisciplineProfessorModel.ByDiscipline.query(departmentIdDisciplineId=id).limit(1000)
    professors = []
    for discipline_professor in disciplines_professors:
        professor = ProfessorModel.get(id=discipline_professor.professorId)
        professors.append(professor.to_dict())
    return professors

def fetch_discipline_testimonials(department_id, discipline_id):
    testimonials = []
    user_id = req.user.get('id') if req.user else None 
    for testimonial in DisciplineTestimonialModel.query(disciplineId=discipline_id).limit(10000):
        testimonial = testimonial.to_dict()
        if(testimonial.get('anonymous') is True):
            testimonial['studentName'] = 'Anônimo'
            if(testimonial['studentId'] != user_id): # Hide ids that are not the user's
                testimonial['studentId'] = None
        testimonials.append(testimonial)
    return testimonials

def add_discipline(department_id, discipline):
    discipline['id'] = str(uuid4())
    discipline = DisciplineModel(**discipline)
    discipline.save()

def add_discipline_from_csv(file):
    df = pd.read_csv(file, sep=',')
    if(sorted(df.columns) != sorted(['id', 'departmentId', 'name', 'description'])):
        raise Exception('Invalid CSV file.')
    departments = [e.id for e in DepartmentModel.scan().limit(10000)]
    if(not all([e in departments for e in df.departmentId.unique()])):
        deps = [e for e in df.departmentId.unique() if e not in departments]
        raise Exception(f'Departamento(s) inexistente(s): {deps}.')

    rows = df.to_dict('records')
    DisciplineModel.put_batch(*rows)
    
def update_discipline(department_id, discipline_id, data):
    data['id'] = discipline_id
    discipline = DisciplineModel.get(departmentId=department_id, id=discipline_id)
    discipline.update(**data)
    discipline.save()

def remove_discipline(department_id, discipline_id):
    discipline = DisciplineModel.get(departmentId=department_id, id=discipline_id)
    discipline.delete()

def fetch_student_evaluation(discipline_id, professor_id, period, student_id):
    discipline_rating = DisciplineRatingModel.get(disciplineIdProfessorIdPeriod=f'{discipline_id}:{professor_id}:{period}', studentId=student_id)
    professor_rating = ProfessorRatingModel.get(disciplineIdProfessorIdPeriod=f'{discipline_id}:{professor_id}:{period}', studentId=student_id)
    discipline_testimonial = DisciplineTestimonialModel.get(disciplineId=discipline_id, professorIdStudentId=f'{professor_id}:{student_id}')
    professor_testimonial = ProfessorTestimonialModel.get(disciplineIdProfessorId=f'{discipline_id}:{professor_id}', studentId=student_id)
    return {
        'disciplineRatings': discipline_rating.to_dict() if discipline_rating else None,
        'professorRatings': professor_rating.to_dict() if professor_rating else None,
        'disciplineTestimonial': discipline_testimonial.to_dict() if discipline_testimonial else None,
        'professorTestimonial': professor_testimonial.to_dict() if professor_testimonial else None
    }

def post_evaluation(data, user):
    professor_id = data.get('professorId')
    discipline_id = data.get('disciplineId')
    discipline_department_id = data.get('disciplineDepartmentId')
    period = data.get('period')
    student_id = user['id']
    student_name = user['name']
    discipline_testimonial_text = data.get('disciplineTestimonial', '')[:255]
    professor_testimonial_text = data.get('professorTestimonial', '')[:255]

    rating_params = {
        'disciplineIdProfessorIdPeriod': f'{discipline_id}:{professor_id}:{period}',
        'disciplineId': discipline_id,
        'disciplineDepartmentId': discipline_department_id,
        'professorId': professor_id,
        'period': period,
        'studentId': student_id,
        'studentName': student_name,
        'createdAt': datetime.now().isoformat()
    }

    testimonial_params = {
        'createdAt': datetime.now().isoformat(),
        'studentId': student_id,
        'studentName': student_name,
        'disciplineId': discipline_id,
        'disciplineDepartmentId': discipline_department_id,
        'professorId': professor_id,
        'anonymous': False,
    }

    discipline_rating = {
        **rating_params,
        'ratings': data.get('disciplineRatings')
    }

    professor_rating = {
        **rating_params,
        'ratings': data.get('professorRatings')
    }

    discipline_testimonial = {
        **testimonial_params,
        'professorIdStudentId': f'{professor_id}:{student_id}',
        'text': discipline_testimonial_text
    }

    professor_testimonial = {
        **testimonial_params,
        'disciplineIdProfessorId': f'{discipline_id}:{professor_id}',
        'text': professor_testimonial_text
    }

    DisciplineRatingModel(**discipline_rating).save()
    ProfessorRatingModel(**professor_rating).save()

    if(discipline_testimonial_text.strip() != ''):
        DisciplineTestimonialModel(**discipline_testimonial).save()
    if(professor_testimonial_text.strip() != ''):
        ProfessorTestimonialModel(**professor_testimonial).save()

    client = boto3.client('lambda')
    client.invoke(
        FunctionName=f'{SERVICE_NAME}-{ENV}-aggregator',
        InvocationType='Event',
        Payload=json.dumps({
            'professorId': professor_id,
            'disciplineId': discipline_id,
            'disciplineDepartmentId': discipline_department_id,
        })
    )

    return True

def fetch_discipline_ratings(discipline_id):
    items = [e.to_dict() for e in DisciplineRatingSummaryModel.query(disciplineId=discipline_id).limit(10000)]
    return items


def remove_testimonial(testimonial):
    id = f"{testimonial['professorId']}:{testimonial['studentId']}"
    item = DisciplineTestimonialModel.get(disciplineId=testimonial['disciplineId'], professorIdStudentId=id)
    # Only the own user can remove its testimonial
    if(item.studentId != req.user.get('id')):
        raise Exception('Unauthorized')
    item.delete()

def report_testimonial(testimonial):
    testimonial['reportedAt'] = datetime.now(timezone.utc).isoformat()
    testimonial = ReportedDisciplineTestimonialModel(**testimonial)
    testimonial.save()
    return testimonial.to_dict()

def fetch_reported_testimonials():
    testimonials = []
    for testimonial in ReportedDisciplineTestimonialModel.scan().limit(10000):
        testimonial = testimonial.to_dict()
        if(testimonial.get('anonymous') is True):
            testimonial['studentName'] = 'Anônimo'
            testimonial['studentId'] = None
        testimonials.append(testimonial)
    return testimonials

def approve_reported_testimonial(testimonial):
    testimonial = ReportedDisciplineTestimonialModel.get(disciplineIdProfessorId=testimonial.disciplineIdProfessorId, createdAt=testimonial.createdAt)
    testimonial.delete()

def remove_reported_testimonial(testimonial):
    reported_testimonial = ReportedDisciplineTestimonialModel.get(disciplineIdProfessorId=testimonial.disciplineIdProfessorId, createdAt=testimonial.createdAt)
    reported_testimonial.delete()
    testimonial = DisciplineTestimonialModel.get(disciplineIdProfessorId=testimonial.disciplineIdProfessorId, createdAt=testimonial.createdAt)
    testimonial.delete()