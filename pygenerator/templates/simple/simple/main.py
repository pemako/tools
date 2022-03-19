#!/usr/bin/env python

import argparse
import logging
import logging.config
import os

from config import settings
from core import SimpleService

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="simple service")
    ap.add_argument(
        "-d",
        "--execute_dir",
        type=str,
        help="simple service execute directory",
        default=os.path.realpath(os.path.dirname(__file__)),
    )
    args = ap.parse_args()
    print("Run simple service at {}".format(args.execute_dir))
    os.chdir(args.execute_dir)

    print("Load logging config...")
    logging.config.dictConfig(settings.logs)

    SimpleService(settings.service, args.execute_dir).run()
