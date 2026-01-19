class user:
    # username: string
    # address: tuple
    # inVC: bool
    # mute: bool
    # deaf: bool
    def __init__(self, username, address, inVC, mute, deaf):
        self.name = username
        self.address = address
        self.inVC = inVC
        self.mute = mute
        self.deaf = deaf

    def set(self, username=None, address=None, inVC=None, mute=None, deaf=None):
        # had to do like this because for example self.name is not accepted as default value
        username = username or self.name
        address = address or self.address
        inVC = inVC or self.inVC
        mute = mute or self.mute
        deaf = deaf or self.deaf
        self.name = username
        self.address = address
        self.inVC = inVC
        self.mute = mute
        self.deaf = deaf
