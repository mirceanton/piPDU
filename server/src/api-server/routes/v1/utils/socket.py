from routes.v1.utils.rabbitmq import RabbitMQ

class Socket:
    def on(self):
        if self.state == True:
            return({
                'status': True,
                'payload': {}
            }), 304
        return RabbitMQ().sendMessage(id = self.id, state = True)

    def off(self):
        if self.state == False:
            return({
                'status': True,
                'payload': {}
            }), 304
        return RabbitMQ().sendMessage(id = self.id, state = False)

    def info(self):
        return ({
            'status': True,
            'payload': {
                "id": self.id,
                "state": self.state
            }
        }), 200

    def __init__(self, id: int):
        self.id = id
        self.state = True

sockets = []
for i in range(0, 15):
    sockets.append(Socket(i))

def allOn():
    return RabbitMQ().sendMessage(state = True)

def allOff():
    return RabbitMQ().sendMessage(state = False)

def setAllOn():
    for sck in socket.sockets:
        sck.state = True

    return ({
        'status': True,
        'payload': {}
    }), 200

def setAllOff():
    for sck in socket.sockets:
        sck.state = False
    
    return ({
        'status': True,
        'payload': {}
    }), 200
