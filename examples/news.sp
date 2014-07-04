
// cookies - off
// javascript - off

markup = '<html xmlns="http://www.w3.org/1999/xhtml"><head/><body><div>\n'
   
get 'http://news.google.com/news?pz=1&cf=all&ned=en_us&hl=en&q&js=0' as html:
    User-Agent:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0'
    
if & != None:
    traverse div in &'html/body/div[3]/div/div/div/div[3]/div/div/table/tbody/tr/td/div/div/div/div[2]':                
        
        if &(div + '@class') == 'esc-separator':
            continue
        
        anchor_path  = div + '/div/div/div/div[2]/table/tbody/tr/td[2]/div/h2/a[1]'
        anchor_ref   = &(anchor_path+'@href')        
        anchor_title = &(anchor_path+'/span[1]')        
        anchor       = ('\t<a href="' + anchor_ref + '">' + anchor_title + '</a><br/>\n')
        
        markup = markup + anchor
else:
    markup = (markup + '\t<p>failed :(</p>\n')
    
markup = (markup + '</div></body></html>')
return markup