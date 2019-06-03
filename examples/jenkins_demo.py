"""
Simple script to set build status on uStatusBoard
builtin leds.

Based on the status, the led will light up green, red
or yellow in order to show each build status.

"""
import time
try:
    import urequests as requests
except ImportError:
    import requests

from status_board import StatusBoard


class Jenkins:
    """
    Class to handle all needed operations to get the
    build status and color assigned to it.

    Attributes:
        last_build: URL to fetch last build regardless its status.
        status_color: Match between color and statuses.
        user: Jenkins username.
        psswd: Password used to authenticate on Jenkins.
        project: Job on Jenkins to retrieve the status from.
        host: IP:port to communicate with Jenkins.

    """
    last_build = "http://{auth}{host}{job}/lastBuild/api/json"
    status_color = {
        "FAILURE": 'red',
        "SUCCESS": 'yellow',
        "UNSTABLE": 'green',
    }

    def __init__(self, host, user, password, job):
        self.user = user
        self.psswd = password
        self.auth = ''
        self.host = host
        self.project = job
        self.set_authorization(user, password)
        self._set_url()

    def set_authorization(self, user, password):
        """
        Set the value for the authorization part of the url.

        Args:
            user (str): Username.
            password (str): Password.

        Returns:
            None.
        """
        if user is not None and password is not None:
            self.auth = "{user}:{password}@".format(
                user=user, password=password
            )
        else:
            self.auth = ''

    def _set_url(self):
        """
        Add values on the URL in order to retrieve data.

        Returns:
            None.
        """
        self.url = self.last_build.format(auth=self.auth, host=self.host, job=self.project)

    def get_status_color(self, status):
        """
        Based on a status return its color assigned.

        Args:
            status (str): status to look the color for.

        Returns:
            String with the color assigned to the status.
        """
        return self.status_color[status]

    def get_build_status(self):
        """
        Make an HTTP request to jenkins API and retrieve the build
        information to look for the build status on it.

        Returns:
            String with the `result` attribute on response.
        """
        querystring = {"depth": "1"}

        payload = ""
        headers = {
            'Connection': "keep-alive",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            }
        response = requests.get(self.url, data=payload, headers=headers, params=querystring)
        data = response.json()['result']
        response.close()
        return data


board = StatusBoard()
USER = 'username'
PASS = 'password'
ENDPOINT = '"jenkins.com:9090/"'

jenkins_project1 = Jenkins(
    host=ENDPOINT, user=USER, password=PASS, job="job/project1"
)
jenkins_project2 = Jenkins(
    host=ENDPOINT, user=USER, password=PASS, job="job/project2"
)

while True:
    project1_status = jenkins_project1.get_build_status()
    project2_status = jenkins_project2.get_build_status()
    build1_color = jenkins_project1.get_status_color(project1_status)
    build2_color = jenkins_project2.get_status_color(project2_status)
    board.set_pixel_color(0, build1_color)
    board.set_pixel_color(1, build2_color)
    time.sleep(10)
