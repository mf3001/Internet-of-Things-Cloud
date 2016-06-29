from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers

from elasticsearch import Elasticsearch
# Create your views here.



def index(request):
    q_dict =  request.GET
    if q_dict:
        es = Elasticsearch()
        response_list = []
        if 'color' in q_dict:
            color_to_parse = q_dict['color']
            colors = color_to_parse.split('_')
            
            for c in colors:
                try:
                    get_size = es.search(index = c)['hits']['total']
                    result_raw = es.search(index = c, filter_path = ['hits.hits._*'], size = get_size)
                    #print "result_raw"
                    #print result_raw
                    result_list = result_raw["hits"]["hits"]
                except:
                    result_list = []
                for i in result_list:
                    response_list.append(i['_source'])

            response = {"trashList": response_list}
            print JsonResponse(response)
            return JsonResponse(response)
        elif 'route' in q_dict:
            index = q_dict['route'] + 'routing'
            print index
            try:
                result_raw = es.search(index = index, filter_path = ['hits.hits._*'], size = 1)
                result = result_raw['hits']['hits'][0]['_source']
            except:
                result = {}
            #print JsonResponse(response)
            return JsonResponse(result)
        elif 'routelist' in q_dict:
            index = q_dict['routelist'] + 'routinglist'
            print index
            try:
                result_raw = es.search(index = index, filter_path = ['hits.hits._*'], size = 1)
                result = result_raw['hits']['hits'][0]['_source']
            except:
                result = {}
            #print JsonResponse(response)
            return JsonResponse(result)
    else:
        #return HttpResponse("Hello, world. You're at the polls index.")
        template = loader.get_template('part1/index.html')
        #print "view.index requested"
        return HttpResponse(template.render(request))