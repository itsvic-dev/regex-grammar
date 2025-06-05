group iso8601 = date | time

group date = (year "-" month ["-" day]) | (year month day) ["T" time]

group year = digit{4}
group month = digit{2}
group day = digit{2}

group time = (hour [":" minute [":" second]]) | (hour [minute [second]]) [tz]

group hour = digit{2}
group minute = digit{2}
group second = digit{2} ["\." ms]
group ms = digit{3}

group tz = "Z" | offset
def offset = mark hour [[":"] minute]
group mark = "[\+\-]"

def digit = "[0-9]"
