import time
import BaseHTTPServer
import os
import platform

HOST_NAME = '192.168.1.10'
PORT_NUMBER = 8000


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        
        # TIME
        os.environ['TZ']= 'UTC+3'
        time.tzset()
        datahora = os.popen('date').read()

        # UPTIME
        uptime_file = open("/proc/uptime", 'r')
        uptime = uptime_file.read().split(" ")[0]

        #CPU
        cpu_file = open('/proc/cpuinfo', 'r')
        cpu_file = cpu_file.read().split('\n')
        cpu = cpu_file[4].split(":")[1]
        speed = cpu_file[6].split(":")[1]
    
        #Utilizacao cpu
        stat_file = open('/proc/stat', 'r')
        stat = stat_file.read().split('\n')[0].split(' ')
        util = ((int(stat[1]) + int(stat[2]) + int(stat[3]))/10000.0) * 100

        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        s.wfile.write("<p>Data e Hora: %s<p>"%datahora)
        s.wfile.write("<p>Uptime: %s<p>"%uptime)
        s.wfile.write("<p>Processador: %s<p>"%cpu)
        s.wfile.write("<p>Velocidade: %s MHz<p>"%speed)
        s.wfile.write("<p>Utilizacao: %s<p>"%util)
        
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

