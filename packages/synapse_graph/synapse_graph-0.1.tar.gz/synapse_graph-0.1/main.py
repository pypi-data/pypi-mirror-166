import os
import synapse_graph

MATRIX_TOKEN = os.getenv('MATRIX_TOKEN')
MATRIX_HOMESERVER_DOMAIN = os.getenv('MATRIX_HOMESERVER_DOMAIN')
HEADERS = {
    'Authorization': f'Bearer {MATRIX_TOKEN}'
}

graph = synapse_graph.SynapseGraph(MATRIX_HOMESERVER_DOMAIN, HEADERS, MATRIX_HOMESERVER_DOMAIN)
graph.load_local_users()
graph.load_local_rooms(hide_private=True)
graph.apply_nodes_to_graph(hide_user_name=False)
graph.calculate_edges()
graph.load_external_users(hide_name=True)
graph.calculate_external_servers_stats()
graph.show()
