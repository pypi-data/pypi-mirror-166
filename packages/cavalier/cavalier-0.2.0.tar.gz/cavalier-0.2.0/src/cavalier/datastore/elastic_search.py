# Copyright 2020 Clivern
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cavalier.logger import Logger
from elasticsearch import Elasticsearch


class ElasticSearch():
    """ElasticSearch Class

    Attributes:
        logger: An instance of Logger class
    """

    def __init__(self, connection):
        """Inits elasticsearch"""
        self.logger = Logger().get_logger(__name__)
        self.client = Elasticsearch(connection)

    def get_client(self):
        """
        Get elasticsearch client

        Returns:
            a dict of client info
        """
        return self.client.client.info()

    def add_before_hook(self, callback):
        """Add before hook

        Args:
            callback: the before callback function
        """
        self._before_hook = callback

    def add_after_hook(self, callback):
        """Add after hook

        Args:
            callback: the after callback function
        """
        self._after_hook = callback

    def insert(self, data):
        """Insert metrics into elastic search

        Args:
            data: the metric data to insert
        """
        self._before_hook(data)
        self._after_hook(data)

    def query(self, filters):
        """Query the elastic search

        Args:
            filters: the filters to use
        """
        pass
