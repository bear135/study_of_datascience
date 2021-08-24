# p 209 답입니다.
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

class Flour:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class Starch:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class Salt:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class Pepper:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class OnionPowder:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class GarlicPowder:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class BigBowl:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
    def setState(self, state):
        self.state = state
class Egg:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class WideBowl:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
    def setState(self, state):
        self.state = state
class ThighMeat:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
    def setState(self, state):
        self.state = state
class CookingOil:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class DeepFryer:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
    def setState(self, state):
        self.state = state
class Lettuce:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class HamburgerBunBottom:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
    def setState(self, state):
        self.state = state
class HamburgerBunTop:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class Mayonnaise:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class Onion:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state
class Pickle:
    def __init__(self, state):
        self.state = state
    def getState(self):
        return self.state

def mix(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl):
    print("  %s, %s, %s, %s, %s, %s를 %s에 넣어 섞는다." 
        %(flour.getState(), starch.getState(), salt.getState(), pepper.getState(), 
        onion_powder.getState(), garlic_powder.getState(), big_bowl.getState()))
    big_bowl.setState("튀김 옷")
    print("  %s이 준비되었습니다!" %big_bowl.getState())    
    return 
    
def beat(egg, wide_bowl):
    print("  %s을 %s에 넣어 푼다." %(egg.getState(), wide_bowl.getState()))
    wide_bowl.setState("계란 옷")
    print("  %s이 준비되었습니다!" %wide_bowl.getState())
    return 

def dip(thigh_meat, wide_bowl):
    print("  %s을 %s에 넣어 담근다." %(thigh_meat.getState(), wide_bowl.getState()))
    thigh_meat.setState("계란 옷을 입힌 허벅지 살")
    print("  %s이 준비되었습니다!" %thigh_meat.getState())
    return 

def smear(thigh_meat, big_bowl):
    print("  %s에 %s을 입힌다." %(thigh_meat.getState(), big_bowl.getState()))
    thigh_meat.setState("튀김 옷을 입힌 허벅지 살")
    print("  %s이 준비되었습니다!" %thigh_meat.getState())
    return 

def boil(cooking_oil, deep_fryer):
    print("  %s을 %s에 데운다." %(cooking_oil.getState(), deep_fryer.getState()))
    deep_fryer.setState("데워진 식용유가 담긴 " + deep_fryer.getState())
    print("  %s가 준비되었습니다!" %deep_fryer.getState())
    return 
    
def fry(thigh_meat, deep_fryer):
    print("  %s을 %s에 데운다." %(thigh_meat.getState(), deep_fryer.getState()))
    thigh_meat.setState("튀긴 치킨")
    print("  %s이 준비되었습니다!" %thigh_meat.getState())
    return   

def put(lettuce, hamburger_bun_bottom):
    print("  %s을 %s 위에 얹는다." %(lettuce.getState(), hamburger_bun_bottom.getState()))
    hamburger_bun_bottom.setState("상추가 얹혀진 햄버거 빵")
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom.getState())
    return 

def spread(mayonnaise, hamburger_bun_bottom):
    print("  %s를 %s에 바른다." %(mayonnaise.getState(), hamburger_bun_bottom.getState()))
    hamburger_bun_bottom.setState("마요네즈가 발라진 햄버거 빵")
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom.getState())
    return

def put_2(thigh_meat, hamburger_bun_bottom):
    print("  %s을 %s에 얹는다." %(thigh_meat.getState(), hamburger_bun_bottom.getState()))
    hamburger_bun_bottom.setState("치킨이 들어간 햄버거 빵")
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom.getState())
    return

def put_3(onion, pickle, hamburger_bun_bottom):
    print("  %s, %s를 %s에 얹는다." %(onion.getState(), pickle.getState(), hamburger_bun_bottom.getState()))
    hamburger_bun_bottom.setState("양파, 피클이 들어간 햄버거 빵")
    print("  %s이 준비되었습니다!" %hamburger_bun_bottom.getState())
    return
    
def cover(hamburger_bun_top, hamburger_bun_bottom):
    print("  또 다른 %s으로 %s을 덮는다." %(hamburger_bun_top.getState(), hamburger_bun_bottom.getState()))
    hamburger_bun_bottom.setState("싸이버거")
    print("  %s가 준비되었습니다!" %hamburger_bun_bottom.getState())
    return

def make_thighburger():
    print("싸이 버거를 만들고 있습니다~")
    
    flour = Flour("밀가루")
    starch = Starch("전분")
    salt = Salt("소금")
    pepper = Pepper("후추")
    onion_powder = OnionPowder("양파 가루")
    garlic_powder = GarlicPowder("마늘 가루")
    big_bowl = BigBowl("큰 그릇")
    egg = Egg("계란")
    wide_bowl = WideBowl("넓은 그릇")
    thigh_meat = ThighMeat("허벅지 살")
    cooking_oil = CookingOil("식용유")
    deep_fryer = DeepFryer("튀김 냄비")
    lettuce = Lettuce("상추")
    hamburger_bun_bottom = HamburgerBunBottom("햄버거 빵")
    hamburger_bun_top = HamburgerBunTop("햄버거 빵")
    mayonnaise = Mayonnaise("마요네즈")
    onion = Onion("양파")
    pickle = Pickle("피클")
    
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
