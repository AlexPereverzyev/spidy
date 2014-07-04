
// cookies - off
// javascript - off

site   = 'http://www.booking.com'
seed   = '/searchresults.html?src=index&nflt=&ss_raw=New&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-us.html%3Fsid%3D71e6b75d82741bb0e5e557dd1752c426%3Bdcid%3D1%3B&dcid=1&sid=71e6b75d82741bb0e5e557dd1752c426&si=ai%2Cco%2Cci%2Cre%2Cdi&ss=New+York%2C+New+York+State%2C+U.S.A.&checkin_monthday=0&checkin_year_month=0&checkout_monthday=0&checkout_year_month=0&interval_of_time=any&flex_checkin_year_month=any&group_adults=2&group_children=0&no_rooms=1&dest_type=city&dest_id=20088325&ac_pageview_id=17796dfd541700bf&ac_position=0&ac_langcode=en&ac_suggestion_list_length=5'
agent  = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0'
markup = '<html xmlns="http://www.w3.org/1999/xhtml"><head/><body><div><h4>' + site + '</h4>\n'

// parse pagination to obtain page URLs to scrap
get (site + seed) as html:
    User-Agent: agent
    
pages = None
if & != None:
    pages = &'//div[@class="results-paging"]/ul[1]//a@href'
else:
    markup = markup + '<p>failed to load page URLs</p>'
    
// iterate over page URLs
count = 0
while pages:    
    count = count + 1    
    if count > 2:
        // only want first two pages
        break
    
    pages[0] >> q    
    get (site + q) as html:
        User-Agent: agent

    if & != None:    
        markup = markup + '<h4>Page ' + $count +'</h4>'

        // now collect the actual data
        traverse div in &'//div[@id="hotellist_inner"]':
            path    = '/div[2]/h3/a[1]'            
            ref     = &(div + path + '@href')
            title   = &(div + path)            
            likes   = &(div + '/div[2]/h3/span/a[1]')
            
            // skip items w/o reference
            if ref == '':
                continue
            
            anchor = ('\t<a href="' + site + ref + '">' + title + ' - ' + likes + ' likes</a><br/>\n')
            markup = markup + anchor        
    else:
        markup = (markup + '\t<p>failed to load page ' + $count + ': ' + site + q + '</p>\n')
    
markup = (markup + '</div></body></html>')
return markup