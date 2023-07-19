# 处理前端查询的请求，查询与指定节点有关系的节点信息以及它们之间的关系，并将结果封装为 JSON 文件，并作为 HTTP 响应返回给前端
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from py2neo import Graph, Node, Relationship

def create_node(graph, label, properties):
    node = Node(label, **properties)
    graph.create(node)
    return node

def create_relationship(graph, start_node, relation_type, end_node):
    relationship = Relationship(start_node, relation_type, end_node)
    graph.create(relationship)

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

@csrf_exempt
def query_related_nodes(request):
    if request.method == 'POST':
        data = request.POST
        node_name = data.get('node_name')

        related_nodes = find_related_nodes(node_name)

        if related_nodes:
            nodes_data = []
            links_data = []

            for idx, (relationship, related_node) in enumerate(related_nodes):
                start_node = relationship.start_node
                end_node = relationship.end_node
                start_node_properties = dict(start_node)
                end_node_properties = dict(end_node)
                link_properties = dict(relationship)

                nodes_data.append({"id": start_node_properties["name"], "label": start_node.labels.pop()})
                nodes_data.append({"id": end_node_properties["name"], "label": end_node.labels.pop()})

                link_data = {
                    "source": start_node_properties["name"],
                    "target": end_node_properties["name"],
                    "relation": link_properties["type"]
                }
                links_data.append(link_data)

            response_data = {
                "nodes": nodes_data,
                "links": links_data
            }

            return JsonResponse(response_data)

        else:
            return JsonResponse({"message": f"{node_name} 没有找到相关的节点信息"})


# urls中添加以下路由:
# path('query/', query_related_nodes, name='query_related_nodes'),