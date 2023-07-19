from py2neo import Graph
from py2neo import Node,Relationship
import pandas as pd

# 测试代码
# import numpy

# # 查看numpy包的所有属性和方法
# print(dir(numpy))

# # 查看numpy中特定类的所有属性和方法
# print(dir(numpy.ndarray))

def create_node(graph,label,properties):
    node = Node(label,**properties)
    graph.create(node)
    return node

def create_relationship(graph,start_node,relation_type,end_node):
    relationship = Relationship(start_node, relation_type, end_node)
    graph.create(relationship)

graph = Graph('bolt://localhost:7687',auth=('neo4j','12345678'))
graph.delete_all()

# 读取包含命名空间信息的csv文件
node_namespaces = pd.read_csv('./data/data/package_namespace.csv')

nodes = {}

# 把命名空间的信息存储到nodes节点中
for i in range(len(node_namespaces)):
    properties = {
        'name': node_namespaces.loc[i, 'name'],
        'type': node_namespaces.loc[i, 'type'],
        'variables': node_namespaces.loc[i, 'variables'],
        'functions': node_namespaces.loc[i, 'functions'],
        'classes': node_namespaces.loc[i, 'classes'],
        'modules': node_namespaces.loc[i, 'modules']
    }
    node = create_node(graph, '命名空间', properties)
    nodes[node_namespaces.loc[i, 'name']] = node

# 读取包含类信息的csv文件
node_classes = pd.read_csv('./data/data/package_class.csv')

# 把类的信息存储到nodes节点中
for i in range(len(node_classes)):
    properties = {
        'name': node_classes.loc[i, 'name'],
        'type': node_classes.loc[i, 'type'],
        'parent_classes': node_classes.loc[i, 'parent_classes'],
        'attributes': node_classes.loc[i, 'attributes'],
        'methods': node_classes.loc[i, 'methods'],
        'Docstrings': node_classes.loc[i, 'Docstrings']
    }
    node = create_node(graph, '类', properties)
    nodes[node_classes.loc[i, 'name']] = node

# 读取包含方法信息的csv文件
node_methods = pd.read_csv('./data/data/package_method.csv')

# 把类的信息存储到nodes节点中
for i in range(len(node_methods)):
    properties = {
        'name': node_methods.loc[i, 'name'],
        'type': node_methods.loc[i, 'type'],
        'Parameters': node_methods.loc[i, 'Parameters'],
        'return_value': node_methods.loc[i, 'return_value'],
        'Docstrings': node_methods.loc[i, 'Docstrings']
    }
    node = create_node(graph, '方法', properties)
    nodes[node_methods.loc[i, 'name']] = node

# 读取包含属性信息的csv文件
node_attributes = pd.read_csv('./data/data/package_attribute.csv')

# 把属性的信息存储到nodes节点中
for i in range(len(node_attributes)):
    properties = {
        'name': node_attributes.loc[i, 'name'],
        'type': node_attributes.loc[i, 'type'],
        'default_value': node_attributes.loc[i, 'default_value'],
        'visibility': node_attributes.loc[i, 'visibility'],
        'docstrings': node_attributes.loc[i, 'docstrings']
    }
    node = create_node(graph, '属性', properties)
    nodes[node_attributes.loc[i, 'name']] = node

# 读取包含所有关系的文件
path_information = pd.read_csv('./data/data/all_information_relations.csv')

# 把所有的关系存到数据库中
for i in range(len(path_information)):
    start_node = nodes[path_information.loc[i, 'subject']]
    end_node = nodes[path_information.loc[i, 'object']]
    create_relationship(graph, start_node, path_information.loc[i, 'relation'], end_node)

print('End...')


# 测试代码
# import numpy

# # 查看numpy包的文档字符串
# print(help(numpy))

# # 查看numpy中特定类的文档字符串
# print(help(numpy.ndarray))
