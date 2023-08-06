def check(text):
    import re
    if re.match('^[a-zA-Z0-9_]*$', text):
        print("valid")
    else:
        print("invalid")