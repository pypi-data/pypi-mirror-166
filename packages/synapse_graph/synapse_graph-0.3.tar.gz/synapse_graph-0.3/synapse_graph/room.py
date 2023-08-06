class Room:
    name: str | None
    canonical_alias: str | None
    joined_members: int
    room_id: str

    def __init__(
            self,
            name: str | None,
            canonical_alias: str | None,
            joined_members: int,
            room_id: str,
    ):
        self.name = name
        self.canonical_alias = canonical_alias
        self.joined_members = joined_members
        self.room_id = room_id

    def __str__(self):
        if self.canonical_alias is None:
            return self.room_id
        else:
            return self.canonical_alias
