if __name__ == '__main__':
  import sys, os, codecs, math, time, datetime, calendar
  reload(sys)
  sys.setdefaultencoding('utf-8')
  import requests
  import lxml.html as LH	
  
  
  min_year = 2016
  curr_year = int(time.strftime("%Y")) 
  days_shift = 0;
  
  temp_arr = []
  cnt = 0;
  arg_month = -1 if len(sys.argv) <= 1 else int(sys.argv[1])

  year = curr_year
  
  if len(sys.argv) > 2:
    if sys.argv[2].startswith('-') or sys.argv[2].startswith('+'):
      days_shift = int(sys.argv[2])
    elif len(sys.argv) <= 3:
      year = int(sys.argv[3])

  if year < min_year:
    print 'Cannot parse year less then {}'.format(min_year)
    sys.exit(1)
  if year > curr_year:
    print 'Cannot parse year past {}'.format(curr_year)
    sys.exit(1)
  
  if arg_month > 0 and arg_month < 13:
    month = arg_month
  else:
    month = int(time.strftime("%m")) - 1
    if month == 0:
      month = 12
      year = year - 1
    print 'No valid month number in argumets. Taking previous month {} as default.'.format(month)
  monthdays = calendar.monthrange(year, month)[1]
  date = '{}/01/{}'.format(month, year)
  url = 'http://www.accuweather.com/en/ua/lviv/324561/month/324561?monyr={}'.format(date)
  print "Requesting Weather dada from URL:{}".format(url)
  print 'For month {}'.format(datetime.datetime.strptime(date,"%m/%d/%Y").strftime("%b"))
  r = requests.get(url)
  root = LH.fromstring(r.content)
  day_count = 0
  for table in root.xpath("//*[@id='panel-main']//table[contains(@class, 'calendar-block')]/tbody"):
    for row in table.xpath('.//tr'):
      for cell in row.xpath('td'):
        day_count += 1
        try:
          site_month = int(cell.xpath(".//h3[contains(@class, 'date')]/text()")[0].split('/')[0][4:])
          if site_month != month or (days_shift < 0 and day_count >= monthdays + days_shift) or (days_shift > 0 and day_count <= days_shift):
            continue
        except:
          print sys.exc_info()[0]
          continue
        temp_hi = cell.xpath(".//span[contains(@class, 'large-temp')]/text()")[0][:-1]
        temp_lo = cell.xpath(".//span[contains(@class, 'small-temp')]/text()")[0].replace('/','')[:-1]
        temp_val = (int(temp_hi) + int(temp_lo)) / 2
        temp_arr.append(temp_val)
  if days_shift > 0:
    print 'Skipped {} days from the begining of month'.format(days_shift)
  if days_shift < 0:
    print 'Skipped {} days from the end of month'.format(abs(days_shift))
  print temp_arr
  print 'The average temperature for {} days is: {}'.format(len(temp_arr), round(reduce(lambda x, y: float(x + y), temp_arr) / float(len(temp_arr)), 1))
  