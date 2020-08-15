#########################################################################################################
# Filters the message history for the target user
#
# Parameters
# messages: List of Message (Discord API)
# user: User (Discord API)
# msgLimit: integer
#
# Returns: None or List of Message (Discord API)

def filterMessageHistory(messages, user, msgLimit):
    filteredMessages = [msg for msg in messages if msg.author == user]
    filteredMessages = filteredMessages[0:msgLimit]

    return filteredMessages