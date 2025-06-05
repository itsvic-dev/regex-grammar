group iso8601 = date | time

group date = dateC ["T" time]
def dateC = date1 | date2 | dateNoDay
def date1 = year "-" month "-" day
def date2 = year month day
def dateNoDay = year "-" month

group year = digit{4}
group month = digit{2}
group day = digit{2}

group time = time1 | time2
def time1 = hour [":" minute [":" second ["\." ms]]] [tz]
def time2 = hour [minute [second ["\." ms]]] [tz]

group hour = digit{2}
group minute = digit{2}
group second = digit{2}
group ms = digit{3}

group tz = "Z" | offset
def offset = posNeg hour [[":"] minute]
def posNeg = "[\+\-]"

def digit = "[0-9]"
