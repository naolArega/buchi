from fastapi import APIRouter
from core.http_utils import Response
from models.report_model import ReportModel
from fastapi.encoders import jsonable_encoder
from services.report_service import get_report
from core.buchi_exception import BuchiException

router = APIRouter(prefix="/report", tags=["Report"])

@router.post("/generate_report", description="This endpoint will create a small report using date range.")
async def generate_report(report: ReportModel):
    try:        
        data = await get_report(jsonable_encoder(report))
        return Response("success", "data", data)
    except BuchiException as e:
        return Response("error", "message", e.message)
    except:
        return Response("error", "message", "internal server error, please contact the admin.")