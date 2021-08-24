# p 181 답입니다.
import sys
import importlib
import os

if len(sys.argv) >=2:
    _module = importlib.import_module(sys.argv[1], package=None)
else:    
    print("사용법 : python %s _module" %os.path.basename(sys.argv[0]))
    sys.exit(-1)

menu = _module.menu
def show_menu():
    print("==<< 메뉴 >>==")
    for key in sorted(menu):
        print(key+".",menu[key])
    return
def get_order():
    order = input("무엇을 주문하시겠어요?(q.종료) ")
    if order =="q":
        print("오늘은 이만! 안녕~")
        sys.exit(0)
    print(order, "주문하셨습니다.")
    return order

recipe = _module.recipe
def process_order(order):
    func = recipe.get(order)
    if func != None:
        func()
    else:
        print("다시 주문해주세요~")
    return

while True:
    # 메뉴 보여주기
    show_menu()
    
    # 주문 받기
    order = get_order()
    
    # 주문 처리하기
    process_order(order)
