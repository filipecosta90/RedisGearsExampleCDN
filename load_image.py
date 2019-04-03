#!/usr/bin/env python3

"""
Image loader for our CDN RedisGears Example
For help type:
  load_image.py -h
"""

from __future__ import print_function
from wand.image import Image
import redis
import argparse
import logging


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="redis instance port", default=6379)
parser.add_argument(
    "--password", type=int, help="redis instance password", default=None
)
parser.add_argument("--host", type=str, help="redis instance host", default="127.0.0.1")
parser.add_argument("--image", type=str, help="image to be loaded", required=True)
parser.add_argument("--key", type=str, help="key to store the image to", required=True)

parser.add_argument(
    "--field",
    type=str,
    help="field in which to store the value loaded from image",
    required=True,
)
args = parser.parse_args()

# redis setup
redis_obj = redis.Redis(host=args.host, port=args.port, password=args.password)

log_level = logging.ERROR
logging.basicConfig(level=log_level)

with Image(filename=args.image) as img:
    jpeg_bin = img.make_blob()

    try:
        redis_obj.hset(args.key, args.field, jpeg_bin)
    except redis.RedisError as err:
        logging.error(err)
