import sys
sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb')
from controller import main
from wsgiref.simple_server import make_server

httpd = make_server('', 8000, main.application)
print('Serving HTTP on port 8000...')
httpd.serve_forever()