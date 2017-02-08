# -*- coding: utf-8 -*-
import random
import pickle
import datetime
short_program=[]
new_short_program=[]
my_list4 = open('//media//zhangkun//000FB948000CC321//exchange//AUDUSD//AUDUSDcelue201727.txt', 'rb')

short_program=pickle.load(my_list4)
my_list4.close()

# for each in short_program:
#     print(each)
# print(len(short_program))

short_program=sorted(short_program,key=lambda program:program[4],reverse=True)

for each in short_program:
    if each not in new_short_program:
        if each[4]>10000:
            new_short_program.append(each)

today = datetime.date.today()
new_address = '//media//zhangkun//000FB948000CC321//exchange//AUDUSD//AUDUSDcelue' + str(today.year) + str(
                today.month) + str(today.day) + '.txt'
#new_address = '//media//zhangkun//000FB948000CC321//exchange//AUDUSD//AUDUSDcelue1231_2.txt'
my_list4 = open(new_address, 'wb')
pickle.dump(new_short_program, my_list4)
my_list4.close()

for each in new_short_program:
    print(each)
print(len(new_short_program))





#import datetime   时间函数用法


# # Get a date object
# today = datetime.date.today()
#
# # General functions
# print("Year: %d" % today.year)
#
# print("Month: %d" % today.month)
# print("Day: %d" % today.day)
# print("Weekday: %d" % today.weekday() ) # Day of week Monday = 0, Sunday = 6
#
# # ISO Functions
# print("ISO Weekday: %d" % today.isoweekday() ) # Day of week Monday = 1, Sunday = 7
# print("ISO Format: %s" % today.isoformat())  # YYYY-MM-DD format
# print("ISO Calendar: %s" % str(today.isocalendar()))  # Tuple of (ISO year, ISO week number, ISO weekday)
#
# # Formatted date
# print(today.strftime("%Y/%m/%d") )



