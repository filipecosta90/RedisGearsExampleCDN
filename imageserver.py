from wand.image import Image

def convert_to_format( image_binary, fmt ):
    converted_bin = None
    with Image(blob=image_binary) as original:
        with original.convert(fmt) as converted:
            converted_bin = converted.make_blob()
    return converted_bin

def builder_format( key_pattern, fmt, origin_field, destination_field ):
    GearsBuilder()\
    .filter(lambda x: execute("type", x["key"]) == "hash" )\
    .filter(lambda x: origin_field in x["value"].keys() )\
    .filter(lambda x: destination_field not in x["value"].keys() )\
    .foreach(lambda x: execute("hset", x["key"], destination_field, convert_to_format(x["value"][origin_field],fmt ) ) )\
    .count()\
    .register(key_pattern)

def main():
    builder_format( "cdn:*", "PNG", "fetch_format_png", "fetch_format_jpg" )
    builder_format( "cdn:*", "JPG", "fetch_format_jpg", "fetch_format_png" )    

main()
