from config import api_host, api_port
from api import app


if __name__ == '__main__':
    app.run(host=api_host, port=api_port)
