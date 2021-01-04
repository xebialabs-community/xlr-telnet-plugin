#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#from ispw.ISPWClientUtil import ISPWClientUtil

#params = {'url': configuration.url, 'cesToken':configuration.cesToken, 'username': configuration.username, 'password': configuration.password,
#          'proxyHost': configuration.proxyHost, 'proxyPort': configuration.proxyPort,
#          'proxyUsername': configuration.proxyUsername, 'proxyPassword': configuration.proxyPassword, 'enableSslVerification': configuration.enableSslVerification}

#path = configuration.checkConfigurationPath


#ispw_client = ISPWClientUtil.create_ispw_client(params)
#ispw_client.test_connection_client.get_version(path)

import logging
import sys
import telnetlib

from telnet.TelnetConnection import TelnetConnection

logger = logging.getLogger(__name__)

logger.debug("In connection_check")
params = {'telnetHost': configuration.telnetHost, 'telnetPort':configuration.telnetPort, 'username': configuration.username, 'password': configuration.password,
          'timeout': configuration.timeout, 'separatorString': configuration.separatorString, 'loginStepsList': configuration.loginStepsList, 'exitCommandsList': configuration.exitCommandsList }

telnet_connection = TelnetConnection.create_connection(params)
connectionSuccess = telnet_connection.testConnection(params)
