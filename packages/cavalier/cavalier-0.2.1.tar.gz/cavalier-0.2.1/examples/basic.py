
from cavalier.datastore.elastic_search import ElasticSearch
from cavalier.metric import Metric


def main():
    metric = Metric(
        "customers.123.456.789.cpu",
        40.34,
        {"agentId": "1bee4e3c-0976-44d9-bf4a-6432857e4f3c"}
    )
    es = ElasticSearch("http://localhost:9200")
    es.migrate()
    es.insert(metric)


if __name__ == '__main__':
    main()
