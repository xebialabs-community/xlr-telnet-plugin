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

logger = logging.getLogger(__name__)

logger.debug("In TelnetConnection")

class CommandObject():
    def __init__(self, prompt="", command=""):
        self.prompt = prompt
        self.command = command

class TelnetConnection(object):
    def __init__(self, telnetServer, telnetUsername=None, telnetPassword=None):
        # TODO: bail out if server is not configured
        logger.debug("in telnet connection init")
        self.telnetServer = telnetServer
        self.host = telnetServer['telnetHost']
        self.port = telnetServer['telnetPort']
        self.serverSeparator = telnetServer['separatorString']
        self.loginStepsList = telnetServer['loginStepsList']
        self.exitCommandsList = telnetServer['exitCommandsList']
        self.username = telnetServer['username']
        self.password = telnetServer['password']
        self.timeout = telnetServer['timeout']
        
        if telnetUsername is not None:
            self.username = telnetUsername
        if telnetPassword is not None:
            self.password = telnetPassword

        

    @staticmethod
    def create_connection(telnetServer, username=None, password=None):
        logger.debug("in telnet connection static create_connection")
        return TelnetConnection(telnetServer, username, password)

    def testConnection(self, variables):
        logger.debug("in testConnection - About to connect")
        try :
            telnet_connection = telnetlib.Telnet(self.host, self.port, self.timeout)
        except:
            msg = "Telnet connection failed"
            logger.debug(msg)
            print(msg)
            sys.exit(1)
        telnet_connection.close()
        return True

    def telnet_runcommands(self, variables):
        logger.debug("in runcommands - About to connect")
        try :
            telnet_connection = telnetlib.Telnet(self.host, self.port, self.timeout)
        except:
            msg = "Telnet connection failed"
            logger.debug(msg)
            print(msg)
            sys.exit(1)
        
        # login here, if necessary
        if self.username is not None:
            logging.debug("Found username - %s , so will log in" % (self.username))
            # TODO: bail out if there are no loginsteps
            self.processSteps(telnet_connection, self.loginStepsList, self.serverSeparator)
            logger.debug("finished login")

        logger.debug("starting cmd loop")
        self.processSteps(telnet_connection, variables["commandStepsList"], variables["separatorString"])
        logger.debug("finished task loop")
        logger.debug("About to process the exit command list")
        self.processSteps(telnet_connection, self.exitCommandsList, self.serverSeparator)
        logger.debug("finished exit command loop")
        #exitCmd, containsPassword = self.processString(variables["exitCommand"].encode("ascii"))
        #logger.debug("The exit string (encoded and processed) -> %s" % (exitCmd))
        #logger.debug("The exit string (hexified) -> %s " % (binascii.hexlify(exitCmd)))
        #telnet_connection.write(exitCmd)
        logger.debug("about to read final string")
        output = telnet_connection.read_all()
        telnet_connection.close()
        logger.debug("The returned string was %s" % (output))
        variables["returnedString"] = output

    def processSteps(self, telnet_connection, strOfSteps, separator):
        logger.debug("In processSteps, strOfSteps is %s" % strOfSteps)
        listOfCommands = []
        #TODO: Create a list containing every line in the multiline variable
        listOfLines = strOfSteps.splitlines()
        logger.debug("ListOfLines is %s" % listOfLines)
        for line in listOfLines:
            logger.debug("the line is %s" % line)
            splitLineList = line.split(separator, 2)
            newCommand = CommandObject()
        # process the string - each line should be parsed into parts by removing the separator (prompt and command)
        # Create new command object for each line and place in listOfCommands list
            if len(splitLineList)>1:
                newCommand.prompt = splitLineList[0]
                newCommand.command = splitLineList[1]
            else:
                newCommand.command = splitLineList[0]
            
            listOfCommands.append(newCommand)
        
        for commandObj in listOfCommands:
            logger.debug("\n\n*********************** BEGING PROCESSING commandObj ******************************")
            logger.debug("prompt = %s" % commandObj.prompt)
            logger.debug("command = %s" % commandObj.command)
            # encode the strings
            prompt = commandObj.prompt.encode('ascii')
            command = commandObj.command.encode('ascii')
            self.debugKeyValue(prompt, command, False)
            # process the strings to correct XLR escaping behavior
            procPrompt, promptContainsPassword = self.processString(prompt)
            procCommand, commandContainsPassword = self.processString(command)
            self.debugKeyValue(procPrompt, procCommand, True, promptContainsPassword, commandContainsPassword)
            
            logger.debug("About to read_expect prompt -> %s" % procPrompt)

            indexOfMatch, matchedText, output = telnet_connection.expect([procPrompt], self.timeout)
        
            if indexOfMatch == -1:
                # We could not find requested text
                msg = ("Unable to find match for key = %s, output text = %s " % (procPrompt, output))
                logger.debug(msg)
                print(msg)
                sys.exit(1)

            logger.debug("Output = %s" % output)
            logger.debug("About to write value -> %s" % procCommand)
            telnet_connection.write(procCommand)
            logger.debug("\n*********************** END PROCESSING commandObj ******************************")
        
        '''for key, value in map.iteritems():
                # encode the strings
                key = key.encode('ascii')
                value = value.encode('ascii')
                self.debugKeyValue(key, value, False)
                # process the strings to correct XLR escaping behavior
                procKey, keyContainsPassword = self.processString(key)
                procValue, valueContainsPassword = self.processString(value)
                self.debugKeyValue(procKey, procValue, True, keyContainsPassword, valueContainsPassword)
                
                logger.debug("About to read_until key -> %s" % procKey)

                indexOfMatch, matchedText, output = telnet_connection.expect([procKey], self.timeout)
            
                if indexOfMatch == -1:
                    # We could not find requested text
                    msg = ("Unable to find match for key = %s, output text = %s " % (procKey, output))
                    logger.debug(msg)
                    print(msg)
                    sys.exit(1)

                logger.debug("Output = %s" % output)
                logger.debug("About to write value -> %s" % procValue)
                telnet_connection.write(procValue)'''

    def processString(self, theStr):
        # We don't want debuging to print out the password
        containsPassword = False
        logger.debug("In processString, processing %s" % theStr)
        # When XLR saves values into a map of String, String - special characters are escaped
        # When the user wishes to use non printable control charater,such as carriage return followed by new line, 
        #   they enter \r\n in the XLR task map. XLR then escapes the backslash, thereby changing the string from contol charaters to 
        #   literal backslashes follow by an alpha character - in hex 5c725c6e is saved rather than the control characters 0d0a
        # This processString method corrects the problem 
        newstr = theStr.replace('\\r', b'\r').replace('\\n', b'\n')
        logger.debug("newstr after first process %s" % newstr)
        # if the string contains the literal string |$username| or |$password|, replace with actual username and password
        if '|$username|' in newstr:
            newstr = newstr.replace('|$username|', self.username.encode('ascii'))
        if '|$password|' in newstr:
            newstr = newstr.replace('|$password|', self.password.encode('ascii'))
            containsPassword = True
        return newstr, containsPassword

    def debugKeyValue(self, prompt, command, hasBeenProcessed, promptContainsPassword = False, commandContainsPassword = False):
        if hasBeenProcessed:
            logger.debug("\n*** Processed ascii encoded Prompt and Command")
        else:
            logger.debug("\n*** Unprocessed ascii encoded Prompt and Command")
        if promptContainsPassword:
            prompt = "********"
        if commandContainsPassword:
            command = "********"
        logger.debug("In debugKeyValue - prompt = %s, command = %s" % (prompt,command))
        logger.debug("Converted to Hex - prompt = %s, command = %s" % (binascii.hexlify(prompt), binascii.hexlify(command)))


        

    
