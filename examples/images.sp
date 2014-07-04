
// cookies - off
// javascript - off

get 'http://imgur.com/' as html

if & == None:
    return 'failed :('

skip &'//div[@id="imagelist"]'
        
image_urls = []
image_sources = &'//img@src'        
        
for src in image_sources:
    image_urls << ('http:' + src)

return image_urls