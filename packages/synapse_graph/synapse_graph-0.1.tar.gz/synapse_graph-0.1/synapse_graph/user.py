class User:
    name: str
    admin: bool
    deactivated: bool
    avatar_url: None | str
    rooms: list = []

    def __init__(self, name: str, admin: bool, deactivated: bool, avatar_url: None | str):
        self.name = name
        self.admin = admin
        self.deactivated = deactivated
        self.avatar_url = avatar_url

    def __str__(self):
        return self.name
