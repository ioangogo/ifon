import os
import time
from subprocess import Popen, PIPE
import re
import os
import socket

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip
os.system("clear")
uip=[]
macar=[]
lanip=get_lan_ip()
notorm=re.search(r"([1-9])\d+$", lanip)
notorm=notorm.group(0)
lanip=lanip.replace(str(notorm),"")
knowmac={"e8:99:c4:77:cb:41":"Huw", "18:87:96:e3:f9:75":"Ioan", "7c:6d:62:68:8f:ee":"Ioan 2","f8:e0:79:a7:99:1f":"Alex"}
def rescan():
 devnull = open(os.devnull, 'wb')
 
 p = [] # ip -> process
 for n in range(1, 100): # start ping processes
    ip = str(lanip) + "%d" % n
    p.append((ip, Popen(['ping', '-c', '3', ip], stdout=devnull)))
    #NOTE: you could set stderr=subprocess.STDOUT to ignore stderr also
 os.system("clear")
 while p:
     for i, (ip, proc) in enumerate(p[:]):
         if proc.poll() is not None: # ping finished
             p.remove((ip, proc)) # this makes it O(n**2)
             if proc.returncode == 0:
                 uip.append(ip)
 devnull.close()
 os.system("clear")
 for ipaddr in uip:
  pid = Popen(["arp", "-n", ipaddr], stdout=PIPE)
  s = pid.communicate()[0]
  mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s)
  macar.append(mac.group(0) if mac else "")
while True:
 os.system("clear")
 rescan()
 for dev in macar:
  if str(dev) in knowmac:
   print knowmac[dev], "is on the network"
   del macar[:]
 time.sleep(30)
 os.system("clear")
 print "Refreshing"
