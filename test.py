strd = 'morning/29.10_morning/31.10_morning/2.11_morning/3.11_morning/4.11_morning/5.11_morning/6.11_morning/7.11_morning/8.11_morning/9.11_morning/10.11_morning/11.11_morning/12.11_morning/13.11_morning/14.11_morning/15.11_morning/16.11_morning/17.11_morning/18.11_morning/19.11_morning/20.11_morning/21.11_morning/22.11_morning/23.11_morning/24.11_morning/25.11'
array = strd.split('_')

print(len(array))
setarray = set(array)
print(len(setarray))
print('_'.join(setarray))
