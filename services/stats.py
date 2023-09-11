from experiments.dao import ExperimentDistributionDAO, ExperimentsDAO


class Statistic:

    @classmethod
    def get_statistic(cls):
        experiments = ExperimentsDAO.find_all()
        return cls._get_stats(experiments)

    @classmethod
    def _get_stats_by_name(cls, name):
        distibutions = ExperimentDistributionDAO.find_all(experiment_key=name)
        result_dict = {
            name: []
        }

        for distribution in distibutions:
            result_dict[name].append({
                "name": distribution.experiment_value,
                "count": distribution.device_count
            })

        return result_dict

    @classmethod
    def _get_stats(cls, experiments):
        return [cls._get_stats_by_name(experiment.name) for experiment in experiments]
