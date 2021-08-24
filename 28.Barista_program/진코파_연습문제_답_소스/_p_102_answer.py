while True:
    # 메뉴 보여주기
    print("==<< 메뉴 >>==")
    print("1. 아메리카노")
    print("2. 카페라떼")
    print("3. 에스프레소")
    print("4. 녹차")
    print("5. 망고쥬스")
    
    # 주문 받기
    order = input("무엇을 주문하시겠어요?(q.종료) ")
    if order =="q":
        print("오늘은 이만! 안녕~")
        break
    print(order, "주문하셨습니다.")
    
    # 주문 처리하기
    if order =="1":
        print("아메리카노를 만들고 있습니다~")
    elif order =="2":
        print("카페라떼를 만들고 있습니다~")
    elif order =="3":
        print("에스프레소를 만들고 있습니다~")
    elif order =="4":
        print("녹차를 만들고 있습니다~")
    elif order =="5":
        print("망고쥬스를 만들고 있습니다~")
    else:
        print("다시 주문해주세요~")
