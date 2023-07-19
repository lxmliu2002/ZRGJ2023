from py2neo import Graph

former_node_id = []

def is_contain_parentheses(string):
    if '(' in string:
        return True
    else:
        return False

def find_relationships_first(split_list): # 如果是列表中第一个
    # 连接到Neo4j数据库
    graph = Graph("bolt://localhost:7687", auth=('neo4j', '12345678'))

    query_idtype = f"MATCH (n) WHERE n.name = '{split_list}' RETURN n.id, n.type"
    result_idtype = graph.run(query_idtype)
    for record in result_idtype:
        node_id = record["n.id"]
        node_type = record["n.type"]
        if node_type == 'method' or node_type == 'attribute':
            query_next = f"MATCH (n)-[r:]->(o)-[r:]->(m) WHERE n.id = '{node_id}'  RETURN m.name"
        else:
            query_next = f"MATCH (n)-[r:]->(m) WHERE n.id = '{node_id}'  RETURN m.name"
        result_next = graph.run(query_next)
        next_node = [record["m.name"] for record in result_next]
        global former_node_id
        former_node_id = record["n.id"]
    return next_node


def find_relationships(split_list):
    # 连接到Neo4j数据库
    graph = Graph("bolt://localhost:7687", auth=('neo4j', '12345678'))

    query_idtype = f"MATCH (n)-[r:]->(m) WHERE n.id ='{former_node_id[0]}' AND m.name = '{split_list}' RETURN m.id, m.type"
    result_idtype = graph.run(query_idtype)
    for record in result_idtype:
        node_id = record["m.id"]
        node_type = record["m.type"]
        if node_type == 'method' or node_type == 'attribute':
            query_next = f"MATCH (n)-[r:]->(o)-[r:]->(p)-[r:]->(m) WHERE n.id = '{former_node_id[0]}' AND o.id = '{node_id[0]}' RETURN m.name"
        else:
            query_next = f"MATCH (n)-[r:]->(o)-[r:]->(m) WHERE n.id = '{former_node_id[0]}' AND o.id = '{node_id[0]}' RETURN m.name"
        result_next = graph.run(query_next)
        next_node = [record["m.name"] for record in result_next]
        global former_node_id
        former_node_id = record["n.id"]
    return next_node



def find_relationships_final(split_list): # 如果是列表中最后一个
    # 连接到Neo4j数据库
    graph = Graph("bolt://localhost:7687", auth=('neo4j', '12345678'))
    query_idtype = f"MATCH (n)-[r:]->(m) WHERE n.id ='{former_node_id[0]}' AND m.name = '{split_list}' RETURN m.id, m.type"
    result_idtype = graph.run(query_idtype)
    for record in result_idtype:
        node_id = record["m.id"]
        node_type = record["m.type"]
        if node_type == 'method' or node_type == 'attribute':
            query_next = f"MATCH (n)-[r:]->(o)-[r:]->(p)-[r:]->(m) WHERE n.id = '{former_node_id[0]}' AND o.id = '{node_id[0]}' RETURN m.name"
        else:
            query_next = f"MATCH (n)-[r:]->(o)-[r:]->(m) WHERE n.id = '{former_node_id[0]}' AND o.id = '{node_id[0]}' RETURN m.name"
        result_next = graph.run(query_next)
        next_node = [record["m.name"] for record in result_next]
    return next_node



string = input("请输入字符串: ")
split_lists = string.split('.')
print(split_lists)

for index, split_list in enumerate(split_lists):
    if index == 0:
        find_relationships_first(split_list)
    elif index == len(split_lists) - 1:
        find_relationships_final(split_list)
    else:
        find_relationships(split_list)