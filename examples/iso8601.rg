group iso8601 = fullDate | time

def fullDate = date ["T" time]
group date = date1 | date2 | dateNoDay
def date1 = year "-" month "-" day
def date2 = year month day
def dateNoDay = year "-" month

group year = digit{4}
group month = digit{2}
group day = digit{2}

group time = timeSeparated | timeNonSeparated
def timeSeparated = hour [":" minute [":" second ["\." millisecond]]] [timezone]
def timeNonSeparated = hour [minute [second ["\." millisecond]]] [timezone]

group hour = digit{2}
group minute = digit{2}
group second = digit{2}
group millisecond = digit{3}

group timezone = "Z" | timeOffset
def timeOffset = posOffset | negOffset
def posOffset = "\+" offset
def negOffset = "-" offset
def offset = digit{2} [[":"] digit{2}]

def digit = "[0-9]"
