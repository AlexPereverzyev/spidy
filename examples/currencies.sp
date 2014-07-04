
// cookies - off
// javascript - off

agent   = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0'
reuters = ['http://www.reuters.com/finance/global-market-data', 'Reuters', '//table[@id="currPairs"]/tbody[1]', '//a[1]', '/td[2]']
yahoo   = ['http://finance.yahoo.com/currency-investing', 'Yahoo Finance', '//table[@id="flat-rates-table"]/tbody[1]', '//a[@class="currency-link"][1]', '/td[2]']
sources = [reuters, yahoo]
markup  = ''

for src in sources:
    get src[0] as html:
        User-Agent: agent
        
    if & != None:
        header = src[1]
        pairs  = ''
        prices = ''
        traverse tr in &src[2]:
            pair  = &(tr + src[3])
            price = &(tr + src[4])
            merge 'currencies_pair.spt'  as pair
            merge 'currencies_price.spt' as price
            pairs  = pairs  + pair
            prices = prices + price            
        merge 'currencies_rows.spt' as row    
        markup = markup + row
        
merge 'currencies_page.spt' as markup
return markup