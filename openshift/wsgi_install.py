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
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta charset="utf-8">
  <title>Installing Weblate</title>
<style>
html {
  background: #f5f5f5;
  height: 100%;
}
body {
  color: #404040;
  font-family: "Helvetica Neue",Helvetica,"Liberation Sans",Arial,sans-serif;
  font-size: 14px;
  line-height: 1.4;
}
h1 {
  color: #000;
  line-height: 1.38em;
  margin: .4em 0 .5em;
  font-size: 25px;
  font-weight: 300;
  border-bottom: 1px solid #fff;
}
h1:after {
  content: "";
  display: block;
  height: 1px;
  background-color: #ddd;
}
p {
  margin: 0 0 2em;
}
pre {
  padding: 13.333px 20px;
  margin: 0 0 20px;
  font-size: 13px;
  line-height: 1.4;
  background-color: #fff;
  border-left: 2px solid rgba(120,120,120,0.35);
  font-family: Menlo,Monaco,"Liberation Mono",Consolas,monospace !important;
}
.content {
  display: table;
  margin-left: -15px;
  margin-right: -15px;
  position: relative;
  min-height: 1px;
  padding-left: 30px;
  padding-right: 30px;

}
</style>
</head>
<body>
  <div class="content">
    <h1>Installing Weblate</h1>

    <p>Weblate is beeing installed. Please wait a few minutes and refresh this page.</p>
             
    <pre>''' + \
os.popen('cat ${OPENSHIFT_DATA_DIR}/install.log | grep -v \'^ \'').read() + \
'''</pre>                
  </div>
</body>
</html>'''

  status = '200 OK'
  response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
  
  start_response(status, response_headers)
  return [response_body]
