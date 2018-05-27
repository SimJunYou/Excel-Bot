from time import localtime, strftime

def getTimeGroup():
    return strftime("%d%H%MH %b %y", localtime())

def getTimePeriod():
    hour = int(strftime("%H", localtime()))
    if hour < 11:
        return "Morning"
    elif hour < 18:
        return "Afternoon"
    else:
        return "Evening"
print(getTimePeriod())
print(getTimeGroup())
