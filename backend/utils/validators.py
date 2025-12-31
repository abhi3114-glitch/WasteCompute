DANGEROUS_KEYWORDS = ["rm", "shutdown", "reboot", "mkfs"]

def validate_command(command: str):
    for word in DANGEROUS_KEYWORDS:
        if word in command.lower():
            return False
    return True
