import json
import time
import random
import atexit
from datetime import datetime
from .Logger import Logger
from .utils import *


def insert_update(container, key, value):
    container[key] = value if str(value) != "NaN" else "NaN"


class ExperimentLogger(object):

    def __init__(self, name):
        atexit.register(self.close_save)
        self.id = generate_MD5(f"{name}-{time.time()}-{random.random()}")
        self.begin_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.begin_timestamp = time.time()
        self.name = name
        self.save_dir = f"{DEFAULT_LOG_PATH}/{self.name}"
        self.parameters = dict()
        self.shown_parameter_names = []
        self.performance = None

    @staticmethod
    def clip_decimal(x):
        return int(x * 1000) / 1000

    def close_save(self):
        if self.performance is None:
            Logger.get_logger().error(
                "No results saved, experiment could be interrupted during the training..."
            )
            return
        os.makedirs(self.save_dir, exist_ok=True)

        experiment_log = dict()
        experiment_profile = dict()

        experiment_profile["name"] = self.name
        experiment_profile["id"] = self.id
        experiment_profile["commit_id"] = retrieve_commit_id()

        experiment_profile["begin_timestamp"] = self.clip_decimal(self.begin_timestamp)
        experiment_profile["end_timestamp"] = self.clip_decimal(time.time())
        experiment_profile["elapsed_in_s"] = self.clip_decimal(
            experiment_profile["end_timestamp"] - experiment_profile["begin_timestamp"]
        )

        experiment_log["parameters"] = self.parameters
        experiment_log["performance"] = self.performance

        experiment_profile["MD5"] = generate_MD5(
            self.parameters.__str__() + self.performance.__str__()
        )
        experiment_log["profile"] = experiment_profile
        experiment_log = convert_tolistible_object_to_list(experiment_log)
        os.makedirs(f"{self.save_dir}/{self.begin_time_string[:10]}", exist_ok=True)
        with open(
            f"{self.save_dir}/{self.begin_time_string[:10]}/{self.name}-{self.begin_time_string}-{self.id}.json",
            "w",
        ) as f:
            json.dump(experiment_log, f)

    def insert_shown_parameter_names(self, name):
        self.shown_parameter_names.append(retrieve_var_name(name))

    def insert_batch_shown_parameter_names(self, names: list):
        self.shown_parameter_names.extend(map(lambda x: retrieve_var_name(x), names))

    def set_parameter_by_args(self, parameter_set_in_args):
        parameters = {f"{key}": val for key, val in parameter_set_in_args._get_kwargs()}
        self.set_parameters(parameters)

    def set_parameters_by_dict(self, parameter_set_in_dict):
        for k, v in parameter_set_in_dict.items():
            self.insert_parameters(k, v)

    def set_parameters(self, parameters):
        self.parameters = parameters

    def insert_parameters(self, key, value):
        insert_update(self.parameters, key, value)

    def insert_batch_parameters(self, parameters_list):
        for param in parameters_list:
            param_name = retrieve_var_name(param)
            insert_update(self.parameters, param_name, param)

    def insert_performance(self, key, value):
        if self.performance is None:
            self.performance = dict()
        if key in self.performance.keys():
            print("Warning: key {} already exists.".format(key))
        insert_update(self.performance, key, value)

    def insert_batch_performance(self, result_list):
        for result in result_list:
            result_name = retrieve_var_name(result)
            self.insert_performance(result_name, result)


if __name__ == "__main__":
    ...
