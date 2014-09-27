
import spidy
print spidy.do('''
               get 'https://github.com/explore' as html
               return &'//*[@class="repo-name css-truncate css-truncate-target"]'
               ''')
#print spidy.run('examples/images.sp')
#print spidy.run('examples/weather.sp')
#spidy.run('examples/currencies.sp', "examples/currencies.html")
#spidy.run('examples/news.sp', "examples/news.html")
#spidy.run('examples/bookings.sp', "examples/bookings.html")