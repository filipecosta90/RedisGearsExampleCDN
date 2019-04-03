#!/bin/bash -x

redis-cli flushall
redis-cli module load /Users/filipeoliveira/redis-porto/RedisGears/redisgears.so

# Register for new cdn events
redis-cli -x rg.pyexecute < imageserver.py

# Load sample images into cdn:* keys 
python load_image.py --key=cdn:collage-redisconf19 --field=fetch_format_jpg --image=./data/collage-redisconf19.jpg
python load_image.py --key=cdn:redisconf19-location-header --field=fetch_format_jpg --image=./data/redisconf19-location-header.jpg

read -p "Give it a second and Press [ENTER]"

# Check the image conversions are working
redis-cli hexists cdn:collage-redisconf19 fetch_format_jpg
redis-cli hexists cdn:collage-redisconf19 fetch_format_png
redis-cli hexists cdn:collage-redisconf19 fetch_format_jpg,q_90
redis-cli hexists cdn:collage-redisconf19 fetch_format_jpg,q_80
redis-cli hexists cdn:collage-redisconf19 fetch_format_jpg,q_70
redis-cli hexists cdn:collage-redisconf19 fetch_format_jpg,q_60
redis-cli hexists cdn:collage-redisconf19 fetch_format_png,q_90
redis-cli hexists cdn:collage-redisconf19 fetch_format_png,q_80
redis-cli hexists cdn:collage-redisconf19 fetch_format_png,q_70
redis-cli hexists cdn:collage-redisconf19 fetch_format_png,q_60

redis-cli hexists cdn:redisconf19-location-header fetch_format_jpg
redis-cli hexists cdn:redisconf19-location-header fetch_format_png
redis-cli hexists cdn:redisconf19-location-header fetch_format_jpg,q_90
redis-cli hexists cdn:redisconf19-location-header fetch_format_jpg,q_80
redis-cli hexists cdn:redisconf19-location-header fetch_format_jpg,q_70
redis-cli hexists cdn:redisconf19-location-header fetch_format_jpg,q_60
redis-cli hexists cdn:redisconf19-location-header fetch_format_png,q_90
redis-cli hexists cdn:redisconf19-location-header fetch_format_png,q_80
redis-cli hexists cdn:redisconf19-location-header fetch_format_png,q_70
redis-cli hexists cdn:redisconf19-location-header fetch_format_png,q_60

python save_image.py --key=cdn:collage-redisconf19 --field=fetch_format_jpg,q_60 --image=./data/collage-redisconf19_q_60.jpg
python save_image.py --key=cdn:collage-redisconf19 --field=fetch_format_jpg --image=./data/collage-redisconf19_q_100.jpg
