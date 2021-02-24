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

logger = logging.getLogger(__name__)


def debugPromptCommand(prompt, command, hasBeenProcessed, promptContainsPassword = False, commandContainsPassword = False):
        if hasBeenProcessed:
            logger.debug("\n*** Processed ascii encoded Prompt and Command")
        else:
            logger.debug("\n*** Unprocessed ascii encoded Prompt and Command")
        if promptContainsPassword:
            prompt = "********"
        if commandContainsPassword:
            command = "********"
        logger.debug("In debugPromptCommand - prompt = %s, command = %s" % (prompt,command))
        logger.debug("Converted to Hex - prompt = %s, command = %s" % (binascii.hexlify(prompt), binascii.hexlify(command)))

def checkForErrorCondition(theOutput, errorConditionList, concurrentLoginIndicator):
        logger.debug("In checkForErrorCondition")
        logger.debug("theOutput = %s, errorConditionList = %s, concurrentLoginIndicator = %s" % (theOutput, errorConditionList, concurrentLoginIndicator))
        errorFound = False
        concurrentLoginFound = False
        msg = "No Error Found"
        if concurrentLoginIndicator is not None and len(concurrentLoginIndicator.strip()) == 0:
            concurrentLoginIndicator = None
        if errorConditionList is not None:
            for condition in errorConditionList:
                if len(condition.strip()) > 0:
                    logger.debug("Testing for Condition %s in output %s" % (condition, theOutput))
                    if not errorFound and len(condition) > 0 and condition in theOutput:
                        # First error condition found
                        msg = ("Found error condition '%s' in telnet output string '%s'" % (condition, theOutput))
                        errorFound = True
                        break
        if not errorFound and concurrentLoginIndicator is not None:
            if concurrentLoginIndicator in theOutput:
                # concurrent login found
                msg = ("Found concurrent login indicator '%s' in telnet output string '%s'" % (concurrentLoginIndicator, theOutput))
                concurrentLoginFound = True
        logger.debug("Finished checkForErrorCondition, errorFound = %s, concurrentLoginFound = %s, msg = %s" % (errorFound, concurrentLoginFound, msg))
        return errorFound, concurrentLoginFound, msg

