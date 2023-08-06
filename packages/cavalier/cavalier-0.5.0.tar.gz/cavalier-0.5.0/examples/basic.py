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

from cavalier.datastore.elasticsearch import ElasticSearch
from cavalier.metric import Metric


def main():
    metric = Metric(
        "customers.123.456.789.cpu",
        40.34,
        {"agentId": "1bee4e3c-0976-44d9-bf4a-6432857e4f3c"}
    )
    es = ElasticSearch("http://localhost:9200")
    es.migrate("metric")
    es.insert(metric, "metric")
    es.is_absent("metric", "customers.123.456.789.cpu")


if __name__ == '__main__':
    main()
