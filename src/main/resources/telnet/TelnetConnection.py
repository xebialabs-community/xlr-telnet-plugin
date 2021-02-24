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
import time
from TelnetUtils import debugPromptCommand
from TelnetUtils import checkForErrorCondition

logger = logging.getLogger(__name__)

logger.debug("In TelnetConnection")

errorStateList = ["NO_CONNECTION", "NOT_LOGGED_IN", "CONCURRENT_LOGIN", "ERROR_AFTER_LOGIN", "FAILED_FINAL_TEST"]

class CommandObject():
    def __init__(self, prompt="", command=""):
        self.prompt = prompt
        self.command = command

class TelnetConnection(object):
    def __init__(self, telnetServer, telnetUsername=None, telnetPassword=None):
        logger.debug("In telnet connection init")
        if telnetServer is None:
            msg = "Please choose a Telnet Server for this task"
            logger.debug(msg)
            print(msg)
            sys.exit(1)
        self.telnetServer = telnetServer
        self.host = telnetServer['telnetHost']
        self.port = telnetServer['telnetPort']
        self.serverSeparator = telnetServer['separatorString']
        self.loginStepsList = telnetServer['loginStepsList']
        self.loginErrorIndicatorList = telnetServer['loginErrorIndicatorList']
        self.concurrentLoginIndicator = telnetServer['concurrentLoginIndicator']
        self.numberOfLoginRetries = telnetServer['numberOfLoginRetries']
        self.intervalBetweenLoginRetries = telnetServer['intervalBetweenLoginRetries']
        self.concurrentLoginStepsList = telnetServer['concurrentLoginStepsList']
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
        logger.debug("Creating a new Telnet Connection")
        return TelnetConnection(telnetServer, username, password)

    def testConnection(self, variables):
        telnet_connection = None
        try :
            telnet_connection = telnetlib.Telnet(self.host, self.port, self.timeout)
        except:
            msg = "Telnet connection failed"
            self.errorOut(telnet_connection, msg, "NO_CONNECTION")
        # success
        telnet_connection.close()
        return True

    def telnet_runcommands(self, variables):
        logger.debug("\n\n\n$$$$$$$$$$$$$$$$ BEGIN RUN COMMANDS $$$$$$$$$$$$$$$$")
        capturedFinalOutput = ""
        stepsSuccessful = True
        errorConditionFound = False
        concurrentLoginFound = False
        errorMsg = "No error found"
        
        logger.debug("About to connect")
        ########### CONNECT ################
        telnet_connection = None
        try :
            telnet_connection = telnetlib.Telnet(self.host, self.port, self.timeout)
        except:
            msg = "Telnet connection failed"
            self.errorOut(telnet_connection, msg, "NO_CONNECTION")
        
        ########### LOGIN, IF NECESSARY ################
        logger.debug("self.username is %s" % self.username)
        if self.username is not None:
            logging.debug("Found username - %s , so will log in" % (self.username))
            capturedFinalOutput = self.login(telnet_connection)
            logger.debug("Finished login, success")

        ########### RUN COMMANDS ################
        logger.debug("Starting running command steps")
        errorConditionList = []
        if variables["errorConditionIndicatorList"] is not None:
            errorConditionList = variables["errorConditionIndicatorList"].splitlines()
        
        capturedFinalOutput, stepsSuccessful, errorConditionFound, concurrentLoginFound, errorMsg = self.processSteps(telnet_connection, variables["commandStepsList"], variables["separatorString"], errorConditionList)
        if errorConditionFound:
            logger.debug("Run command steps failed, error condition discovered")
            if self.username is not None:
                logging.debug("Found username")
                self.errorOut(telnet_connection, msg, "ERROR_AFTER_LOGIN")  
            else:
                self.errorOut(telnet_connection, msg, "NOT_LOGGED_IN")

        if not stepsSuccessful:
            logger.debug("Run Command Steps Failed, capturedFinalOutput = %s" % capturedFinalOutput)
            if self.username is not None:
                logging.debug("Found username")
                self.errorOut(telnet_connection, msg, "ERROR_AFTER_LOGIN")  
            else:
                self.errorOut(telnet_connection, msg, "NOT_LOGGED_IN")
        # Success so far, so continure
        logger.debug("Finished running command steps")
        
        ########### LOGOUT and CLOSEOUT ################
        logger.debug("About to closeout after successful telnet_runcommands, about to logout (if necessary) and closeout")
        if self.username is not None:
            logging.debug("Found username - %s , so will logout" % (self.username))
            logoutOutput, logoutSuccessful = self.logout(telnet_connection, errorConditionList)
            logger.debug("Finished logout, logoutOutput = %s, was logout successful = %s" % (logoutOutput, logoutSuccessful))
        capturedFinalOutput, output = self.closeout(telnet_connection, errorConditionList)
        logger.debug("Finished exit command loop")
        logger.debug("The CapturedFinalOutput = %s" % capturedFinalOutput)
        logger.debug("The returned string from read_all after closeout = %s" % (output))
        # Trim output strings
        if capturedFinalOutput is not None:
            capturedFinalOutput = capturedFinalOutput.strip()
            logger.debug("After removing starting and trailing empty spaces - capturedFinalOutput = %s" % capturedFinalOutput)
        else:
            capturedFinalOutput = ""
        if output is not None:
            output = output.strip()
            logger.debug("After removing starting and trailing empty spaces - output = %s" % output)
        else:
            output = ""

        # Test for error Condition based upon configured errorConditionIndicatorList (errorConditionList)
        # We have already logged and closed out, If we find an error here, we will fail the task 
        errorConditionFound, concurrentLoginFound, errorMsg = checkForErrorCondition(capturedFinalOutput, errorConditionList, None)
        if errorConditionFound:
            self.errorOut(telnet_connection, errorMsg, "NO_CONNECTION")
        errorConditionFound, concurrentLoginFound, errorMsg = checkForErrorCondition(output, errorConditionList, None)
        if errorConditionFound:
            self.errorOut(telnet_connection, errorMsg, "NO_CONNECTION")

        # Test for failure condition based upon configured failIfEmptyLastOutput and failIfEmptyFinalString
        if variables["failIfEmptyExitOutput"]:
            logger.debug("Testing exitOutput because we must have a value, capturedFinalOutput = %s" % capturedFinalOutput)
            if len(capturedFinalOutput) == 0:
                errorMsg = "Last Output was empty, will fail the task"
                self.errorOut(telnet_connection, errorMsg, "NO_CONNECTION")
        if variables["failIfEmptyFinalString"]:
            logger.debug("Testing returnedString/ final output because we must have a value, output = %s" % output)
            if len(output) == 0:
                errorMsg = "Final Output was empty, will fail the task"
                self.errorOut(telnet_connection, errorMsg, "NO_CONNECTION")

        ########### SUCCESS ################
        variables["exitOutput"] = capturedFinalOutput
        variables["returnedString"] = output



