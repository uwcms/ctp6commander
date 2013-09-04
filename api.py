"""Command/readout the CTP6 links.

Various python functions to issue/interpret IPBus commands over uHAL.

"""

import collections
import logging

log = logging.getLogger(__name__)

BANKS = [
    "Bank00to11",
    "Bank12to23",
    "Bank24to35",
    "Bank36to47",
]

STATUS_FLAGS = {
    'Overflow': {
        'prefix': 'GTRXUnderflow',
        'bad': True,
    },
    'Underflow': {
        'prefix': 'GTRXOverflow',
        'bad': True,
    },
    'LossSync': {
        'prefix': 'GTRXLossOfSync',
        'bad': True,
    },
    'PLLk OK': {
        'prefix': 'GTRXPLLKDet',
        'bad': False,
    },
    'ErrDetect': {
        'prefix': 'GTRXErrorDet',
        'bad': True,
    },
}


def expand_links(linklists):
    """Expand link-ranges in the form 'XX-YY,ZZ,QQ-RR'.

    Returns a generator which yields individual integer links.

    """
    for linklist in linklists:
        for link in linklist.split(','):
            if '-' not in link:
                yield int(link)
            else:
                low, high = tuple(link.split('-'))
                for i in range(int(low), int(high) + 1):
                    yield i


def build_masked_set(bank_index, links):
    """ Find the correct per-bank bit mask for a given bank + link set.

    Returns an integer with the bit mask.

    """
    output = 0
    for link in links:
        bank_for_link = link / 12
        if bank_index != bank_for_link:
            continue
        offset = link % 12
        output |= (1 << offset)
    return output


def reset(hw, links, power_down=False):
    """ Reset the desired MGTs.

    Returns 1 if successful

    """
    if power_down:
        log.info("Powering down links")
        pwr_nodes = [hw.getNode("GTPowerDown" + bank) for bank in BANKS]
        for ibank, node in enumerate(pwr_nodes):
            mask = build_masked_set(ibank, links)
            log.debug("Masked value: %x", mask)
            node.write(mask)
        hw.dispatch()
        for node in pwr_nodes:
            node.write(0x0)
        hw.dispatch()

    log.info("Resetting links")
    rst_nodes = [hw.getNode("GTReset" + bank) for bank in BANKS]
    for ibank, node in enumerate(rst_nodes):
        mask = build_masked_set(ibank, links)
        node.write(mask)
    hw.dispatch()
    for node in rst_nodes:
        node.write(0x0)
    hw.dispatch()
    return 1


def capture(hw, links, ncapture, capture_char, expected_word_fn=None):
    """ Execute a orbit capture command for the given links.

    Returns a dictionary containing the captured and expected data.
    If expected_word_fn is not None, it is assumed to a function which takes
    a link index and returns a list given the expected data

    """
    log.info("Setting orbit trigger character to 0x%x",
             int(capture_char, 16))
    orbit_char_reg = hw.getNode("OrbitCharReq")
    trigger = hw.getNode("CaptureTrigger")

    orbit_char_reg.write(int(capture_char, 16))
    trigger.write(0)
    hw.dispatch()

    log.info("Triggering capture")
    trigger.write(1)
    hw.dispatch()

    rams = [hw.getNode('MGT%i' % link) for link in links]

    output = {}

    for link, ram in zip(links, rams):
        result = ram.readBlock(ncapture)
        hw.dispatch()
        output[link] = {}
        output[link]['expected'] = []
        if expected_word_fn:
            output[link]['expected'] = expected_word_fn(link)[:ncapture]
        output[link]['capture'] = [word for word in result]

    trigger.write(0)
    hw.dispatch()
    return output


def status(hw, links):
    """ Query the status of the given links.

    Returns a dictionary mapping each link to a STATUS_FLAG state dictionary.

    """
    output = collections.defaultdict({})
    for flag, flag_cfg in output.iteritems():
        flag_cfg['banks'] = [flag_cfg['prefix'] + bank for bank in BANKS]
        flag_cfg['nodes'] = [hw.getNode(bank) for bank in flag_cfg['banks']]
        flag_cfg['values'] = [node.read() for node in flag_cfg['nodes']]
        # eventually do the whole dispatch all at once
        hw.dispatch()
        output[flag]['links'] = {}
        for link in links:
            value = bool(flag_cfg['values'][link / 12].value()
                         & (1 << (link % 12)))
            output[link][flag] = (value != flag_cfg['bad'])
    return output
