#!/usr/bin/env python
""" An HTTP API for querying the status and capture RAMs of the CTP6.

The UI dynamism is all defined in the javascript/HTML.  This app only serves
JSON data resulting from querying the H/W via IPBus.

Author: Evan K. Friis, UW Madison

"""
import argparse
import logging
import os

from flask import Flask, render_template, url_for

import api
#import uhal

app = Flask(__name__)
log = logging.getLogger(__name__)
HWINTERFACE = None


@app.route('/')
def index():
    """ Landing page. """
    return render_template("interface.html")


@app.route('/reset/<linkstring>')
def reset(linkstring=None):
    """ Reset a given set of transcievers.

    If no links are specified (/reset/), all links are reset.

    """
    return ', '.join(str(x) for x in api.expand_links([linkstring]))


@app.route('/status/<linkstring>')
def status(linkstring=None):
    """ Query the status of the links.  """
    return linkstring


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection",
                        help="Manually connection XML file. "
                        "If not specified, take from CTP6_CONNECTION env.")
    parser.add_argument("--verbose", action='store_true',
                        help="Increase verbosity")
    parser.add_argument("--port", default=8081, help="Port to serve")
    parser.add_argument("--visible", action="store_true",
                        help="Serve outside of localhost")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        #uhal.setLogLevelTo(uhal.LogLevel.WARNING)
    else:
        #uhal.setLogLevelTo(uhal.LogLevel.WARNING)
        logging.basicConfig(level=logging.WARNING)

    if not args.connection:
        args.connection = os.environ['CTP6_CONNECTION']

    # Build the uHAL interface
    # hw_connection = 'file://%s' % args.connection
    # log.info("Setting up connection: %s", hw_connection)
    # manager = uhal.ConnectionManager(hw_connection)
    # HWINTERFACE = manager.getDevice('ctp6.frontend')

    # Serve forever
    host = '127.0.0.1' if not args.visible else '0.0.0.0'
    app.run(port=args.port, host=host)
