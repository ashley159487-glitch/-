import json

def save_data(shop_obj, user_money) :
    data = {"shop_money" : shop_obj.money, "shop_itemlist" : shop_obj.itemlist, "user_money" : user_money}
    with open("shop_data.json", "w", encoding= "utf-8") as f :
        json.dump(data, f, indent = 4, ensure_ascii = False)
        
import os

class ordererror(Exception) :
    pass

class Shop :
    def __init__(self, money, itemlist) :
        self.money = money
        self.itemlist = itemlist
    
    def show_info(self) :
        i = 1
        for name, info in self.itemlist.items() :
            print("구매 가능 아이템 : %d.%s(%d개), %d골드" %(i, name, info[1], info[0]))
            i = i + 1
    
    def add_items(self, name, price, count) :
        if self.money < (price * count) :
            raise ordererror("상점 잔고가 부족합니다.")
        if name in self.itemlist :
            if self.itemlist[name][0] != price :
                raise ordererror("등록되어있는 상품과 가격이 다릅니다!")            
        self.money -= int((price * count) * 0.7)
        if name in self.itemlist :
            self.itemlist[name][1] += count
        else :
            self.itemlist[name] = [price, count]
        print("아이템이 상점에 등록 됐습니다.")
           
    def sell_items(self, name, count) :
        if name in self.itemlist :
            if self.itemlist[name][1] < count :
                raise ordererror("재고가 부족합니다!")
            self.money += self.itemlist[name][0] * count
            self.itemlist[name][1] -= count
            if self.itemlist[name][1] == 0 :                
                del self.itemlist[name]
                print("구매하셨습니다. 상품이 품절되었습니다.")
            else :
                print("구매하셨습니다.")
        else :
            print("존재하지 않는 상품입니다.")

title = "===진솔이네 잡화점===\n"
msg = "1. 아이템 목록\n2. 아이템 추가\n3. 나가기\n"

if os.path.exists("shop_data.json") :
    with open("shop_data.json", "r", encoding= "utf-8") as f :
        loaded_data = json.load(f)
        my_shop = Shop(loaded_data["shop_money"], loaded_data["shop_itemlist"])
        user_money = loaded_data["user_money"]
else :
    my_shop = Shop(50000, {})
    user_money = 50000
    
while True :
    try :
        choice = int(input(title + msg + "\n메뉴 선택 : "))
        if choice == 1 :
            name_list = list(my_shop.itemlist.keys())
            if not name_list :
                print("상점이 비었습니다.")
                continue
            print("%d골드" %user_money)
            my_shop.show_info()
            item_num = int(input("구매하실 아이템의 번호를 입력해주세요(나가기 : 0) : "))            
            if item_num == 0 :
                continue
            elif not (1 <= item_num <= len(name_list)) :
                raise ordererror("번호를 다시 입력해주세요!")
            while True :
                total_cnt = int(input("구매하실 아이템의 수량을 입력해주세요(나가기 : 0) : "))
                if total_cnt == 0 :
                    break
                elif total_cnt < 0 :
                    print("수량을 다시 입력해주세요.")
                    continue
                elif total_cnt > my_shop.itemlist[name_list[item_num-1]][1] :
                    print("재고가 부족합니다.")
                    continue
                else :
                    item_price = my_shop.itemlist[name_list[item_num-1]][0]
                    total_price = item_price * total_cnt
                    if user_money < total_price :
                        print("잔액이 부족합니다.")
                        print("현재 잔액은 %d골드 입니다." %user_money)
                        continue
                    else :
                        my_shop.sell_items(name_list[item_num - 1], total_cnt)
                        user_money -= total_price
                        print("현재 잔액은 %d골드 입니다." %user_money)
                        save_data(my_shop, user_money)
                        break
            
        elif choice == 2 :
            while True :
                print("신규 아이템을 등록해주세요.(나가기 : 0)")
                print("상점 잔고 : %d골드" %my_shop.money)
                new_item = input("신규 아이템 : ")
                if new_item == "0" :
                    break
                item_price = int(input("아이템 가격 : "))
                if item_price == 0 :
                    break
                elif item_price < 0 :
                    print("가격은 0보다 커야합니다.")
                    continue
                item_cnt = int(input("아이템 수량 : "))
                if item_cnt == 0 :
                    break
                elif item_cnt < 0 :
                    print("수량은 0보다 커야합니다.")
                    continue
                if my_shop.money < (item_price * item_cnt) :
                    print("상점 잔고가 부족합니다!")
                    continue
                if new_item in my_shop.itemlist :
                    if item_price != my_shop.itemlist[new_item][0] :
                        print("상점에 등록되어있는 아이템과 가격이 다릅니다!")
                        continue
                my_shop.add_items(new_item, item_price, item_cnt)
                save_data(my_shop, user_money)
                break

        elif choice == 3 :
            break
        
        else :
            print("다시 입력해주세요.")
        
    except Exception as e:
        print("\n!!오류 발생 : ", e)
