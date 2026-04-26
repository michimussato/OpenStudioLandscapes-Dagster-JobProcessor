# Todo
#  - [ ] Disable as long as no certificates are involved
DEADLINE_ERRORS = [
    # Connecting to the correct repository?
    "'\nConfiguration Error: Failed to establish connection to michimussato-fuji.nord:4433 due to a communication error.\n'"
    # Changed repo but need to go and enter the passphrase again manually
    "'Error: Error encountered when loading the configured Client Certificate (/nfs/deadline/Deadline10/certs/certs/Deadline10RemoteClient.pfx). It is likely either an invalid x.509 certificate, or the wrong passphrase was provided.\n\nFull Error:\nThe certificate data cannot be read with the provided password, the password may be incorrect.\n'",
]
DEADLINE_SUCCESSES = [
    "'result: System.Collections.Generic.List`1[System.String]\n'",
]
