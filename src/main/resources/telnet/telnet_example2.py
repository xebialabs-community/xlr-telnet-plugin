#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import telnetlib , socket, sys

class TELNET2(object):

    def __init__(self):
        self.tn = None
        self.username = "root"
        self.password = "12345678"
        self.host = "rainmaker.wunderground.comxxx"
        self.port = 3000
        self.timeout = 5
        self.login_prompt = b"login: "
        self.password_prompt = b"Password: "

    def connect(self):
        try :
            self.tn = telnetlib.Telnet(self.host,self.port,self.timeout)
        except:
            print("connection failed")
            sys.exit(1)

        try:
            print("About to try")
            output = self.tn.read_until("Press Return to continue:XXX", self.timeout)
            print("Succeeded")
        except:
            print("TELNET.connect() socket.timeout")
            sys.exit(1)
        #print(output)
        self.tn.write(b"\r\n")
        output = self.tn.read_until("city code-- ", self.timeout)
        #print(output)
        print("about to enter city code")
        self.tn.write(b"nyc\r\n")
        '''self.tn.read_until(self.login_prompt, self.timeout) 
        self.tn.write(self.username.encode('ascii') + b"\n")

        if self.password :
            self.tn.read_until(self.password_prompt,self.timeout)
            self.tn.write(self.password.encode('ascii') + b"\n")'''

    def write(self,msg):
        self.tn.write(msg.encode('ascii') + b"\n")
        return True


    def read_until(self,value):
        return self.tn.read_until(value)


    def read_all(self):
        try :
            return self.tn.read_all().decode('ascii')
        except socket.timeout :
            print("read_all socket.timeout")
            return False

    def close(self):
        self.tn.close()
        return True


    def request(self,msg):
        self.__init__()
        self.connect()
        print("Connected")
        if self.write(msg) == True :
            print("in True")
            #self.close()
            resp = self.read_all()
            self.close()
            print("This is the response - %s" % resp)
            return resp
        else :
            return False

telnet = TELNET2()

#call request function 
print("Telnet created, about to request")
resp = telnet.request("X\r\n") # it will be return ps output
print(resp) 
