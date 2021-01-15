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
        self.logoutStepsList = telnetServer['logoutStepsList']
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
        capturedFinalOutput = "There was no output"
        stepsSuccessful = True
        logger.debug("in runcommands - About to connect")
        ########### CONNECT ################
        try :
            telnet_connection = telnetlib.Telnet(self.host, self.port, self.timeout)
        except:
            msg = "Telnet connection failed"
            logger.debug(msg)
            print(msg)
            sys.exit(1)
        
        ########### LOGIN, IF NECESSARY ################
        if self.username is not None:
            logging.debug("Found username - %s , so will log in" % (self.username))
            capturedFinalOutput = self.login(telnet_connection)
            logger.debug("finished login, success")

        ########### RUN COMMANDS ################
        logger.debug("starting cmd loop")
        capturedFinalOutput, stepsSuccessful = self.processSteps(telnet_connection, variables["commandStepsList"], variables["separatorString"])
        if not stepsSuccessful:
            logger.debug("Run Command Steps Failed, capturedFinalOutput = %s" % capturedFinalOutput)
            output = self.closeout(telnet_connection)
            logger.debug("finished exit command loop")
            msg = "Run command steps failed"
            logger.debug(msg)
            print(msg)
            sys.exit(1)
        logger.debug("finished task loop")
        
        ########### LOGOUT and CLOSEOUT ################
        logger.debug("About to closeout after successful telnet_runcommands, about to logout (if necessary) and closeout")
        if self.username is not None:
            logging.debug("Found username - %s , so will logout" % (self.username))
            capturedFinalOutput, logoutSuccessful = self.logout(telnet_connection)
            logger.debug("finished logout, capturedFinalOutput = %s, was logout successful = %s" % (capturedFinalOutput, logoutSuccessful))
        output = self.closeout(telnet_connection)
        logger.debug("finished exit command loop")
        logger.debug("The returned string from read_all after closeout was %s" % (output))
        variables["returnedString"] = output
        logger.debug("The CapturedFinalOutput = %s" % capturedFinalOutput)

    def login(self, telnet_connection):
        logger.debug("In login")
        # Bail out if incorrectly configured, close the connection
        if self.loginStepsList is None:
            logger.debug("Username configured but there are no Login Steps")
            output = self.closeout(telnet_connection)
            logger.debug("finished exit command loop, output from closeout was %s" % output)
            msg = "There is a username configured for this Telnet Server, but there are no Login Steps"
            logger.debug(msg)
            print(msg)
            sys.exit(1)
        capturedFinalOutput, stepsSuccessful = self.processSteps(telnet_connection, self.loginStepsList, self.serverSeparator)
        # Bail out if login fails, close the connection
        if not stepsSuccessful:
            logger.debug("Login Failed, capturedFinalOutput = %s" % capturedFinalOutput)
            # We could not login so there is no need to logout - go directly to closeout
            output = self.closeout(telnet_connection)
            logger.debug("finished exit command loop, output from closeout was %s" % output)
            msg = "Login failed"
            logger.debug(msg)
            print(msg)
            sys.exit(1)
        #Successful login
        return capturedFinalOutput

    def logout(self, telnet_connection):
        logger.debug("In logout")
        capturedFinalOutput = ""
        stepsSuccessful = True
        if self.logoutStepsList is not None:
            capturedFinalOutput, stepsSuccessful = self.processSteps(telnet_connection, self.logoutStepsList, self.serverSeparator)
        # We will continue even if logout was unsuccessful or there were no logout steps
        return capturedFinalOutput, stepsSuccessful

    def closeout(self, telnet_connection):
        logger.debug("In closeout")
        capturedFinalOutput, stepsSuccessful = self.processSteps(telnet_connection, self.exitCommandsList, self.serverSeparator)
        logger.debug("Result from running exit commands - capturedFinalOutput = %s, stepSuccessful = %s" % (capturedFinalOutput, stepsSuccessful))
        logger.debug("about to run read_all")
        output = telnet_connection.read_all()
        logger.debug("Output from read_all = %s" % output)
        telnet_connection.close()
        return output



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
        finalOutput = ""
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
            logger.debug("##### begin - DEBUGING ATTEMPT TO MATCH #######")
            logger.debug("Value we are trying to match = %s", procPrompt)
            logger.debug("indexOfMatch = %d, output = %s" % (indexOfMatch, output) )
            #if matchedText is not 'None':
                #logger.debug("The matchedText is %s" % matchedText.group())
            logger.debug("Value we were looking for -> displayed in HEX = %s" % binascii.hexlify(procPrompt))
            logger.debug("Output we were searching through -> displayed in HEX = %s" % binascii.hexlify(output))
            logger.debug("##### end - DEBUGING ATTEMPT TO MATCH #######")
            finalOutput = output
            if indexOfMatch == -1:
                # We could not find requested text
                msg = ("Unable to find match for key = %s, This was the actual output %s" % (procPrompt, finalOutput))
                logger.debug(msg)
                print(msg)
                # Return False so calling code can bail out
                return finalOutput, False
            # Write command
            logger.debug("About to write value -> %s" % procCommand)
            telnet_connection.write(procCommand)
            logger.debug("\n*********************** END PROCESSING commandObj ******************************")
        return finalOutput, True
        

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
        # if the string contains the literal string [$username] or [$password], replace with actual username and password
        if '[$username]' in newstr:
            newstr = newstr.replace('[$username]', self.username.encode('ascii'))
        if '[$password]' in newstr:
            newstr = newstr.replace('[$password]', self.password.encode('ascii'))
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


        

    
