import requests
import logging
import json


class Meta:
    def __init__(
            self,
            gc2
    ):
        self.__gc2 = gc2
        self.__url = f"{gc2.url}/"
        self.table = None
        self.geojson = None
