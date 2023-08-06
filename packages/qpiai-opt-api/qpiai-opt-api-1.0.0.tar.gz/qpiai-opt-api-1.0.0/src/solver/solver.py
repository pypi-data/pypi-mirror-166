from pydantic import BaseModel
import pickle
import requests
from requests.models import Response


class Solver:
    """
    Solver class connects to QpiAI-Opt's cloud server, and run the solver on the passed problem.

    Initialize Solver class with problem and access token

    :type problem: BaseModel
    :param problem: Problem object to be passed from one of the classes in problem directory

    :type url: str
    :param url: Url to access api

    :type access_token: str
    :param access_token: access token to authenticate the solver
    """
    response: Response

    def __init__(self, problem: BaseModel, url: str, access_token: str):
        self.Problem = problem
        self.data = pickle.dumps(problem)
        self.url = url
        self.access_token = access_token

    def run(self):
        """
        Runs the problem on the QpiAI-Opt Solver on cloud
        """
        self.response = requests.post(url=f"{self.url}/{self.Problem.problem_type}",
                                      headers={"access_token": self.access_token}, data=self.data)

    def get_result(self):
        """
        to fetch the result after the solver has returned the result of the submitted problem

        :return Response: json
        """
        result = {'num_nodes': self.response.json()['num_nodes'],
                  'objective': self.response.json()['objective'],
                  'time': self.response.json()['time']}
        return result

    def get_solution(self):
        return self.response.json()['solution']

    def get_qubo_graph(self):
        return self.response.json()['graph']
