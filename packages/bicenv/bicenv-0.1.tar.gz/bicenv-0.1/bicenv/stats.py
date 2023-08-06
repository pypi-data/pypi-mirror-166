import os
import datetime
import pandas as pd
import numpy as np
from .agv import AGV
from .request import Request


class Statistics:
    """Statistics Class

    Parameters
    ----------
    results_root : [String]
        relative path for results location
    exp_name : [String]
        [Name of experiment. Current date and time is automatically appended to name to avoid overwriting]

    """

    def __init__(self, results_root, exp_name):
        """Statistics Class

        Parameters
        ----------
        results_root : [String]
            relative path for results location
        exp_name : [String]
            [Name of experiment. Current date and time is automatically appended to name to avoid overwriting]
        """

        self.req_results = []
        self.rejected_req_results = []
        self.agv_results = []
        self.agg_results = {}
        self.results_root = results_root
        self.exp_name = exp_name

    def save_results(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%Hh-%Mm-%Ss")
        self.exp_name_t = f"{self.exp_name}-{now}"
        main_path = os.path.join(self.results_root, self.exp_name_t)
        tables_path = os.path.join(main_path, "tables")
        plots_path = os.path.join(main_path, "plots")

        if not os.path.exists(main_path):
            os.makedirs(main_path)
            os.mkdir(os.path.join(main_path, "tables"))
            os.mkdir(os.path.join(main_path, "plots"))

        request_df = pd.DataFrame(self.req_results)
        rejected_request_df = pd.DataFrame(self.rejected_req_results)

        request_df.to_csv(
            os.path.join(tables_path, "requests_results.csv"), index=False
        )

        rejected_request_df.to_csv(
            os.path.join(tables_path, "rejected_requests_results.csv"), index=False
        )

        agv_df = pd.DataFrame(self.agv_results)
        agv_df.to_csv(os.path.join(tables_path, "agv_results.csv"), index=False)


    def record_rejected_request_stats(self, request:Request):
        """
        Records request specific stats

        Parameters
        ----------
        request : Request
            Object of Request class
        """
        self.rejected_req_results.append(vars(request))



    def record_request_stats(self, request:Request):
        """
        Records request specific stats

        Parameters
        ----------
        request : Request
            Object of Request class
        """
        self.req_results.append(vars(request))

        # self.req_results["est_pickup_time"].append(round(request.est_pickup_time, 2))
        

    def record_agv_stats(self, agv:AGV):

        """
        Record AGV specific stats
        """
        self.agv_results.append(vars(agv))


    def get_agg_stats(self):
        """
        Return a dictionary with aggregated episode stats
        """

        agv_df = pd.DataFrame(self.agv_results)
        req_df = pd.DataFrame(self.req_results)
        num_rejected_reqs = len(self.rejected_req_results)

        self.agg_results["num_rejected_reqs"] = num_rejected_reqs

        req_df['tardiness'] = np.maximum(0, req_df['delivery_time'] - req_df['ldt'])
        agv_df['total_travel_time'] = agv_df['loaded_travel_time'] + agv_df['unloaded_travel_time']

        agv_stat_run_dict = agv_df.groupby('type').agg({'loaded_travel_time':'mean', 'unloaded_travel_time':'mean', 'total_travel_time':'mean'}).to_dict()
        req_stat_run_dict = req_df.groupby('request_cost').agg({'tardiness':'mean'}).to_dict()
        
        stat_dict = {}
        for k in agv_stat_run_dict.keys():
            for l in agv_stat_run_dict[k].keys():
                stat_dict[f'mean_{k}_AGV_type_{l}'] = agv_stat_run_dict[k][l]
                # print(k,l)

        for k in req_stat_run_dict.keys():
            for l in req_stat_run_dict[k].keys():
                stat_dict[f'mean_{k}_request_cost_{l}'] = req_stat_run_dict[k][l]

        self.agg_results.update(stat_dict)

        # Costs

        tardiness_cost, fleet_travel_cost = self.get_objective__value(agv_df, req_df)

        self.agg_results["tardiness_cost"] = tardiness_cost
        self.agg_results["fleet_travel_cost"] = fleet_travel_cost
        
        for key, val in self.agg_results.items():
            self.agg_results[key] = round(val, 2)
            if type(val) == np.int64:
                print(key, val)
                raise RuntimeError("This is an int")

        return self.agg_results


    def get_objective__value(self, agv_df, req_df):
        """
        Return the objective value of the current episode
        """
        tardiness_cost = (req_df['tardiness'] * req_df['request_cost']).sum()
        fleet_travel_cost = (agv_df['total_travel_time'] * agv_df['travel_cost']).sum()

        return tardiness_cost, fleet_travel_cost
        