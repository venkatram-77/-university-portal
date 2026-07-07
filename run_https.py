import os
import sys
import ssl
from wsgiref import simple_server

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
import django
django.setup()
from django.core.handlers.wsgi import WSGIHandler

app = WSGIHandler()
host = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')

httpd = simple_server.make_server(host, port, app)
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
print(f"HTTPS server running on https://{host}:{port}/")
httpd.serve_forever()
