#!/usr/bin/env python

"""
Image Server for our CDN RedisGears Example
"""

from wand.image import Image

def convert_to_format( image_binary, fmt ):
    converted_bin = None
    with Image(blob=image_binary) as original:
        with original.convert(fmt) as converted:
            converted_bin = converted.make_blob()
    return converted_bin

def compress_quality_to_percent( image_binary, percent ):
    compressed_bin = None
    with Image(blob=image_binary) as original:
        with original.clone() as image:
            image.compression_quality = percent
            compressed_bin = image.make_blob()
    return compressed_bin

def builder_format( key_pattern, fmt, origin_field, destination_field ):
    GearsBuilder()\
    .filter(lambda x: execute("type", x["key"]) == "hash" )\
    .filter(lambda x: origin_field in x["value"].keys() )\
    .filter(lambda x: destination_field not in x["value"].keys() )\
    .foreach(lambda x: execute("hset", x["key"], destination_field, convert_to_format(x["value"][origin_field],fmt ) ) )\
    .count()\
    .register(key_pattern)

def builder_compress( key_pattern, percent, origin_field, destination_field ):
    GearsBuilder()\
    .filter(lambda x: execute("type", x["key"]) == "hash" )\
    .filter(lambda x: origin_field in x["value"].keys() )\
    .filter(lambda x: destination_field not in x["value"].keys() )\
    .foreach(lambda x: execute("hset", x["key"], destination_field, compress_quality_to_percent(x["value"][origin_field],percent ) ) )\
    .count()\
    .register(key_pattern)

def main():
    builder_format( "cdn:*", "PNG", "fetch_format_jpg", "fetch_format_png" )
    builder_format( "cdn:*", "JPG", "fetch_format_png", "fetch_format_jpg" )
    builder_compress( "cdn:*", 90, "fetch_format_jpg", "fetch_format_jpg,q_90" )
    builder_compress( "cdn:*", 80, "fetch_format_jpg", "fetch_format_jpg,q_80" )
    builder_compress( "cdn:*", 70, "fetch_format_jpg", "fetch_format_jpg,q_70" )
    builder_compress( "cdn:*", 60, "fetch_format_jpg", "fetch_format_jpg,q_60" )
    builder_compress( "cdn:*", 90, "fetch_format_png", "fetch_format_png,q_90" )
    builder_compress( "cdn:*", 80, "fetch_format_png", "fetch_format_png,q_80" )
    builder_compress( "cdn:*", 70, "fetch_format_png", "fetch_format_png,q_70" )
    builder_compress( "cdn:*", 60, "fetch_format_png", "fetch_format_png,q_60" )

main()
