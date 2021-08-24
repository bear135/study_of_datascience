# 단계 7 - 함수 구현

def pour(cup, ingredient):
    print("pour", ingredient, "into", cup) 
    return

def stir(cup):
    print("stir", cup)
    return

def put(cup, whipping_cream):
    print("put", whipping_cream, "on", cup)
    return

def spread(whipping_cream, cocoa_powder):
    print("spread", cocoa_powder, "on", whipping_cream)
    return

cup = "cup"
chocolate_sauce = "chocolate sauce"
espresso = "espresso"
warm_milk = "warm milk"
whipping_cream = "whipping cream"
cocoa_powder = "cocoa_powder"

pour(cup, chocolate_sauce)
pour(cup, espresso)
stir(cup)
pour(cup, warm_milk)
stir(cup)
put(cup, whipping_cream)
spread(whipping_cream, cocoa_powder)
