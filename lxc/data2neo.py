from py2neo import Graph
from py2neo import Node,Relationship
import pandas as pd

graph = Graph('bolt://localhost:7687',auth=('neo4j','12345678'))
graph.delete_all()

nodes = {}

node_namespace = pd.read_csv('./data/numpy_namespace_nodes.csv')
for i in range(len(node_namespace)):
    node = Node('namespace',name=node_namespace.loc[i,'name'])
    graph.create(node)
    nodes[node_namespace.loc[i,'name']] = node

path_namespace = pd.read_csv('./data/numpy_namespace_relation.csv')
for i in range(len(path_namespace)):
    relation = Relationship(nodes[path_namespace.loc[i,'subject']],path_namespace.loc[i,'relation'],nodes[path_namespace.loc[i,'object']])
    graph.create(relation)
# namespace节点和关系

node_method = pd.read_csv('./data/numpy_method.csv')
for i in range(len(node_method)):
    node = Node('method',name=node_method.loc[i,'method'],parameters = node_method.loc[i,'parameters'],)
    graph.create(node)
    nodes[node_method.loc[i,'method']] = node

path_method = pd.read_csv('./data/numpy_method.csv')
for i in range(len(path_method)):
    relation = Relationship(nodes[path_method.loc[i,'namespace']],path_method.loc[i,'relation1'],nodes[path_method.loc[i,'method']])
    graph.create(relation)
# method节点和关系

node_property = pd.read_csv('./data/numpy_property.csv')
for i in range(len(node_property)):
    node = Node('property',name=node_property.loc[i,'property'])
    graph.create(node)
    nodes[node_property.loc[i,'property']] = node

path_property = pd.read_csv('./data/numpy_property.csv')
for i in range(len(path_property)):
    relation = Relationship(nodes[path_property.loc[i,'namespace']],path_property.loc[i,'relation1'],nodes[path_property.loc[i,'property']])
    graph.create(relation)
# property节点和关系

node_return_class = pd.read_csv('./data/numpy_return_nodes.csv')
for i in range(len(node_return_class)):
    node = Node('class',name=node_return_class.loc[i,'name'])
    graph.create(node)
    nodes[node_return_class.loc[i,'name']] = node

path_return_method = pd.read_csv('./data/numpy_method.csv')
for i in range(len(path_return_method)):
    relation = Relationship(nodes[path_return_method.loc[i,'method']],path_return_method.loc[i,'relation2'],nodes[path_return_method.loc[i,'return_class']])
    graph.create(relation)

path_return_property = pd.read_csv('./data/numpy_property.csv')
for i in range(len(path_return_property)):
    relation = Relationship(nodes[path_return_property.loc[i,'property']],path_return_property.loc[i,'relation2'],nodes[path_return_property.loc[i,'return_class']])
    graph.create(relation)
# 添加class

# =====更新Python数据=====

node_python_method = pd.read_csv('./data/python_method.csv')
for i in range(len(node_python_method)):
    node = Node('method',name=node_python_method.loc[i,'method'],parameters = node_python_method.loc[i,'parameters'],)
    graph.create(node)
    nodes[node_python_method.loc[i,'method']] = node

path_python_method = pd.read_csv('./data/python_method.csv')
for i in range(len(path_python_method)):
    relation = Relationship(nodes[path_python_method.loc[i,'class']],path_python_method.loc[i,'relation1'],nodes[path_python_method.loc[i,'method']])
    graph.create(relation)

path_return_python = pd.read_csv('./data/python_method.csv')
for i in range(len(path_return_python)):
    relation = Relationship(nodes[path_return_python.loc[i,'method']],path_return_python.loc[i,'relation2'],nodes[path_return_python.loc[i,'return_class']])
    graph.create(relation)
# 添加Python相关数据

path_numpy_hasclass_relation = pd.read_csv('./data/numpy_hasclass_relation.csv')
for i in range(len(path_numpy_hasclass_relation)):
    relation = Relationship(nodes[path_numpy_hasclass_relation.loc[i,'namespace']],path_numpy_hasclass_relation.loc[i,'relation'],nodes[path_numpy_hasclass_relation.loc[i,'class']])
    graph.create(relation)

