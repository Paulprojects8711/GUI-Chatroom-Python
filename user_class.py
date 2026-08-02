class user:
    # username: string
    # address: tuple
    # lastSeen: int
    # lastSent: string
    # inVC: bool
    # mute: bool
    # deaf: bool
    def __init__(self, username, address, lastSeen, lastSent, inVC, mute, deaf):
        self.name = username
        self.address = address
        self.lastSeen = lastSeen
        self.lastSent = lastSent
        self.inVC = inVC
        self.mute = mute
        self.deaf = deaf
