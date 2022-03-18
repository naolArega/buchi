from core import mongodb
from datetime import timedelta, date
from core.buchi_exception import BuchiException

adoptions_collection = mongodb.buchi.get_collection('adoptions')
pets_collection = mongodb.buchi.get_collection('pets')

async def get_report(report: dict):
    generated_report = {
        "adopted_pet_types": await get_adopted_pet_types(report["from_date"], report["to_date"]),
        "weekly_adoption_requests": await get_weekly_adoption_request(report["from_date"], report["to_date"])
    }
    return generated_report

async def get_weekly_adoption_request(from_date: str, to_date: str):
    try:        
        start_date = date.fromisoformat(from_date)
        to_date = date.fromisoformat(to_date)
        end_date = to_date
        weekly_adoption_request_reports = {}
        while start_date < to_date:
            days_until_last_date = (to_date - start_date).days
            if days_until_last_date < 7:
                end_date = start_date + timedelta(days=days_until_last_date)
            else:
                end_date = start_date + timedelta(days=7)
            adoption_request_count = await adoptions_collection.count_documents({
                "request_date": {'$gte': start_date.isoformat(), '$lte': end_date.isoformat()}
            })
            if adoption_request_count > 0:
                weekly_adoption_request_reports.update({end_date.isoformat(): adoption_request_count})
            start_date = end_date
        return weekly_adoption_request_reports
    except:
        raise BuchiException("unable to generate weekly adoption requests")

async def get_adopted_pet_types(from_date: str, to_date: str):
    try:        
        pet_report = {}
        distinct_pets_types = await pets_collection.distinct("type")
        for type in distinct_pets_types:
            pet_count = await get_distinct_adopted_pets(type, from_date, to_date)
            if pet_count > 0:
                pet_report.update({type: pet_count})
        return pet_report
    except:
        raise BuchiException("unable to generate pet report")

async def get_distinct_adopted_pets(type: str, from_date: str, to_date: str):
    try:
        adopted_pets_count = await adoptions_collection.count_documents({
                "type": type,
                "request_date": {'$gte': from_date, '$lte': to_date}
            })
        return adopted_pets_count
    except:
        raise BuchiException("unable to fetch adopted pets count")