############# Login, Logout, Closeout Methods ##################
    def login(self, telnet_connection):
        logger.debug("In login")
        loginErrorList = []
        if self.loginErrorIndicatorList is not None:
            loginErrorList = self.loginErrorIndicatorList.splitlines()
        loginRetryCounter = 0
        # Bail out if incorrectly configured, close the connection
        if self.loginStepsList is None:
            errorMsg = "There is a username configured for this Telnet Server, but Login Steps have not been configured"
            self.errorOut(telnet_connection, errorMsg, "NOT_LOGGED_IN")

        capturedFinalOutput, stepsSuccessful, errorConditionFound, concurrentLoginFound, errorMsg = self.processSteps(telnet_connection, 
                self.loginStepsList, self.serverSeparator, loginErrorList, self.concurrentLoginIndicator)

        if errorConditionFound:
            # login error string found
            self.errorOut(telnet_connection, errorMsg, "NOT_LOGGED_IN")
        
        # Testing for Concurrent Login condition
        # if concurrentLoginFound - this means a concurrent login was discovered 
        #       so - while still concurrentLoginFound and numberOfLoginRetries > 0, run the concurrentLoginStepsList steps
        # 

        # ensure there are concurrentLoginSteps
        if concurrentLoginFound and self.concurrentLoginStepsList is None:
            errorMsg = errorMsg + " Concurrent Login Condition discovered but Concurrent Login Steps have not been configured"
            self.errorOut(telnet_connection, errorMsg, "CONCURRENT_LOGIN")

        while concurrentLoginFound and loginRetryCounter < self.numberOfLoginRetries:
            logger.debug(("Found concurrent login condition, will try again - errorMsg = %s, loginRetryCounter = %d" % (errorMsg, loginRetryCounter))) 
            pollingInterval = int(self.intervalBetweenLoginRetries)
            time.sleep(pollingInterval)
            # try logging in again but use retry login steps
            capturedFinalOutput, stepsSuccessful, errorConditionFound, concurrentLoginFound, errorMsg = self.processSteps(telnet_connection, 
                self.concurrentLoginStepsList, self.serverSeparator, loginErrorList, self.concurrentLoginIndicator)
            loginRetryCounter += 1
        # If we still have a concurrent login error but have exhausted retries, we need to logout and close out then exit
        if loginRetryCounter >= self.numberOfLoginRetries and concurrentLoginFound:
            errorMsg = errorMsg + "Concurrent Login condition discovered and retries have exceeded the configured limit."
            self.errorOut(telnet_connection, errorMsg, "CONCURRENT_LOGIN")

        # Bail out if login fails, close the connection
        if not stepsSuccessful:
            logger.debug("Login Failed, capturedFinalOutput = %s" % capturedFinalOutput)
            errorMsg = "Login failed"
            self.errorOut(telnet_connection, errorMsg, "NOT_LOGGED_IN")
        
        #Successful login
        return capturedFinalOutput

    def logout(self, telnet_connection, errorConditionList=None):
        logger.debug("In logout")
        capturedFinalOutput = ""
        stepsSuccessful = True
        errorConditionFound = False
        concurrentLoginFound = False
        errorMsg = "No error found"
        if self.logoutStepsList is not None:
            capturedFinalOutput, stepsSuccessful, errorConditionFound, concurrentLoginFound, errorMsg = self.processSteps(telnet_connection, 
                self.logoutStepsList, self.serverSeparator, errorConditionList, None)
        if errorConditionFound:
            # If we detect a task error condition while logging out, we will error out (which will retry logout without looking for errors)
            # This may be problematic because the logout steps may not be configured in a way that will work after we have already run some
            # some logout steps. Better to configure the task steps to discover this error rather than have it discovered during logout
            self.errorOut(telnet_connection, errorMsg, "ERROR_AFTER_LOGIN")
        # We will check to see if logout was successful, we will just return to the caller so the next step (closeout) will run
        return capturedFinalOutput, stepsSuccessful

    def closeout(self, telnet_connection, errorConditionList=None):
        logger.debug("In closeout")
        capturedFinalOutput = ""
        stepsSuccessful = True
        errorConditionFound = False
        concurrentLoginFound = False
        errorMsg = "No error found"
        capturedFinalOutput, stepsSuccessful, errorConditionFound, concurrentLoginFound, errorMsg = self.processSteps(telnet_connection, self.exitCommandsList, 
            self.serverSeparator, errorConditionList, None)
        logger.debug("Checking for errorConditionFound")
        if errorConditionFound:
            self.errorOut(telnet_connection, errorMsg, "NOT_LOGGED_IN")
        logger.debug("Result from running exit commands - capturedFinalOutput = %s, stepSuccessful = %s" % (capturedFinalOutput, stepsSuccessful))
        logger.debug("about to run read_all")
        output = ""
        # In some cases, where a command is run but no output is produced, read_all times out. 
        # We will ignore the failure and instead depend upon the failIfEmptyExitOutput and failIfEmptyFinalString task configuration 
        #  (handled by caller) to determine success or failure.
        try :
            output = telnet_connection.read_all()
        except:
            msg = "read_all failed"
            logger.debug(msg)
        logger.debug("Output from read_all = %s" % output)
        telnet_connection.close()
        return capturedFinalOutput, output

