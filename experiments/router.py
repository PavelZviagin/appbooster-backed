from fastapi import APIRouter, Depends

from experiments.dao import DevicesDAO
from experiments.dependency import get_device_token
from experiments.schemas import ExperimentsSchema
from services.calculation import ExperimentsCalculation
from services.stats import Statistic

api_router = APIRouter(prefix="/api")


@api_router.get("/experiments")
async def get_experiments(device_token=Depends(get_device_token)) -> ExperimentsSchema:
    experiments = DevicesDAO.find_one_or_none(device_token=device_token)

    if experiments:
        return experiments

    calculation = ExperimentsCalculation(device_token)
    calculation.calculate()

    return ExperimentsSchema.model_validate({"button_color": calculation.button_color, "price": calculation.price})


@api_router.get("/stats")
async def get_stats():
    return Statistic.get_statistic()
