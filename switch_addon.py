def switch(n):
    global switch_variable
    switch_variable = n
    return True


def case(*ca):
    global switch_variable
    if switch_variable in ca:
        return True
    else:
        return False


"""
while(switch()):
    if case():
        <code>
        break
    if case():
        <code>
        break
    <code>
    break
"""
