from datetime import date
from datetime import datetime
from datetime import timedelta

buildentries = {
    "08.02.2016": 12,
    "05.02.2016": 18,
    "09.02.2016": 17
}

lowest_time = sorted(buildentries.keys())[0]
print("lowest_time:", lowest_time)

history = datetime.strptime(lowest_time, "%d.%m.%Y").date()
print("history:", history)

today = date.today()

delta = timedelta(days=1)

dayvalues = {}
current_entry = history
while current_entry < today:
    current_as_string = date.strftime(current_entry, "%d.%m.%Y")
    print("current:", current_as_string)
    if current_as_string in buildentries:
        dayvalues[current_as_string] = buildentries[current_as_string]
    else:
        dayvalues[current_as_string] = 0

    current_entry += delta


line_counter = 1
for t in sorted(dayvalues):
    print("t:", t)
    print("n:", dayvalues[t])
    line_counter += 1
