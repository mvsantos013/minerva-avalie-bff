from uuid import uuid4
from src.app.models import ProfessorModel, DisciplineProfessorModel
from src.lib.adapters import s3_adapter
from src.constants import BUCKET_FILES

def fetch_professors():
    professors = [e.to_dict() for e in ProfessorModel.query().limit(10000)]
    return professors

def fetch_professor(professor_id):
    professor = ProfessorModel.get(id=professor_id)
    return professor.to_dict()

def fetch_professor_disciplines(professor_id):
    professor = ProfessorModel.get(id=professor_id)
    if(professor is None):
        raise Exception('Professor not found')
    disciplines = [e.to_dict() for e in DisciplineProfessorModel.query(professorId=professor_id).limit(10000)]
    return disciplines

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

    professor = ProfessorModel(**professor)
    professor.save()

def update_professor(professor_id, data):
    data['id'] = professor_id
    professor = ProfessorModel.get(id=professor_id)
    
    # Update picture
    picture = data.get('picture')
    del data['picture']
    if picture:
        picture_extension = picture.filename.split('.')[-1]
        s3_path = f'public/imgs/professors/prof-{professor_id}.{picture_extension}'
        s3_adapter.upload_file(s3_path, picture)
        data['pictureUrl'] = f'https://{BUCKET_FILES}.s3.amazonaws.com/{s3_path}'

    professor.update(**data)
    professor.save()

def remove_professor(professor_id):
    professor = ProfessorModel.get(id=professor_id)

    # Delete picture from S3
    if getattr(professor, 'pictureUrl', None):
        s3_path = professor.pictureUrl.split(f'{BUCKET_FILES}.s3.amazonaws.com/')[1]
        if(s3_adapter.file_exists(s3_path)):
            s3_adapter.delete_file(s3_path)

    professor.delete()