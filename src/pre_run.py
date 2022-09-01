import colorama


def pre_use():
    """
    This function is called everytime the program is run. All init code should be placed here.
    """
    colorama.init()


def pre_cli_only():
    """
    This function is called when the program is run directly, that meaning not imported as a module. Console cleaning and such should be placed here.
    """
    pass