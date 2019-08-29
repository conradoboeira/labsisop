import time
import BaseHTTPServer
import os
import platform
import subprocess
import sys
from time import sleep

HOST_NAME = '192.168.1.10'
PORT_NUMBER = 8000

class GetCpuLoad(object):
    '''
    classdocs
    '''


    def __init__(self, percentage=True, sleeptime = 1):
        '''
        @parent class: GetCpuLoad
        @date: 04.12.2014
        @author: plagtag
        @info: 
        @param:
        @return: CPU load in percentage
        '''
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
        '''
        http://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
        read in cpu information from file
        The meanings of the columns are as follows, from left to right:
            0cpuid: number of cpu
            1user: normal processes executing in user mode
            2nice: niced processes executing in user mode
            3system: processes executing in kernel mode
            4idle: twiddling thumbs
            5iowait: waiting for I/O to complete
            6irq: servicing interrupts
            7softirq: servicing softirqs

        #the formulas from htop 
             user    nice   system  idle      iowait irq   softirq  steal  guest  guest_nice
        cpu  74608   2520   24433   1117073   6176   4054  0        0      0      0


        Idle=idle+iowait
        NonIdle=user+nice+system+irq+softirq+steal
        Total=Idle+NonIdle # first line of file for all cpus

        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
        '''
        cpu_infos = {} #collect here the information
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            #compute for every cpu
            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')#remove empty elements
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                #update dictionionary
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        '''
        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)

        '''
        start = self.getcputime()
        #wait a second
        sleep(self.sleeptime)
        stop = self.getcputime()

        cpu_load = {}

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: CPU_Percentage})
        return cpu_load



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
        #stat_file = open('/proc/stat', 'r')
        #stat = stat_file.read().split('\n')[0].split(' ')
        #util = ((int(stat[2]) + int(stat[3]) + int(stat[4]))/10000.0) * 100
        x = GetCpuLoad()
        util = x.getcpuload()['cpu']

        #Memoria ram
        mem_file = open('/proc/meminfo', 'r')
        mem = mem_file.read().split('\n')
        total = int(mem[0].split()[1])/1000.0
        free = int(mem[1].split()[1])/1000.0
        usada = total - free

        #Versao do sistema
        os_file = open('/etc/os-release')
        os_stat = os_file.read().split('\n')
        versao = os_stat[4][13:-1]
        
        #Processos
        proc = subprocess.check_output(['ps']).replace('\n', '<br>').replace(']','').replace('[','')


        s.wfile.write("<html><head><title>Info do sistema</title></head>")
        s.wfile.write("<p>Data e Hora: %s<p>"%datahora)
        s.wfile.write("<p>Uptime: %s<p>"%uptime)
        s.wfile.write("<p>Processador: %s<p>"%cpu)
        s.wfile.write("<p>Velocidade: %s MHz<p>"%speed)
        s.wfile.write("<p>Utilizacao: %s %%<p>"%util)
        s.wfile.write("<p>Memoria RAM total: %s MB<p>"%total)
        s.wfile.write("<p>Memoria RAM usada: %s MB<p>"%usada)
        s.wfile.write("<p>Versao do sistema: %s<p>"%versao)
        s.wfile.write("<p>Lista de processos:<br> %s<p>"%proc)
        
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

