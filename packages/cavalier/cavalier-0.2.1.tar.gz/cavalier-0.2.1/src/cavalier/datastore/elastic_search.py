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
        client: An instance of elasticsearch client
    """

    def __init__(self, connection):
        """Inits elasticsearch"""
        self.logger = Logger().get_logger(__name__)
        self.client = Elasticsearch(connection)
        self.before_hook = None
        self.after_hook = None

    def get_client(self):
        """
        Get elasticsearch client

        Returns:
            a dict of client info
        """
        return self.client.info()

    def add_before_hook(self, callback):
        """Add before hook

        Args:
            callback: the before callback function
        """
        self.before_hook = callback

    def add_after_hook(self, callback):
        """Add after hook

        Args:
            callback: the after callback function
        """
        self.after_hook = callback

    def insert(self, metric, indexName="metric"):
        """Insert metrics into elastic search

        Args:
            indexName: the elasticsearch index
            metric: the metric data to insert
        """
        self.logger.debug("Trigger before hook for metric: {}", str(metric))

        if self.before_hook is not None:
            self.before_hook(metric)

        doc = {
           "id": metric.id,
           "name": metric.name,
           "value": metric.value,
           "timestamp": metric.timestamp,
           "meta": metric.meta
        }

        self.logger.debug("Insert metric into elasticsearch: {}", str(metric))

        response = self.client.index(index=indexName, document=doc)

        self.logger.debug("Trigger after hook for metric: {}", str(metric))

        if self.after_hook is not None:
            self.after_hook(metric)

        return response


    def migrate(self, indexName="metric", shards=1, replicas=1):
        """Create metric index

        Args:
            indexName: the elasticsearch index
            shards: the number of shards
            replicas: the number of replicas
        """
        doc = {
            "settings": {
               "number_of_shards": shards,
               "number_of_replicas": replicas
            },
           "mappings": {
                "properties": {
                   "id": {"type": "text"},
                   "name": {"type": "text"},
                   "value": {"type": "float"},
                   "timestamp": {"type": "long"},
                   "meta": {"type": "object"}
                }
            }
        }

        response = self.client.index(index=indexName, document=doc)

        return response