############# Utility Methods ##################

    def errorOut(self, telnet_connection, msg, currentState):
        logger.debug("In errorOut with currentState %s, error message = %s " % (currentState, msg))
        global errorStateList
        if currentState not in errorStateList:
            msg = "Plugin Error - attempt to process unkown error state - %, original error msg - " % (currentState, msg)
        # determine state
        # states 
        # - no connection so just fail - NO_CONNECTION
        # - Failed during login, just close out - NOT_LOGGED_IN
        # - Failed because of concurrent login, must logout and close - CONCURRENT_LOGIN
        # - Failed during command execution, must logout (if there is a username) and must close out - ERROR_AFTER_LOGIN
        # - already logged out and closed out but fail 'must not be empty tests - FAILED_FINAL_TEST

        if currentState == "NOT_LOGGED_IN":
            self.closeout(telnet_connection)
        elif currentState == "CONCURRENT_LOGIN":
            self.logout(telnet_connection)
            self.closeout(telnet_connection)
        elif currentState == "ERROR_AFTER_LOGIN":
            self.logout(telnet_connection)
            self.closeout(telnet_connection)
        # ALL STATES including NO_CONNECTION and FAILED_FINAL_TEST
        print(msg)
        sys.exit(1)
        


    def processSteps(self, telnet_connection, strOfSteps, separator, errorConditionList=None, concurrentLoginIndicator=None):
        logger.debug("In processSteps")
        errorConditionFound = False
        concurrentLoginFound = False
        errorMsg = "No errors found"
        listOfCommands = []
        listOfLines = strOfSteps.splitlines()
        # logger.debug("ListOfLines is %s" % listOfLines)
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
            # debugPromptCommand(prompt, command, False)
            # process the strings to correct XLR escaping behavior
            procPrompt, promptContainsPassword = self.processString(prompt)
            procCommand, commandContainsPassword = self.processString(command)
            #self.debugPromptCommand(procPrompt, procCommand, True, promptContainsPassword, commandContainsPassword)
            
            logger.debug("About to read_expect")

            indexOfMatch, matchedText, output = telnet_connection.expect([procPrompt], self.timeout)
            logger.debug("##### begin - DEBUGING ATTEMPT TO MATCH #######")
            if promptContainsPassword:
                logger.debug("Prompt contains password so we cannot log debug information.")    
            else:
                logger.debug("Value we were trying to match = %s", procPrompt)
                logger.debug("indexOfMatch = %d, output = %s" % (indexOfMatch, output) )
                #if matchedText is not 'None':
                    #logger.debug("The matchedText is %s" % matchedText.group())
                logger.debug("Value we were looking for -> displayed in HEX = %s" % binascii.hexlify(procPrompt))
                logger.debug("Output we were searching through -> displayed in HEX = %s" % binascii.hexlify(output))
            logger.debug("##### end - DEBUGING ATTEMPT TO MATCH #######")

            logger.debug("##### begin checking output for error conditions and/or concurrentLogin")
            errorConditionFound, concurrentLoginFound, errorMsg = checkForErrorCondition(output, errorConditionList, concurrentLoginIndicator)
            
            finalOutput = output

            if errorConditionFound:
              return finalOutput, False, errorConditionFound, concurrentLoginFound, errorMsg

            if concurrentLoginFound:
              return finalOutput, False, errorConditionFound, concurrentLoginFound, errorMsg 

            logger.debug("##### end checking output for error conditions and/or concurrentLogin") 

            if indexOfMatch == -1:
                # We could not find requested text
                if promptContainsPassword:
                    msg = ("Unable to find match for a prompt that contains a password. This debug message is incomplete to prevent revealing the password.")
                else:
                    msg = ("Unable to find match for prompt = %s, This was the actual output %s" % (procPrompt, finalOutput))
                logger.debug(msg)
                print(msg)
                # Return False so calling code can bail out
                return finalOutput, False, errorConditionFound, concurrentLoginFound, errorMsg
            # Write command
            if commandContainsPassword:
                logger.debug("About to write command that contains a password so we will not log.")
            else:
                logger.debug("About to write command -> %s" % procCommand)
            telnet_connection.write(procCommand)
            logger.debug("\n*********************** END PROCESSING commandObj ******************************")
        return finalOutput, True, errorConditionFound, concurrentLoginFound, errorMsg


    def processString(self, theStr):
        # We don't want debuging to print out the password
        containsPassword = False
        logger.debug("In processString, processing %s" % theStr)
        # When XLR saves string values backslash characters are escaped
        # When the user wishes to use non printable control charater,such as carriage return followed by new line, 
        #   they enter \r\n in the list of strings. XLR then escapes the backslash, thereby changing the string from contol charaters to 
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


        

    
