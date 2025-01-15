

def flow(x):
    if x < 100:
        if x <= 50:
            return 0
        else: #x>50
            return 75
    #else - can skip the else line bc the if would catch all occurances 
    x -= 50
    while not (x < 200):
        x -= 50
    
    return x


print(flow(50))
print(flow(357.504))