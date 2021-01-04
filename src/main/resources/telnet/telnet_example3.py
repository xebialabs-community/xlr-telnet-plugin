#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import logging
import sys
import telnetlib
import binascii
import socket

quitCommand = b"quit\r\n"

class TELNET3(object):

    def __init__(self):
        self.tn = None
        self.username = "root"
        self.password = "12345678"
        #self.host = "scn.org"
        #self.port = 23

        #self.host = "rainmaker.wunderground.com"
        #self.port = 3000

        self.host = "telehack.com"
        self.port = 23
        
        self.timeout = 30
        self.login_prompt = b"login: "
        self.password_prompt = b"Password: "
        

    '''def connect(self):
        try :
            self.tn = telnetlib.Telnet(self.host,self.port,self.timeout)
        except:
            print("connection failed")
            sys.exit(1)

        try:
            print("About to try")
            output = self.read_expect(self.login_prompt)
            print("Succeeded- output = %s" % output)
            print("About to write")
            didWrite = self.write(b"visitor\r\n")
            print("didWrite = %s, visitor\r\n" % didWrite)
            output = self.read_expect("")
            didWrite = self.write(b"\r\n")
            print("didWrite1 = %s, \r\n" % didWrite)
            output = self.read_expect("")
            didWrite = self.write(b"\r\n")
            print("didWrite2 = %s, \r\n" % didWrite)
            output = self.read_expect("")
            didWrite = self.write(b"\r\n")
            print("didWrite3 = %s, \r\n" % didWrite)
            output = self.read_expect("")
            didWrite = self.write(b"\r\n")
            print("didWrite4 = %s, \r\n" % didWrite)
            output = self.read_expect("")
            didWrite = self.write(b"\r\n")
            print("didWrite5 = %s, \r\n" % didWrite)

            output = self.read_expect("Your Choice ==> ")
            print(output)
            self.write(b"2\r\n")
            print("didWrite = %s, 2\r\n" % didWrite)
            output = self.read_expect("Your Choice ==> ")
            print(output)
            self.write(b"x\r\n")
            print("didWrite = %s, x\r\n" % didWrite)
            output = self.read_expect("Your Choice ==> ")
            print(output)
        except Exception, e:
            print("Exception thrown, %s" % str(e))
            sys.exit(1)'''

    '''def connect(self):
        try :
            self.tn = telnetlib.Telnet(self.host,self.port,self.timeout)
        except:
            print("connection failed")
            sys.exit(1)

        try:
            print("About to try")
            output = self.read_expect("Press Return to continue:")
            print("Succeeded- output = %s" % output)
            print("About to write")
            didWrite = self.write(b"\r\n")
            print("didWrite = %s, \r\n" % didWrite)
            output = self.read_expect("city code-- ")
            didWrite = self.write(b"nyc\r\n")
            print("didWrite1 = %s, nyc\r\n" % didWrite)
            
        except Exception, e:
            print("Exception thrown, %s" % str(e))
            sys.exit(1)'''

    def connect(self):
        try :
            self.tn = telnetlib.Telnet(self.host,self.port,self.timeout)
        except:
            print("connection failed")
            sys.exit(1)

        try:
            print("About to try")
            output = self.read_expect(b"forever.")
            print("Succeeded- output = %s" % output)
            output = self.read_expect(b".")
            print("Succeeded- output = %s" % output)
            print("About to write")
            didWrite = self.write(b"date\r\n")
            print("didWrite = %s, date\r\n" % didWrite)
            theDate = self.read_expect(b"CST")
            output = self.read_expect(".")
            print("Succeed - %s" % output)
            #didWrite = self.write(b"nyc\r\n")
            #print("didWrite1 = %s, nyc\r\n" % didWrite)
            return theDate
        except Exception, e:
            print("Exception thrown, %s" % str(e))
            sys.exit(1)


    def write(self,msg):
        print("In the write method")
        theMsg = msg.encode('ascii')
        print("Will write %s" % theMsg)
        self.tn.write(theMsg)
        return True


    def read_expect(self, value):
        print("About to read_expect prompt -> %s" % value)
        indexOfMatch, matchedText, output = self.tn.expect([value], self.timeout)
        if indexOfMatch == -1:
            # We could not find requested text
            msg = ("Unable to find match for key = %s, output text = %s " % (value, output))
            print(msg)
            sys.exit(1)
        else:
            print("OUTPUT - %s" % output)
            return output


    def read_all(self):
        try :
            readAll = self.tn.read_all()
            print("READALL = %s" % readAll)
            return self.tn.read_all().decode('ascii')
        except socket.timeout :
            print("read_all socket.timeout")
            return False

    def close(self):
        self.tn.close()
        return True


    def request(self,msg):
        self.__init__()
        theData = self.connect()
        print("Finished Connect, the data is %s" % theData)
        #resp = self.read_all()
        if self.write(msg) == True :
            print("in True")
            #self.close()
            #resp = self.read_all()
            print("About to close")
            self.close()
            return theData
        else :
            return False

telnet = TELNET3()

#call request function 
print("Telnet created, about to request TELNET3")
resp = telnet.request("EXIT\r\n") # it will be return ps output
print("The final response = %s" % resp) 
