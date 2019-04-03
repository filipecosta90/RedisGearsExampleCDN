#!/bin/bash -x

redis-cli flushall
redis-cli module load /Users/filipeoliveira/redis-porto/RedisGears/redisgears.so

# Register for new cdn events
redis-cli -x rg.pyexecute < imageserver.py

# Load sample images into cdn:* keys 
python load_image.py --key=cdn:10th-anniv --field=fetch_format_jpg --image=./data/10th-anniv.jpg

# Check the image conversions are working
redis-cli hexists cdn:10th-anniv fetch_format_jpg
redis-cli hexists cdn:10th-anniv fetch_format_png
