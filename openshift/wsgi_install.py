#!/usr/bin/python
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

def application(environ, start_response):

  ctype = 'text/html'
  response_body = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <title>Installing Weblate</title>
</head>
<body>
  <h1>Installing Weblate</h1>
  Weblate is beeing installed. Please wait a few minutes and refresh this page.
</body>
</html>'''

  status = '200 OK'
  response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
  
  start_response(status, response_headers)
  return [response_body]
