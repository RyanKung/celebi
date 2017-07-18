# -*- eval: (venv-workon "celebi"); -*-
from celebi import wsgi_server

if __name__ == '__main__':
    wsgi_server().start()
