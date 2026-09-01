# LEGB - 렉비
# L - Local
# E - enclosing
# G - Global
# B - Built in -> len, print, int, list

# list = "a"
# tmp = (10, 20, 30)
# l = list(tmp)


x = "Chad"

def outer_function():
    x = "염씨"

    def inner_function():
        x = "inner"        

    inner_function()
    

outer_function()



name = "chad"

def check_name() : 
    global name
    name = "염씨"

check_name()
print(name)



def upgrage() : 
    item = "낡은 검"

    def check_s():
        nonlocal item
        item = "고급 검"

    check_s()
    print(item)


upgrage()