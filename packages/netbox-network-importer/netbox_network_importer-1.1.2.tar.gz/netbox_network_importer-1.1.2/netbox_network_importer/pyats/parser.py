import genie


def show_interfaces(pyats, hostname):
    """Get `show interfaces` command parsed by Genie.

    :param pyats: passed pyats connection instance with loaded testbed
    """
    dev = pyats.connect_device(hostname=hostname)
    show_ifcs = dev.parse("show interfaces")

    return show_ifcs


def show_vlan(pyats, hostname):
    try:
        dev = pyats.connect_device(hostname=hostname)
        return dev.parse("show vlan")
    except genie.metaparser.util.exceptions.InvalidCommandError:
        return {}
    except genie.metaparser.util.exceptions.SchemaEmptyParserError:
        return {}


def show_interfaces_status(pyats, hostname):
    try:
        dev = pyats.connect_device(hostname=hostname)
        return dev.parse("show interfaces status")
    except genie.metaparser.util.exceptions.InvalidCommandError:
        return {}
    except genie.metaparser.util.exceptions.SchemaEmptyParserError:
        return {}


def show_interfaces_trunk(pyats, hostname):
    try:
        dev = pyats.connect_device(hostname=hostname)
        return dev.parse("show interfaces trunk")
    except genie.metaparser.util.exceptions.InvalidCommandError:
        return {}
    except genie.metaparser.util.exceptions.SchemaEmptyParserError:
        return {}


def learn_interfaces(pyats, hostname):
    """PyATS Learn Device Features `learn interface` command parsed by pyATS.

    :param pyats: passed pyats connection instance with loaded testbed
    """

    dev = pyats.connect_device(hostname=hostname)

    learn_ifcs = dev.learn("interface")
    return learn_ifcs.info
