def is_command_allowed(command: str) -> bool:
    command = command.strip().lower()

    # Allow simple python execution
    if command == "python":
        return True

    # Allow python inline execution
    if command.startswith("python"):
        return True

    blocked = ["rm", "shutdown", "reboot", "mkfs", "sudo"]
    for b in blocked:
        if b in command:
            return False

    return True
