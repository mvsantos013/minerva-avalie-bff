from datetime import datetime 
from src.app.models import (DisciplineRatingModel, 
        ProfessorRatingModel, DisciplineRatingSummaryModel, ProfessorRatingSummaryModel)

def handler(event, context):
    ''' Every time that there's a evaluation, this function will be called.
        It will compute the average evaluation for the professor and discipline.
    '''
    professor_id = event['professorId']
    discipline_id = event['disciplineId']
    discipline_department_id = event['disciplineDepartmentId']
    periods = get_periods()

    # Aggregate professor ratings of each student of each period for the discipline
    professor_rating_summary = compute_professor_rating_summary(professor_id, discipline_id, discipline_department_id, periods)
    ProfessorRatingSummaryModel(**professor_rating_summary).save()

    # Aggregate discipline ratings of each student of each period for the professor
    discipline_rating_summary = compute_discipline_rating_summary(professor_id, discipline_id, discipline_department_id, periods)
    DisciplineRatingSummaryModel(**discipline_rating_summary).save()

    return True

def get_periods(start_year=2023):
    today = datetime.today()
    periods = []
    for year in range(start_year, today.year + 1):
        for semester in range(1, 3 if today.month <= 6 else 4):
            if year == today.year and semester > (today.month + 5) // 6:
                break
            periods.append(f"{year}.{semester}")
    return periods

def compute_professor_rating_summary(professor_id, discipline_id, discipline_department_id, periods):
    all_professor_ratings = []
    for period in periods:
        ratings = ProfessorRatingModel.query(disciplineIdProfessorIdPeriod=f'{discipline_id}:{professor_id}:{period}').limit(1000)
        all_professor_ratings.extend(ratings)
    questions_summary = {}
    for rating_item in all_professor_ratings:
        questions = rating_item.ratings['questions']
        for question in questions:
            id = question['id']
            if id not in questions_summary:
                questions_summary[id] = {
                    'questionId': id,
                    'averageValue': 0,
                    'count': 0
                }
            questions_summary[id]['averageValue'] += question['value']
            questions_summary[id]['count'] += 1
    summary = []
    total_average = 0
    total_count = 0
    for item in questions_summary.values():
        total_average += item['averageValue']
        total_count += item['count']
        item['averageValue'] /= item['count']
        item['averageValue'] = round(item['averageValue'], 2)
        summary.append(item)
    total_average /= total_count
    total_average = round(total_average, 2)
    professor_rating_summary = {
        'professorId': professor_id,
        'disciplineId': discipline_id,
        'disciplineDepartmentId': discipline_department_id,
        'details': summary,
        'averageValue': total_average,
        'count': total_count,
        'createdAt': datetime.now().isoformat(),
    }
    return professor_rating_summary

def compute_discipline_rating_summary(professor_id, discipline_id, discipline_department_id, periods):
    all_discipline_ratings = []
    for period in periods:
        ratings = DisciplineRatingModel.query(disciplineIdProfessorIdPeriod=f'{discipline_id}:{professor_id}:{period}').limit(1000)
        all_discipline_ratings.extend(ratings)
    questions_summary = {}
    for rating_item in all_discipline_ratings:
        questions = rating_item.ratings['questions']
        for question in questions:
            id = question['id']
            if id not in questions_summary:
                questions_summary[id] = {
                    'questionId': id,
                    'averageValue': 0,
                    'count': 0
                }
            questions_summary[id]['averageValue'] += question['value']
            questions_summary[id]['count'] += 1
    summary = []
    total_average = 0
    total_count = 0
    for item in questions_summary.values():
        total_average += item['averageValue']
        total_count += item['count']
        item['averageValue'] /= item['count']
        item['averageValue'] = round(item['averageValue'], 2)
        summary.append(item)
    total_average /= total_count
    total_average = round(total_average, 2)
    discipline_rating_summary = {
        'professorId': professor_id,
        'disciplineId': discipline_id,
        'disciplineDepartmentId': discipline_department_id,
        'details': summary,
        'averageValue': total_average,
        'count': total_count,
        'createdAt': datetime.now().isoformat(),
    }
    return discipline_rating_summary