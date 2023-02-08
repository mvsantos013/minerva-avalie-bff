from uuid import uuid4
from src.models import ProfessorModel
from src.lib.adapters import s3_adapter
from src.constants import BUCKET_FILES

def fetch_professors_by_department(department_id):
    professors = [e.to_dict() for e in ProfessorModel.query(departmentId=department_id).limit(10000)]
    for professor in professors:
        if(professor['publicRating'] is False): # Hide rating summary if it's not public
            professor['ratingSummary'] = {}
    return professors

def fetch_professor(department_id, professor_id):
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')
    if(professor.publicRating is False): # Hide rating summary if it's not public
        professor.ratingSummary = {}
    return professor.to_dict()

def add_professor(professor):
    professor['id'] = str(uuid4())
    picture = professor.get('picture')
    del professor['picture']

    # Upload picture to S3
    if picture:
        picture_extension = picture.filename.split('.')[-1]
        s3_path = f'public/imgs/professors/prof-{professor["id"]}.{picture_extension}'
        s3_adapter.upload_file(s3_path, picture)
        professor['pictureUrl'] = f'https://{BUCKET_FILES}.s3.amazonaws.com/{s3_path}'
    
    if('ratingSummary' in professor):
        del professor['ratingSummary']

    professor = ProfessorModel(**professor)
    professor.save()

def update_professor(professor_id, data):
    data['id'] = professor_id
    department_id = data.get('departmentId')
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)
    
    # Update picture
    picture = data.get('picture')
    del data['picture']
    if picture:
        picture_extension = picture.filename.split('.')[-1]
        s3_path = f'public/imgs/professors/prof-{professor_id}.{picture_extension}'
        s3_adapter.upload_file(s3_path, picture)
        data['pictureUrl'] = f'https://{BUCKET_FILES}.s3.amazonaws.com/{s3_path}'

    if('ratingSummary' in data):
        del data['ratingSummary']

    professor.update(**data)
    professor.save()

def remove_professor(department_id, professor_id):
    professor = ProfessorModel.get(departmentId=department_id, id=professor_id)

    # Delete picture from S3
    if getattr(professor, 'pictureUrl', None):
        s3_path = professor.pictureUrl.split(f'{BUCKET_FILES}.s3.amazonaws.com/')[1]
        if(s3_adapter.file_exists(s3_path)):
            s3_adapter.delete_file(s3_path)

    professor.delete()