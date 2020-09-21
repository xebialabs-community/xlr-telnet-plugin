#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import logging
import getpass
import sys
import telnetlib

from telnet.TelnetConnection import TelnetConnection

logger = logging.getLogger(__name__)

logger.debug("In telnet_task")

#ispw_client = ISPWClientUtil.create_ispw_client(ispwServiceServer, cesToken)
#method = str(task.getTaskType()).lower().replace('.', '_')
#call = getattr(ispw_client, method)
#output = call(locals())
print("in task, about to create connection")
print("telnetServer host = %s" % (telnetServer['telnetHost']))
print("telnetUsername = %s" % (telnetUsername))
print("telnetPassword = %s" % (telnetPassword))
telnet_connection = TelnetConnection.create_connection(telnetServer, telnetUsername, telnetPassword)
method = str(task.getTaskType()).lower().replace('.', '_')
call = getattr(telnet_connection, method)
output = call(locals())
