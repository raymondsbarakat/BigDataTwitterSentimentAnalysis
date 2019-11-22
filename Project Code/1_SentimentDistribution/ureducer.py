
#!/usr/bin/env /hadoop/bin/python3
# Above is a hashbang to make Hadoop use the virtualenv I crafted.
import sys

# Below code goes through each line of stdin and does the reduction by adding sums.

previous = None
sum = 0

for line in sys.stdin:
    splitted = line.strip().split(' ')
    key = ' '.join(splitted[0:len(splitted) - 1])
    value = splitted[len(splitted) - 1]
    if key != previous:
        if previous is not None:
            print(str(sum) + ' ' + previous)
        previous = key
        sum = 0
    sum += int(value)
print(str(sum) + ' ' + previous)