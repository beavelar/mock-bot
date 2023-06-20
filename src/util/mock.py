def mock(message: str) -> str:
    """
    Mocks the provided message by capitalizing every other letter
    """
    result = ""
    capitalize = True
    for character in message:
        new_character = character
        if character != " ":
            if capitalize:
                new_character = character.upper()
            else:
                new_character = character.lower()
            capitalize = not capitalize
        result += new_character
    return result
