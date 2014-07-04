
// cookies - on
// javascript - on

log      'sending request'
get      'http://api.openweathermap.org/data/2.5/weather?q=kiev,ua&units=metric' as json
log      'processing response'
skip    &'tag[1]'
city  = &'.@name'
desc  = &'weather[1]@description'
temp  = &'main[1]@temp'
pres  = &'main[1]@pressure'
humid = &'main[1]@humidity'
log      'returning results'
return   [city, desc, temp, pres, humid]