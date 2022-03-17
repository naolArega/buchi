from services.pet_service import get_adopted_pet_types
from services.adoption_service import get_weekly_adoption_request

async def get_report(report: dict):
    generated_report = {
        "adopted_pet_types": await get_adopted_pet_types(),
        "weekly_adoption_requests": await get_weekly_adoption_request(report["from_date"], report["to_date"])
    }
    return generated_report