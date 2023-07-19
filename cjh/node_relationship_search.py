from py2neo import Graph

def find_related_nodes(node_name):
    # 连接到Neo4j数据库
    graph = Graph("bolt://localhost:7687", auth=('neo4j', '12345678'))

    # 构建查询语句，匹配与给定节点名称相关的关系
    cypher_query = (
        f"MATCH (n {{name: '{node_name}'}})-[r]->(related) "
        "RETURN r, related"
    )

    result = graph.run(cypher_query)

    related_nodes = []
    for record in result:
        relationship = record["r"]
        related_node = record["related"]
        related_nodes.append((relationship, related_node))

    return related_nodes

# 用户输入命名空间或类或方法或属性
node_name = input("请输入命名空间或类或方法或属性的名称：")

related_nodes = find_related_nodes(node_name)

if related_nodes:
    print(f"{node_name} 相关的节点信息：")
    for relationship, related_node in related_nodes:
        print(f"关系：{relationship}")
        print(f"相关节点信息：{related_node}")
        print("-" * 20)
else:
    print(f"{node_name} 没有找到相关的节点信息")
print('End...')
