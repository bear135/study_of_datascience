import sys

def show_menu():
    print("==<< 메뉴 >>==")
    print("1. 싸이 버거")
    print("2. 불고기 버거")
    print("3. 새우 버거")
    return
def get_order():
    order = input("무엇을 주문하시겠어요?(q.종료) ")
    if order =="q":
        print("오늘은 이만! 안녕~")
        sys.exit(0)
    print(order, "주문하셨습니다.")
    return order
def make_thighburger():
    print("싸이 버거를 만들고 있습니다~")
    return
def make_bulgogiburger():
    print("불고기 버거를 만들고 있습니다~")
    return
def make_shrimpburger():
    print("새우 버거를 만들고 있습니다~")
    return
def process_order(order):
    if order =="1":
        make_thighburger()
    elif order =="2":
        make_bulgogiburger()
    elif order =="3":
        make_shrimpburger()
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
