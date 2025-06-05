group langtag = language ["-" script] ["-" region]
group language = alpha{2,3}
group script = alpha{4}
group region = alpha{2} | digit{3}

def alpha = "[a-zA-Z]"
def digit = "[0-9]"
