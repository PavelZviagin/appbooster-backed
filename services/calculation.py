import random

from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from experiments.dao import (DevicesDAO, ExperimentDistributionDAO,
                             ExperimentsDAO)


class ExperimentsCalculation:

    def __init__(self, device_token):
        self.device_token = device_token

    def _calculate_experiment(self, experiment):
        distributions = ExperimentDistributionDAO.find_all(experiment_key=experiment.name)

        if not distributions:
            option = random.choice(experiment.options)
            self._insert_distribution(experiment.name, option)
            return option

        current_distribution_by_count = dict()

        total_devices = 0
        for distribution in distributions:
            current_distribution_by_count[distribution.experiment_value] = distribution.device_count
            total_devices += distribution.device_count

        excepted_distribution = experiment.values

        current_distribution = dict()

        for k, v in excepted_distribution.items():
            if k in current_distribution_by_count:
                current_procent = current_distribution_by_count[k] * 100 / total_devices
                current_distribution[k] = current_procent - v
            else:
                current_distribution[k] = -1

        min_deviation_value = min(current_distribution, key=current_distribution.get)
        if min_deviation_value in current_distribution_by_count:
            self._update_distribution(
                experiment.name,
                min_deviation_value,
                current_distribution_by_count.get(min_deviation_value, 1) + 1
            )
        else:
            self._insert_distribution(experiment.name, min_deviation_value)
        return min_deviation_value

    def _insert_experiments(self):
        DevicesDAO.add(
            device_token=self.device_token,
            button_color=self.button_color,
            price=self.price)

    @staticmethod
    def _insert_distribution(experiment_name, experiment_value, device_count=1):
        ExperimentDistributionDAO.add(
            experiment_key=experiment_name,
            experiment_value=experiment_value,
            device_count=device_count)

    @staticmethod
    def _update_distribution(experiment_name, experiment_value, device_count):
        ExperimentDistributionDAO.update_device_count(
            experiment_key=experiment_name,
            experiment_value=experiment_value,
            device_count=device_count)

    def calculate(self):
        try:
            experiments = ExperimentsDAO.find_all()

            for experiment in experiments:
                setattr(self, experiment.name, self._calculate_experiment(experiment))

            self._insert_experiments()
        except OperationalError:
            raise HTTPException(status_code=500, detail="Database connection error")
        except AttributeError:
            raise HTTPException(status_code=500, detail="Internal error")

