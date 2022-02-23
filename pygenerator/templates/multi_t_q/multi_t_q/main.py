#!/usr/bin/env python3

import argparse
import logging
import logging.config
import os

from config import settings
from core import Multi_t_qService

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="multi_t service")
    ap.add_argument(
        "-d",
        "--execute_dir",
        type=str,
        help="multi_t service execute directory",
        default=os.path.realpath(os.path.dirname(__file__)),
    )
    args = ap.parse_args()
    print("Run multi_t service at {}".format(args.execute_dir))
    os.chdir(args.execute_dir)

    print("Load logging config...")
    logging.config.dictConfig(settings.logs)

    Multi_t_qService(settings.service, args.execute_dir).run()
