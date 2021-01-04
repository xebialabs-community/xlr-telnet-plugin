#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import getpass
import sys
import telnetlib


HOST = "rainmaker.wunderground.com"
PORT = 3000
#user = raw_input("Enter your remote account: ")
#password = getpass.getpass()
print("About to connect")
tn = telnetlib.Telnet(HOST, PORT)
#print("About to read all")
#output = tn.read_all()
#print(output)


#output = tn.read_until("Press Return to continue:")
indexOfMatch, matchedText, output = tn.expect(["Press Return to continue:XXX"], 20)
        
if indexOfMatch == -1:
    # We could not find requested text
    msg = ("Unable to find match for key = %s, output text = %s " % ("Press Return to continue:XXX", output))
    print(msg)
    sys.exit(1)


print("output = %s" % output)
tn.write("\r\n")
#output = tn.read_all()
#print(output)
tn.read_until("city code-- ")
tn.write("nyc\r\n")
tn.write("X\r\n")

print tn.read_all()