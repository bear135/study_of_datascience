# p 181 답입니다.
'''
단계 1 : 순서를 붙여 레시피 정리하기
싸이버거 조리순서
  다음 사이트를 참고했습니다.
  https://www.10000recipe.com/recipe/6860538
1. 밀가루, 전분, 소금, 후추, 양파 가루, 마늘 가루를 큰 그릇에 넣고 섞어 튀김옷을 만든다.
2. 계란을 넓은 그릇에 넣고 풀어 계란옷을 만든다.
3. 허벅지 살을 계란옷에 담근다.
4. 허벅지 살에 튀김옷을 입힌다.
5. 식용유를 튀김 냄비에 데운다.
6. 닭고기를 기름에 튀긴다.
7. 햄버거 빵 위에 상추를 얹는다.
8. 상추에 마요네즈를 바른다.
9. 치킨을 상추에 얹는다.
10. 치킨에 양파, 피클을 얹는다.
11. 빵을 덮는다.

단계 2 : 우리말로 동작, 대상 순서로 나열하기
섞는다. 밀가루, 전분, 소금, 후추, 양파 가루, 마늘 가루를, 큰 그릇에, 그러면 튀김옷이 나온다.
푼다. 계란을, 넓은 그릇에, 그러면 계란옷이 나온다.
담근다. 허벅지 살을, 계란옷에, 그러면 계란옷을 입힌 허벅지 살이 나온다.
입힌다. 허벅지 살에, 튀김옷을, 그러면 튀김옷을 입힌 허벅지 살이 나온다.
데운다. 식용유를, 튀김 냄비에, 그러면 데워진 식용유가 나온다.
튀긴다. 튀김옷을 입힌 허벅지 살을, 튀김 냄비에, 그러면 튀긴 싸이치킨이 나온다.
얹는다. 상추를, 햄버거 빵 위에, 그러면 상추가 얹혀진 햄버거 빵이 나온다.
바른다. 마요네즈를, 상추에, 그러면 마요네즈가 발라진 햄버거 빵이 나온다.
얹는다. 싸이 치킨을, 상추에, 그러면 싸이 치킨이 들어간 햄버거 빵이 나온다.
얹는다. 양파, 피클을, 싸이 치킨에, 그러면 양파, 피클이 들어간 햄버거 빵이 나온다.
덮는다. 빵을, 그러면 싸이버거가 나온다.

3. 우리말로 함수 호출 형태로 변경하기
섞는다(밀가루, 전분, 소금, 후추, 양파 가루, 마늘 가루, 큰 그릇) -> 튀김옷
푼다(계란, 넓은 그릇) -> 계란옷
담근다(허벅지 살, 계란옷) -> 계란옷을 입힌 허벅지 살
입힌다(계란옷을 입힌 허벅지 살, 튀김옷) -> 튀김옷을 입힌 허벅지 살
데운다(식용유, 튀김 냄비) -> 데워진 식용유
튀긴다(튀김옷을 입힌 허벅지 살, 튀김 냄비) -> 튀긴 싸이 치킨
얹는다(상추, 햄버거 빵) -> 상추가 얹혀진 햄버거 빵
바른다(마요네즈, 상추) -> 마요네즈가 발라진 햄버거 빵
얹는다(싸이 치킨, 상추) -> 싸이 치킨이 들어간 햄버거 빵
얹는다(양파, 피클, 치킨) -> 양파, 피클이 들어간 햄버거 빵
덮는다(빵) -> 싸이버거

4. 영어로 함수 호출 형태 변경하기

batter = mix(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl)
beaten_egg = beat(egg, wide_bowl)
beaten_egg_thigh_meat = dip(thigh_meat, beaten_egg)
batter_thigh_meat = smear(beaten_egg_thigh_meat, batter)
deep_fryer = boil(cooking_oil, deep_fryer)
fried_thigh_chicken = fry(batter_thigh_meat, deep_fryer)
hamburger_bun_with_lettuce = put(lettuce, hamburger_bun)
hamburger_bun_with_mayonnaise = spread(mayonnaise, hamburger_bun_with_lettuce) 
hamburger_bun_with_fried_thigh_chicken = put_2(fried_thigh_chicken, hamburger_bun_with_mayonnaise)
hamburger_bun_with_onion_pickle = put_3(onion, pickle, hamburger_bun_with_fried_thigh_chicken)
thigh_burger = cover(hamburger_bun, hamburger_bun_with_onion_pickle)

파이썬에서는 같은 이름을 가진 함수를 정의하지 못합니다. 그래서 얹는다에 대응하는 함수를 put, put_2, put_3으로 정의하였습니다.

'''
menu = {
    "1" : "싸이 버거",
    "2" : "불고기 버거",
    "3" : "새우 버거"
}

def mix(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl):
    print("  %s, %s, %s, %s, %s, %s를 %s에 넣어 섞는다." 
        %(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl))
    big_bowl = "튀김 옷"
    print("  %s이 준비되었습니다!" %big_bowl)    
    return big_bowl
    
