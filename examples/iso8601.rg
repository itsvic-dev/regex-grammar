group iso8601 = date | time

group date = (year "-" month ["-" day]) | (year month day) ["T" time]

group year = digit{4}
group month = "0[1-9]" | "1[0-2]"
group day = "0[1-9]" | "[12][0-9]" | "3[0-1]"

group time = (hour [":" minute [":" second]]) | (hour [minute [second]]) [tz]

group hour = "[01][0-9]" | "2[0-3]"
group minute = "[0-5][0-9]"
group second = "[0-5][0-9]" ["\." ms]
group ms = digit{3}

group tz = "Z" | offset
def offset = mark hour [[":"] minute]
group mark = "[\+\-]"

def digit = "[0-9]"
