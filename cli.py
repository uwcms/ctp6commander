#!/usr/bin/env python

""" Command line interface to the CTP6. """

import argparse
import logging
import os
import sys

from termcolor import colored

import uhal
import api

log = logging.getLogger(__name__)


def do_reset(hw, args):
    """ Reset the desired links.

    Returns 1 on success

    """
    return api.reset(hw, args.links, args.power_down)


def print_status_header(links):#output, links):
    """ Print out the status header row for the desired links.

    Two horizontal lines, with the link label for each link between the lines.

    """
    def write_hdiv():
        sys.stdout.write('----------')#output('----------')
        for underline in range(len(links)):
            sys.stdout.write('---')#output('---')
        sys.stdout.write('\n')#output('\n')
    write_hdiv()
    sys.stdout.write('Flag      ')#output('Flag      ')
    for link in links:
        sys.stdout.write('%3i' % link)#output('%3i' % link)
    sys.stdout.write('\n')#output('\n')
    write_hdiv()


def do_status(hw, args):#, output):
    """ Print out the status registers from all of the links.  """
    status_flags = api.status(hw, args.links)
    print_status_header(args.links)#output, args.links)

    # get labels of flags
    flags = [x[0] for x in status_flags.values()[0]]

    # Loop over each flag
    for iflag, flag in enumerate(flags):
        sys.stdout.write("%-11s" % flag)
        for link in args.links:
            if status_flags[link][iflag][1]:
                sys.stdout.write(colored(' * ', 'green'))#output(colored(' * ', 'green'))
            else:
                sys.stdout.write(colored(' E ', 'red'))#output(colored(' E ', 'red'))
        sys.stdout.write('\n')


def do_capture(hw, args):
    """ Capture an orbit of data and summarize the result. """
    sys.stdout.write('     word: ')
    sys.stdout.write(' '.join('%8i' % word for word in range(args.ncapture)))
    sys.stdout.write('\n')

    expected_word_fn = None
    if args.expected:
        log.info("Loading expected pattern from %s", args.expected)
        mod = __import__(args.expected.replace('.py', ''))
        expected_word_fn = getattr(mod, 'pattern')

    capture = api.capture(hw, args.links, args.ncapture,
                          args.capture_char, expected_word_fn)

    for link in sorted(capture.keys()):
        capture_data = capture[link]
        sys.stdout.write('link %5i ' % link)
        result_strs = []
        expected_data = capture_data['expected']
        for idx, word in enumerate(capture_data['capture']):
            color_fn = lambda x: x
            if expected_data:
                expected = expected_data[idx % len(expected_data)]
                if word == expected:
                    color_fn = lambda x: colored(x, 'green')
                else:
                    color_fn = lambda x: colored(x, 'red')
            result_strs.append(color_fn('%8x' % word))

        sys.stdout.write(' '.join(result_strs))
        sys.stdout.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("command", choices=['reset', 'status', 'capture'],
                        help="Action to perform")

    parser.add_argument("links", nargs='*', help="Specify links. "
                        "If none are specified, reset all.")

    parser.add_argument("--connection",
                        help="Manually connection XML file. "
                        "If not specified, take from CTP6_CONNECTION env.")
    parser.add_argument("--verbose", action='store_true',
                        help="Increase verbosity")

    parser_rst = parser.add_argument_group('reset')
    parser_stat = parser.add_argument_group('status')
    parser_cap = parser.add_argument_group('capture')

    # Reset arguments
    parser_rst.add_argument("--power-down", action='store_true',
                            dest='power_down',
                            help="Additionally power down the links")

    # Capture arguments
    parser_cap.add_argument("--orbit-capture-char", dest='capture_char',
                            type=str, metavar='0xbc', default='0xbc',
                            help="character to trigger capture "
                            "- default: %(default)s")

    parser_cap.add_argument("--nwords", dest='ncapture',
                            type=int, metavar='N', default=4,
                            help="Number of words to capture from each link"
                            "- default: 0x%(default)i")

    parser_cap.add_argument("--expected", metavar='pattern.txt',
                            help="Pattern file with 1 word/line in hex")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        uhal.setLogLevelTo(uhal.LogLevel.WARNING)
    else:
        uhal.setLogLevelTo(uhal.LogLevel.WARNING)
        logging.basicConfig(level=logging.WARNING)

    if not args.connection:
        args.connection = os.environ['CTP6_CONNECTION']

    if not args.links:
        log.debug("Using all links")
        args.links = range(48)
    else:
        args.links = list(api.expand_links(args.links))

    hw_connection = 'file://%s' % args.connection
    log.info("Setting up connection: %s", hw_connection)
    manager = uhal.ConnectionManager(hw_connection)

    hw = manager.getDevice('ctp6.frontend')

    commands = {
        'reset': do_reset,
        'status': do_status,
        'capture': do_capture
    }

    commands[args.command](hw, args)

    log.info("done.")