def beat(egg, wide_bowl):
    print("  %s을 %s에 넣어 푼다." %(egg, wide_bowl))
    wide_bowl = "계란 옷"
    print("  %s이 준비되었습니다!" %wide_bowl)
    return wide_bowl

def dip(thigh_meat, beaten_egg):
    print("  %s을 %s에 넣어 담근다." %(thigh_meat, beaten_egg))
    thigh_meat = "계란 옷을 입힌 " + thigh_meat
    print("  %s이 준비되었습니다!" %thigh_meat)
    return thigh_meat

def smear(beaten_egg_thigh_meat, batter):
    print("  %s에 %s을 입힌다." %(beaten_egg_thigh_meat, batter))
    beaten_egg_thigh_meat = "튀김 옷을 입힌 허벅지 살"
    print("  %s이 준비되었습니다!" %beaten_egg_thigh_meat)
    return beaten_egg_thigh_meat

def boil(cooking_oil, deep_fryer):
    print("  %s을 %s에 데운다." %(cooking_oil, deep_fryer))
    deep_fryer = "데워진 식용유가 담긴 " + deep_fryer
    print("  %s가 준비되었습니다!" %deep_fryer)
    return deep_fryer
    
def fry(batter_thigh_meat, deep_fryer):
    print("  %s을 %s에 데운다." %(batter_thigh_meat, deep_fryer))
    batter_thigh_meat = "튀긴 치킨"
    print("  %s이 준비되었습니다!" %batter_thigh_meat)
    return batter_thigh_meat    

def put(lettuce, hamburger_bun):
    print("  %s을 %s 위에 얹는다." %(lettuce, hamburger_bun))
    hamburger_bun = "상추가 얹혀진 " + hamburger_bun
    print("  %s이 준비되었습니다!" %hamburger_bun)
    return hamburger_bun

def spread(mayonnaise, hamburger_bun_with_lettuce):
    print("  %s를 %s에 바른다." %(mayonnaise, hamburger_bun_with_lettuce))
    hamburger_bun_with_lettuce = "마요네즈가 발라진 햄버거 빵"
    print("  %s이 준비되었습니다!" %hamburger_bun_with_lettuce)
    return hamburger_bun_with_lettuce 

def put_2(fried_thigh_chicken, hamburger_bun_with_mayonnaise):
    print("  %s을 %s에 얹는다." %(fried_thigh_chicken, hamburger_bun_with_mayonnaise))
    hamburger_bun_with_mayonnaise = "치킨이 들어간 햄버거 빵"
    print("  %s이 준비되었습니다!" %hamburger_bun_with_mayonnaise)
    return hamburger_bun_with_mayonnaise

def put_3(onion, pickle, hamburger_bun_with_fried_thigh_chicken):
    print("  %s, %s를 %s에 얹는다." %(onion, pickle, hamburger_bun_with_fried_thigh_chicken))
    hamburger_bun_with_fried_thigh_chicken = "양파, 피클이 들어간 햄버거 빵"
    print("  %s이 준비되었습니다!" %hamburger_bun_with_fried_thigh_chicken)
    return hamburger_bun_with_fried_thigh_chicken

def cover(hamburger_bun, hamburger_bun_with_onion_pickle):
    print("  또 다른 %s으로 %s을 덮는다." %(hamburger_bun, hamburger_bun_with_onion_pickle))
    hamburger_bun_with_onion_pickle = "싸이버거"
    print("  %s가 준비되었습니다!" %hamburger_bun_with_onion_pickle)
    return hamburger_bun_with_onion_pickle

def make_thighburger():
    print("싸이 버거를 만들고 있습니다~")
    
    flour = "밀가루"
    starch = "전분"
    salt = "소금"
    pepper = "후추"
    onion_powder = "양파 가루"
    garlic_powder = "마늘 가루"
    big_bowl = "큰 그릇"
    egg = "계란"
    wide_bowl = "넓은 그릇"
    thigh_meat = "허벅지 살"
    cooking_oil = "식용유"
    deep_fryer = "튀김 냄비"
    lettuce = "상추"
    hamburger_bun = "햄버거 빵"
    mayonnaise = "마요네즈"
    onion = "양파"
    pickle = "피클"
    
    batter = mix(flour, starch, salt, pepper, onion_powder, garlic_powder, big_bowl)
    beaten_egg = beat(egg, wide_bowl)
    beaten_egg_thigh_meat = dip(thigh_meat, beaten_egg)
    batter_thigh_meat = smear(beaten_egg_thigh_meat, batter)
    deep_fryer = boil(cooking_oil, deep_fryer)
    fried_thigh_chicken = fry(batter_thigh_meat, deep_fryer)
    hamburger_bun_with_lettuce = put(lettuce, hamburger_bun)
    hamburger_bun_with_mayonnaise = spread(mayonnaise, hamburger_bun_with_lettuce) 
    hamburger_bun_with_fried_thigh_chicken = put_2(fried_thigh_chicken, hamburger_bun_with_mayonnaise)
    hamburger_bun_with_onion_pickle = put_3(onion, pickle, hamburger_bun_with_fried_thigh_chicken)
    thigh_burger = cover(hamburger_bun, hamburger_bun_with_onion_pickle)
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
