from django.shortcuts import render
from python_hint.settings import graph
from django.http import HttpResponse
import json


# Create your views here.

def codes(request):
    return render(request,'python_code/index.html')

def find_next_id(m,n,id):
    if id == -1:
        query_idtype = f"MATCH (m{{name:'{m}'}})-[]->(n{{name:'{n}'}}) return ID(n),n.type"
        result_idtype = graph.run(query_idtype).data()[0]
    else:
        query_idtype = f"MATCH (m)-[]->(n) WHERE ID(m) = {id} return ID(n),n.type"
        result_idtype = graph.run(query_idtype).data()[0]
    if result_idtype['n.type'] == "method" or result_idtype['n.type'] == 'property':
            result_id = graph.run(f"MATCH (m)-[]->(n) WHERE ID(m) = {result_idtype['ID(n)']} return ID(n)").data()[0]['ID(n)']
    else:
        result_id = result_idtype['ID(n)']
    return result_id

# 根据id查询所属的类
def find_full_type(id):
    labels = []
    path = []
    query_id = id
    res = graph.run(f"match (m) where id(m) = {id} return m.name,labels(m)").data()[0]
    name = res['m.name']
    labels = res['labels(m)']
    path.append(name)
    while 'root' not in labels:
        res = graph.run(f"match (m:namespace)-[]->(n) where id(n) = {query_id} return id(m),m.name,labels(m)").data()
        if len(res):
            res = res[0]
            labels = res['labels(m)']
            query_id = res['id(m)']
            path.append(res['m.name'])
        else:
            res = graph.run(f"match (m:class)-[]->(n) where id(n) = {query_id} return id(m),m.name,labels(m)").data()
            if len(res):
                res = res[0]
                labels = res['labels(m)']
                query_id = res['id(m)']
                path.append(res['m.name'] + '()')
            else:
                return ''
    return ".".join(path[::-1])

# 获得节点指向的节点
def get_list(id):
    nodes = graph.run(f"match (n)-[]->(m) where id(n) = {id} return m.name as name,m.parameters as des,m.type as category,id(m) as id").data()
    return nodes

# 解析字符串，获得最后一个类型的id
def get_last_id(line):
    line = line.replace('()','')
    split_lists = line.split('.')
    next_id = -1
    for m,n in zip(split_lists[:],split_lists[1:]):
        next_id = find_next_id(m,n,next_id)
    
    if next_id == -1:
        query_idType = f"MATCH (m) WHERE m.name = '{split_lists[0]}' RETURN ID(m)"
        results = graph.run(query_idType).data()[0]
        next_id = results['ID(m)']
    return next_id

# 响应获得类型和提示的请求
def getType(request):
    line = request.GET.get('line')
    needList = request.GET.get('needList')
    next_id = get_last_id(line)
    line = find_full_type(next_id)
    if not needList:
        return HttpResponse(json.dumps({'type':line}))
    else:
        nodes = get_list(next_id)
        return HttpResponse(json.dumps({'type':line,'nodes':nodes}))

# 给定id，查询所有指向的节点，返回包括该节点在内的所有结点
def get_all_nodes(request):
    curr_id = request.GET.get('id')
    nodes = get_list(curr_id)
    last_node = graph.run(f"match (m) where id(m) = {curr_id} return m.name as name,m.parameters as des,m.type as category,ID(m) as id").data()[0]
    lines = []
    node_num = len(nodes)
    for index,node in enumerate(nodes):
        cat = node['category']
        relation_name = 'return_class' if last_node['category'] == 'method' or last_node['category'] == 'property' else 'has_' + cat
        temp = {
            'source':node_num,
            'target':index,
            'name': relation_name,
        }
        lines.append(temp)
    nodes.append(last_node)
    return HttpResponse(json.dumps({'nodes':nodes,'lines':lines}))

def query(request):
    nodes = graph.run(f"match (m:root) return m.name as name,m.parameters as des,m.type as category,ID(m) as id").data()
    return render(request,'python_code/query.html',{'nodes':nodes,'lines':[],'bread_list':[]})