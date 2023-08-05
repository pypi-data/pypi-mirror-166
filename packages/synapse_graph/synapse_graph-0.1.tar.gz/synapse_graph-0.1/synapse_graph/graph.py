import requests
from pyvis.network import Network
from synapse_graph import User
from synapse_graph.room import Room


class SynapseGraphError(Exception):
    text: str

    def __init__(self, text: str = 'Unknown Error'):
        self.text = text

    def __str__(self):
        return self.text


class SynapseGraph:
    rooms: list = []
    users: list = []
    external_users: list = []
    graph_name: str

    user_servers_stats = {

    }

    HEADERS: dict
    MATRIX_HOMESERVER: str

    graph: Network

    user_node_color: str
    ext_user_node_color: str
    room_node_color: str

    min_room_d: int = 10
    max_room_d: int = 30

    def __init__(self, name: str, headers: dict, matrix_homeserver: str,
                 user_node_color: str = '#326051', room_node_color: str = '#99a9af',
                 ext_user_node_color: str = '#B4976D'):
        self.graph_name = name
        self.HEADERS = headers
        self.MATRIX_HOMESERVER = matrix_homeserver
        self.graph = Network('100%', '100%')
        self.user_node_color = user_node_color
        self.room_node_color = room_node_color
        self.ext_user_node_color = ext_user_node_color

    def __str__(self):
        return self.graph_name

    def show(self, file_name: str = 'nx') -> None:
        """Render and open graph to html"""

        self.graph.options = {
            "physics": {
                "barnesHut": {
                    "theta": 0.6,
                    "gravitationalConstant": -22200,
                    "centralGravity": 0.15,
                    "springLength": 170
                },
                "minVelocity": 1.4,
                "timestep": 0.49
            }
        }

        self.graph.show(f'{file_name}.html')

    def clear(self):
        """Clear all collected data"""

        self.rooms.clear()
        self.users.clear()

    def apply_nodes_to_graph(self, hide_user_name: bool = True) -> None:
        """Apply nodes to graph"""

        # Users
        for user in self.users:
            self.graph.add_node(
                n_id=str(user),
                color=self.user_node_color,
                label='user' if hide_user_name else str(user),
                size=5
            )

        # Rooms
        min_joined_users: int
        max_joined_users: int

        first: bool = True
        for room in self.rooms:
            if first:
                min_joined_users = max_joined_users = room.joined_members
                first = False
            else:
                if room.joined_members < min_joined_users:
                    min_joined_users = room.joined_members

                if room.joined_members > max_joined_users:
                    max_joined_users = room.joined_members

        for room in self.rooms:
            if room.joined_members != min_joined_users:
                node_size: float = ((self.max_room_d - self.min_room_d) / (100 / (
                        (room.joined_members / (max_joined_users - min_joined_users)) * 100))) + self.min_room_d
            else:
                node_size = room.joined_members + self.min_room_d
            self.graph.add_node(n_id=str(room), label=str(room), color=self.room_node_color, size=node_size)

    def load_local_users(self, filtered_users: tuple = ()) -> None:
        """Load users list form homeserver"""

        response = requests.get(f'https://{self.MATRIX_HOMESERVER}/_synapse/admin/v2/users?dir=f&from=0&guests=false',
                                headers=self.HEADERS)
        if response.ok:
            for user in response.json()['users']:
                if len(filtered_users) != 0:
                    if user['name'] in filtered_users:
                        self.users.append(User(
                            name=user['name'],
                            admin=user['admin'],
                            deactivated=user['deactivated'],
                            avatar_url=user['avatar_url']
                        ))
                else:
                    self.users.append(User(
                        name=user['name'],
                        admin=user['admin'],
                        deactivated=user['deactivated'],
                        avatar_url=user['avatar_url']
                    ))
        else:
            raise SynapseGraphError(response.json()['error'])

    def load_local_rooms(self, hide_private: bool = True) -> None:
        """Load rooms list form homeserver"""

        response = requests.get(
            f'https://{self.MATRIX_HOMESERVER}/_synapse/admin/v1/rooms?dir=f&from=0&order_by=name',
            headers=self.HEADERS
        )

        if response.ok:
            for room in response.json()['rooms']:
                if hide_private and not room['public']:
                    continue

                self.rooms.append(
                    Room(
                        name=room['name'],
                        canonical_alias=room['canonical_alias'],
                        joined_members=room['joined_members'],
                        room_id=room['room_id']
                    )
                )
        else:
            raise SynapseGraphError(response.json()['error'])

    def load_external_users(self, hide_name: bool = True):
        """Load all external members in rooms and connect edges too"""

        for room in self.rooms:
            response = requests.get(
                f'https://{self.MATRIX_HOMESERVER}/_synapse/admin/v1/rooms/{room.room_id}/members?dir=b&from=0&order_by=id',
                headers=self.HEADERS
            )

            if response.ok:
                for member in response.json()['members']:
                    if member not in self.external_users:
                        self.external_users.append(member)

                    self.graph.add_node(
                        member,
                        color=self.ext_user_node_color,
                        label='external user' if hide_name else member,
                        size=5
                    )
                    self.graph.add_edge(str(member), str(room))

    def calculate_edges(self) -> None:
        """Calculate edges for nodes"""

        for user in self.users:
            response = requests.get(
                f'https://{self.MATRIX_HOMESERVER}/_synapse/admin/v1/users/'
                f'{str(user)}/joined_rooms?dir=b&from=0&order_by=id', headers=self.HEADERS)

            if response.ok:
                for room_id in response.json()['joined_rooms']:
                    for room in self.rooms:
                        if room.room_id == room_id:
                            self.graph.add_edge(str(user), str(room))

    def calculate_external_servers_stats(self) -> None:
        for ext_user in self.external_users:
            ext_user: str

            if self.user_servers_stats.get(ext_user.split(':')[1], False):
                self.user_servers_stats[ext_user.split(':')[1]] += 1
            else:
                self.user_servers_stats[ext_user.split(':')[1]] = 1

        pass
