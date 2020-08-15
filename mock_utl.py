import re

#########################################################################################################
# Mock function to mock incoming message
#
# Parameters
# message: string
#
# Returns: string

def MoCk(message):
    mock = ""
    cap = True

    for char in message:
        if char == ' ':
            mock += ' '
        else:
            if cap:
                mock += char.upper()
            else:
                mock += char.lower()
            
            cap = not cap
    
    return mock

#########################################################################################################
# Parses and returns the number of messages to mock
#
# Parameters
# message: string
#
# Returns: integer

async def getNumOfMsgs(message):
    numberOfMessages = -1

    try:
        parsedMessage = message.split('>')
        parsedMessage = parsedMessage[len(parsedMessage) - 1]
        numberOfMessages = re.search(r'\d+', parsedMessage)
        
        if numberOfMessages is None:
            numberOfMessages = -1
        else:
            numberOfMessages = int(re.search(r'\d+', parsedMessage).group())
    except Exception as ex:
        print('-----------------------------------------------------------------------------')
        print('Exception caught in getNumOfMsgs')
        print(str(ex))
        print('-----------------------------------------------------------------------------\n')
    
    return numberOfMessages