#!/usr/bin/env python

import argparse
import os

from loguru import logger

from config import settings
from core import Multi_pService

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="multi_p service")
    ap.add_argument(
        "-d",
        "--execute_dir",
        type=str,
        help="multi_p service execute directory",
        default=os.path.realpath(os.path.dirname(__file__)),
    )
    args = ap.parse_args()
    logger.info("Run multi_p service at {}", args.execute_dir)
    os.chdir(args.execute_dir)

    logger.remove()
    logger.info("Load logging config...")

    Multi_pService(settings, args.execute_dir).run()