# =====更新pandas数据=====


node_namespace = pd.read_csv('./data/pandas_namespace_nodes.csv')
for i in range(len(node_namespace)):
    node = Node('namespace',name=node_namespace.loc[i,'name'])
    graph.create(node)
    nodes[node_namespace.loc[i,'name']] = node

path_namespace = pd.read_csv('./data/pandas_namespace_relation.csv')
for i in range(len(path_namespace)):
    relation = Relationship(nodes[path_namespace.loc[i,'subject']],path_namespace.loc[i,'relation'],nodes[path_namespace.loc[i,'object']])
    graph.create(relation)

node_method = pd.read_csv('./data/pandas_method.csv')
for i in range(len(node_method)):
    node = Node('method',name=node_method.loc[i,'method'],parameters = node_method.loc[i,'parameters'],)
    graph.create(node)
    nodes[node_method.loc[i,'method']] = node

path_method = pd.read_csv('./data/pandas_method.csv')
for i in range(len(path_method)):
    relation = Relationship(nodes[path_method.loc[i,'namespace']],path_method.loc[i,'relation1'],nodes[path_method.loc[i,'method']])
    graph.create(relation)
# method节点和关系

node_property = pd.read_csv('./data/pandas_property.csv')
for i in range(len(node_property)):
    node = Node('property',name=node_property.loc[i,'property'])
    graph.create(node)
    nodes[node_property.loc[i,'property']] = node

path_property = pd.read_csv('./data/pandas_property.csv')
for i in range(len(path_property)):
    relation = Relationship(nodes[path_property.loc[i,'namespace']],path_property.loc[i,'relation1'],nodes[path_property.loc[i,'property']])
    graph.create(relation)
# property节点和关系

node_return_class = pd.read_csv('./data/pandas_return_nodes.csv')
for i in range(len(node_return_class)):
    node = Node('class',name=node_return_class.loc[i,'name'])
    graph.create(node)
    nodes[node_return_class.loc[i,'name']] = node

path_return_method = pd.read_csv('./data/pandas_method.csv')
for i in range(len(path_return_method)):
    relation = Relationship(nodes[path_return_method.loc[i,'method']],path_return_method.loc[i,'relation2'],nodes[path_return_method.loc[i,'return_class']])
    graph.create(relation)

path_return_property = pd.read_csv('./data/pandas_property.csv')
for i in range(len(path_return_property)):
    relation = Relationship(nodes[path_return_property.loc[i,'property']],path_return_property.loc[i,'relation2'],nodes[path_return_property.loc[i,'return_class']])
    graph.create(relation)
# 添加class

path_pandas_hasclass_relation = pd.read_csv('./data/pandas_hasclass_relation.csv')
for i in range(len(path_pandas_hasclass_relation)):
    relation = Relationship(nodes[path_pandas_hasclass_relation.loc[i,'namespace']],path_pandas_hasclass_relation.loc[i,'relation'],nodes[path_pandas_hasclass_relation.loc[i,'class']])
    graph.create(relation)

graph.run('MATCH (n:namespace {name: "numpy"})SET n:root')
graph.run('MATCH (n:namespace {name: "pandas"})SET n:root')
graph.run('MATCH (n:class {name: "Str"})SET n:root')
graph.run('MATCH (n:class {name: "Dict"})SET n:root')
graph.run('MATCH (n:class {name: "List"})SET n:root')
graph.run('MATCH (n:class {name: "Set"})SET n:root')

graph.run("MATCH (n) SET n.type=labels(n)[0] RETURN n.name ,labels(n)[0]")
graph.run("MATCH (n:namespace{name:'numpy'})-[:has_method]->(m),(p:class{name:'ndarray'}) CREATE (p)-[:has_method]->(m)")

graph.run("match (n) where n.parameters is null set n.parameters=''")