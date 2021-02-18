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

from telnet.TelnetConnection import TelnetConnection

logger = logging.getLogger(__name__)

logger.debug("In connection_check, note that we check only that we can connect to the telnet server. We do not test logging in and logging out.")
params = {'telnetHost': configuration.telnetHost, 'telnetPort':configuration.telnetPort, 'username': configuration.username, 'password': configuration.password,
          'timeout': configuration.timeout, 'separatorString': configuration.separatorString, 'loginStepsList': configuration.loginStepsList,
          'concurrentLoginIndicator': configuration.concurrentLoginIndicator, 'numberOfLoginRetries': configuration.numberOfLoginRetries,
          'intervalBetweenLoginRetries': configuration.intervalBetweenLoginRetries, 'concurrentLoginStepsList': configuration.concurrentLoginStepsList, 
          'logoutStepsList': configuration.logoutStepsList, 'exitCommandsList': configuration.exitCommandsList }

telnet_connection = TelnetConnection.create_connection(params)
connectionSuccess = telnet_connection.testConnection(params)
