#!/usr/bin/env python3

"""
Image saver from our CDN RedisGears Example
For help type:
  save_image.py -h
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
parser.add_argument(
    "--image", type=str, help="name of the image to be saved", required=True
)
parser.add_argument(
    "--key", type=str, help="key to retrieve the image from", required=True
)

parser.add_argument(
    "--field",
    type=str,
    help="field from in which to load the image blob",
    required=True,
)
args = parser.parse_args()

# redis setup
redis_obj = redis.Redis(host=args.host, port=args.port, password=args.password)

log_level = logging.ERROR
logging.basicConfig(level=log_level)

try:
    image_binary = redis_obj.hget(args.key, args.field)
    with Image(blob=image_binary) as image:
        image.save(filename=args.image)
except redis.RedisError as err:
    logging.error(err)
