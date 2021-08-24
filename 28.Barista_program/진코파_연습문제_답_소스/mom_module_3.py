# p 191 답입니다.
'''

4. 영어로 함수 호출 형태 변경하기

mix(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl)
beat(egg, wide_bowl)
dip(thigh_meat, beaten_egg)
smear(thigh_meat, big_bowl)
boil(cooking_oil, deep_fryer)
fry(thigh_meat, deep_fryer)
put(lettuce, hamburger_bun_bottom)
spread(mayonnaise, hamburger_bun_bottom) 
put_2(thigh_meat, hamburger_bun_bottom)
put_3(onion, pickle, hamburger_bun_bottom)
cover(hamburger_bun_top, hamburger_bun_bottom)

파이썬에서는 같은 이름을 가진 함수를 정의하지 못합니다. 그래서 얹는다에 대응하는 함수를 put, put_2, put_3으로 정의하였습니다.

'''
menu = {
    "1" : "싸이 버거",
    "2" : "불고기 버거",
    "3" : "새우 버거"
}

def mix(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl):
    print("  %s, %s, %s, %s, %s, %s를 %s에 넣어 섞는다." 
        %(flour[0], starch[0], salt[0], pepper[0], 
        onion_powder[0], garlic_powder[0], big_bowl[0]))
    big_bowl[0] = "튀김 옷"
    print("  %s이 준비되었습니다!" %big_bowl[0])    
    return 
    
def beat(egg, wide_bowl):
    print("  %s을 %s에 넣어 푼다." %(egg[0], wide_bowl[0]))
    wide_bowl[0] = "계란 옷"
    print("  %s이 준비되었습니다!" %wide_bowl[0])
    return 

def dip(thigh_meat, wide_bowl):
    print("  %s을 %s에 넣어 담근다." %(thigh_meat[0], wide_bowl[0]))
    thigh_meat[0] = "계란 옷을 입힌 허벅지 살"
    print("  %s이 준비되었습니다!" %thigh_meat[0])
    return 

def smear(thigh_meat, big_bowl):
    print("  %s에 %s을 입힌다." %(thigh_meat[0], big_bowl[0]))
    thigh_meat[0] = "튀김 옷을 입힌 허벅지 살"
    print("  %s이 준비되었습니다!" %thigh_meat[0])
    return 

def boil(cooking_oil, deep_fryer):
    print("  %s을 %s에 데운다." %(cooking_oil[0], deep_fryer[0]))
    deep_fryer[0] = "데워진 식용유가 담긴 " + deep_fryer[0]
    print("  %s가 준비되었습니다!" %deep_fryer[0])
    return 
    
def fry(thigh_meat, deep_fryer):
    print("  %s을 %s에 데운다." %(thigh_meat[0], deep_fryer[0]))
    thigh_meat[0] = "튀긴 치킨"
    print("  %s이 준비되었습니다!" %thigh_meat[0])
    return   

def put(lettuce, hamburger_bun_bottom):
    print("  %s을 %s 위에 얹는다." %(lettuce[0], hamburger_bun_bottom[0]))
    hamburger_bun_bottom[0] = "상추가 얹혀진 햄버거 빵"
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom[0])
    return 

def spread(mayonnaise, hamburger_bun_bottom):
    print("  %s를 %s에 바른다." %(mayonnaise[0], hamburger_bun_bottom[0]))
    hamburger_bun_bottom[0] = "마요네즈가 발라진 햄버거 빵"
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom[0])
    return

def put_2(thigh_meat, hamburger_bun_bottom):
    print("  %s을 %s에 얹는다." %(thigh_meat[0], hamburger_bun_bottom[0]))
    hamburger_bun_bottom[0] = "치킨이 들어간 햄버거 빵"
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom[0])
    return

def put_3(onion, pickle, hamburger_bun_bottom):
    print("  %s, %s를 %s에 얹는다." %(onion[0], pickle[0], hamburger_bun_bottom[0]))
    hamburger_bun_bottom[0] = "양파, 피클이 들어간 햄버거 빵"
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom[0])
    return
    
def cover(hamburger_bun_top, hamburger_bun_bottom):
    print("  또 다른 %s으로 %s을 덮는다." %(hamburger_bun_top[0], hamburger_bun_bottom[0]))
    hamburger_bun_bottom[0] = "싸이버거"
    print("  %s가 준비되었습니다!" %hamburger_bun_bottom[0])
    return

def make_thighburger():
    print("싸이 버거를 만들고 있습니다~")
    
    flour = ["밀가루"]
    starch = ["전분"]
    salt = ["소금"]
    pepper = ["후추"]
    onion_powder = ["양파 가루"]
    garlic_powder = ["마늘 가루"]
    big_bowl = ["큰 그릇"]
    egg = ["계란"]
    wide_bowl = ["넓은 그릇"]
    thigh_meat = ["허벅지 살"]
    cooking_oil = ["식용유"]
    deep_fryer = ["튀김 냄비"]
    lettuce = ["상추"]
    hamburger_bun_bottom = ["햄버거 빵"]
    hamburger_bun_top = ["햄버거 빵"]
    mayonnaise = ["마요네즈"]
    onion = ["양파"]
    pickle = ["피클"]
    
    mix(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl)
    beat(egg, wide_bowl)
    dip(thigh_meat, wide_bowl)
    batter_thigh_meat = smear(thigh_meat, big_bowl)
    boil(cooking_oil, deep_fryer)
    fry(thigh_meat, deep_fryer)    
    put(lettuce, hamburger_bun_bottom)
    spread(mayonnaise, hamburger_bun_bottom) 
    put_2(thigh_meat, hamburger_bun_bottom)
    put_3(onion, pickle, hamburger_bun_bottom)
    cover(hamburger_bun_top, hamburger_bun_bottom)
    
    return
def make_bulgogiburger():
    print("불고기 버거를 만들고 있습니다~")
    return
def make_shrimpburger():
    print("새우 버거를 만들고 있습니다~")
    return
recipe = {
    "1": make_thighburger,
    "2": make_bulgogiburger,
    "3": make_shrimpburger
}
