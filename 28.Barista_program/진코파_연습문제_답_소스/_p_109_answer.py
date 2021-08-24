while True:
    # 메뉴 보여주기
    print("==<< 메뉴 >>==")
    print("1. 싸이 버거")
    print("2. 불고기 버거")
    print("3. 새우 버거")
    
    # 주문 받기
    order = input("무엇을 주문하시겠어요?(q.종료) ")
    if order =="q":
        print("오늘은 이만! 안녕~")
        break
    print(order, "주문하셨습니다.")
    
    # 주문 처리하기
    if order =="1":
        print("싸이 버거를 만들고 있습니다~")
    elif order =="2":
        print("불고기 버거를 만들고 있습니다~")
    elif order =="3":
        print("새우 버거를 만들고 있습니다~")
    else:
        print("다시 주문해주세요~")
