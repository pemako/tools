#!/usr/bin/env python

import argparse
import os

from loguru import logger

from config import settings
from core import Multi_p_tService

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="multi_p_t service")
    ap.add_argument(
        "-d",
        "--execute_dir",
        type=str,
        help="multi_p_t service execute directory",
        default=os.path.realpath(os.path.dirname(__file__)),
    )
    args = ap.parse_args()
    logger.info("Run multi_p_t service at {}", args.execute_dir)
    os.chdir(args.execute_dir)

    logger.remove()
    logger.info("Load logging config...")

    Multi_p_tService(settings, args.execute_dir).run()
