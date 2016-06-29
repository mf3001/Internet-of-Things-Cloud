from elasticsearch import Elasticsearch

def create_response(color):
    #color is lower-case string
    try:
        get_size = es.search(index = color)['hits']['total']
        result_raw = es.search(index = color, filter_path = ['hits.hits._*'], size = get_size)
        result_list = result_raw["hits"]["hits"]
    except:
        result_list = []
    response_list = []
    for i in result_list:
        response_list.append(i['_source'])
    return {"trashList": response_list}