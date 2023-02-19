class Socket():
    def __init__(self, id: int):
        self.id = id
        self.state = True

    def info(self):
        return {
            'id': self.id,
            'state': self.state
        }

sockets = [Socket(i) for i in range(16)]
