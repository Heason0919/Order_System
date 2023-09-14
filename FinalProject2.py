import cv2
import msvcrt
import requests


#菜單
主餐品項 = [['Torpedo',[['Pork',80],['Chicken',85],['Beef', 95],['Salmon', 110]]],
            ["Burrito",[['Chicken', 90],['Beef', 100]]],
            ['Sandwich',[['Chicken', 75],['Beef', 85],['Snapper', 85]]]]
飲料品項 = [['Pepsi', 20],['Cola', 25]]
Menu = [["meal",主餐品項],["drink",飲料品項]]

#賣家帳號密碼
sellers = (("A1075544","please","Manager"),("A1075504","let","Manager"),("B1075130","me","Clerk"),("A1077179","pass","Clerk"))

#訂單編號
order_num = 0

#賣家權限
Seller_Permissions = ''

#買家操作頁面
#選擇餐點
def meal_choose():

    #將餐點用list儲存
    order_list=[]

    #紀錄meal與drink的數量
    numMeal = 0
    numDrink = 0
    flag = 0

    while True:
        #選擇主餐or飲料
        print("What would you like for today? (",end="")
        for kind in range(0,len(Menu)):
            print(kind,"=",Menu[kind][0],end="")
            if kind != len(Menu)-1:
                print(", ",end="")
            if kind == len(Menu)-1:
                print(")")            
        Combo_Number = int(input(": "))

        #選擇主餐
        meal_list = Menu[Combo_Number][1]
        print("What meal do you want? (",end="")
        for meal in range(0,len(meal_list)):
            print(meal,"=",meal_list[meal][0],end="")
            if meal != len(meal_list)-1:
                print(", ",end="")
            if meal == len(meal_list)-1:
                print(")")               
        meal_Number = int(input(": "))
        if  Menu[Combo_Number][0] == 'meal':
            #選擇口味
            flavor_list = meal_list[meal_Number][1]
            print('What flavor would you prefer? (',end="")
            for flavor in range(0,len(flavor_list)):
                print(flavor,"=",flavor_list[flavor][0],end="")
                if flavor != len(flavor_list)-1:
                    print(", ",end="")
                if flavor == len(flavor_list)-1:
                    print(")")
            Flavor_Number = int(input(": "))
        
        #選擇餐點數量
        print("How many you want?")
        num = input(": ")

        # 紀錄訂單 紀錄meal & drink 的數量(為了套餐優惠)
        if Menu[Combo_Number][0] == "meal":
            # 類別 品項名稱 口味 價錢 數量
            order_list.append((Menu[Combo_Number][0],meal_list[meal_Number][0],flavor_list[Flavor_Number][0],flavor_list[Flavor_Number][1],int(num)))
            numMeal+=int(num)
        elif Menu[Combo_Number][0] == "drink":
            # 類別 品項名稱 價錢 數量
            order_list.append((Menu[Combo_Number][0],meal_list[meal_Number][0],meal_list[meal_Number][1],int(num)))
            numDrink+=int(num)

        print("Do you want to continue your order? (Y = Yes, N = No, I = Inspect)")
        con = input(": ").upper()

        #列印購物車裡面的商品
        if con == "I":
            sum_i = 0
            for item_i in order_list:
                if item_i[0] == 'meal':
                    print('>>>', item_i[2], item_i[1], '( $', item_i[3], ')', '*', item_i[4])
                    sum_i += item_i[3] * item_i[4]
                else:
                    print('>>>', item_i[1], '( $', item_i[2], ')', '*', item_i[3])
                    sum_i += item_i[2] * item_i[3]
            print('[', 'Total Cost :', '$', sum_i, ']\n')
            
            print("Do you want to continue your order? (Y = Yes, N = No)")
            con = input(": ").upper()
        
        #結束點餐
        if con == "N":
            # 如果有單點的商品會詢問是否要加點成套餐
            if flag == 1:
                return order_list,numMeal,numDrink
            while flag == 0:
                if numMeal > numDrink:
                    print("There is a combo discount of 10 dollars for the meal and drink. Would you like to add some drinks? (Y = yes, N = No)")
                    add_or_not = input(": ").upper()
                    if add_or_not == "Y":
                        flag = 1
                    elif add_or_not == "N":
                        return order_list,numMeal,numDrink
                    else:
                        print("Error.Please enter again.")
                elif numMeal < numDrink:
                    print("There is a combo discount of 10 dollars for the meal and drink. Would you like to add some meals? (Y = yes, N = No)")
                    add_or_not = input(": ").upper()
                    if add_or_not == "Y":
                        flag = 1
                    elif add_or_not == "N":
                        return order_list,numMeal,numDrink
                    else:
                        print("Error.Please enter again.")
                else:
                    # return  訂單資料、餐點和飲料數量(tuple輸出)
                    return order_list,numMeal,numDrink
        else:
            if con == "Y":
                continue
            
            #不合法輸入
            else:
                while con == "Y":
                    print("illegal input")
                    print("Do you want to end your order? (Y = yes, N = No)")
                    con = input(": ").upper()
                    if con == "N":
                        # return order and 餐點和飲料數量(tuple輸出)
                        return order_list,numMeal,numDrink
 
#印出訂單明細
def details_print(details):
    
    #桌號
    print("\nTable number")
    table_num = int(input(": "))
    
    #計算訂單編號
    order_sum = 0
    
    #讀取OrderList_Progress.txt的檔案
    with open('OrderList_Progress.txt','r') as file_object:
        for line in file_object:
            order_sum+=1
            
    #讀取OrderList_Completed.txt的檔案
    with open('OrderList_Completed.txt','r') as file_object:
        for line in file_object:
            order_sum+=1
            
    #讀取OrderList_Cancelled.txt的檔案
    with open('OrderList_Cancelled.txt','r') as file_object:
        for line in file_object:
            order_sum+=1
    
    global order_num
    order_num = order_sum + 1

    #將訂單資料以dict儲存
    order_1 = {
       'OrderId : ' : order_num,
       'Table : ' : table_num,
       'Content : ' : details[0], #order_list
       'numMeal':details[1],
       'numDrink':details[2],
       'status':'進行中'
    }
    
    #寫入進行中的訂單文檔
    with open('OrderList_Progress.txt','a') as file_object:
        orderlist = str(order_num) + " , " + str(table_num) + " , " + str(details[0]) + " , 進行中\n"
        file_object.write(str(orderlist))
        
    print('\nHere are your order details : ')
    print ('[' + 'NO.%s'%(order_1['OrderId : ']) + ']')

    sum = 0

    #印出內容+計算總額
    for item in order_1['Content : ']:
        if item[0] == 'meal':
            sum += item[3]*item[4]
            print(item[1],"-",item[2]," ",str(item[3]),"*",str(item[4]))
        if item[0] == 'drink':
            sum += item[2]*item[3]
            print(item[1]," ",str(item[2]),"*",str(item[3]))

    # 計算有多少折扣
    plus = 0
    maxNum = 0
    
    if order_1['numMeal']>order_1['numDrink']:
        maxNum = order_1['numDrink']
    else :
        maxNum = order_1['numMeal']
    if maxNum != 0:
        plus = 10*maxNum
        print("主餐+飲料折扣10元 可折扣" + str(plus) + "元")

    sum -= plus

    return sum

#確認會員資格
def vip_check(sum):

    print("Do you have a membership? (Y = yes , N = no)")
    VIP = input(": ").upper()
    
    #具有會員資格
    if VIP == 'Y':
        sum = 0.9*sum

    #不具有會員資格
    else:
        print('\nOnly cost $15, you will get a 10 percent discount on all delicacies.')
        print('Would you like to join our membership? (Y = yes , N = no) : ')
        VIP_join = input(": ").upper()
        if VIP_join == 'Y':
            sum = 0.9*sum + 15
        else:
            sum = sum

    print('Here is your bill. It\'s ' + '$' + str(sum) + ' in all.')
    return sum

#選擇付款方式
def pay_choose(sum):
    coco_choose = -1
    while coco_choose == -1:
        print("which dollors you like to pay")
        coco_choose = input("Enter 0 for 'Pay with TWD', 1 for 'Pay with USD', 2 for 'Pay with JPY'.\n")
        if coco_choose == '0':
            print("Total is NT$"+str(sum))
        elif coco_choose == '1':
            print("Total is US$"+change(sum,'USD'))
        elif coco_choose == '2':
            print("Total is JPY"+change(sum,'JPY'))
        else:
            coco_choose = '-1'
    pay_type = 0
    while pay_type == 0:
        print('\nHow would you like to pay?')
        pay_type = input("Enter 1 for 'Pay in cash',2 for 'Pay by credit card',3 for 'Pay by digital payment'.\n")
        if pay_type == '1':
            print('\nPlease insert your money.\n')
        elif pay_type == '2':
            print('\nPlease scan your card.\n')
        elif pay_type == '3':
            print('\nPlease scan your QR code or barcode.\n')
        else:
            print('\nPlease enter again.')
            pay_type = 0
    print('Thank you very much.\n')

#登入賣家
def login():
    print("Who are you? (C = Costumer,O = Owner)")
    x = input(": ").upper()
    if x == "O":
        account = ""
        password = ""
        account = input("account : ")
        password = input("password : ")
        # 偵測是否有該使用者
        user_flag = False
        for user in sellers:
            if user[0] == account and user_flag == False:
                if user[1] == password:
                    global Seller_Permissions
                    Seller_Permissions = user[2]
                    if Seller_Permissions == "Manager":
                        seller()
                        return True
                    elif Seller_Permissions == "Clerk":
                        inspect_orderlist()
                        return True
                else:
                    print("Wrong password.")
                    return False
        print("Wrong account.")
        return False
    elif x == "C":
        #叫出示意圖
        img = cv2.imread('menu.jpg') 
        cv2.namedWindow('MENU',1)
        cv2.resizeWindow('MENU', 300, 300)
        cv2.imshow('MENU',img)
        print('Open Our Menu & Close TO Coutinue')
        cv2.waitKey()
        cv2.destroyAllWindows()

        #選擇餐點
        details = meal_choose()

        #印出訂單明細
        sum = details_print(details)

        #確認餐點是否正確
        print('\nIs the meal correct? (y = yes , n = no)')
        meal_check = input(": ").lower()

        #內容錯誤，重新選擇餐點
        while(meal_check == 'n'):
            print('\nPlease choose a meal once again.\n')
            details = meal_choose()
            details_print(details)
            print('\nIs the meal correct? (y = yes , n = no)')
            meal_check = input(": ").lower()

        #確認會員資格，並選擇付款方式
        sum = vip_check(sum)
        pay_choose(sum)
        return True
    return False
 
#刪除菜單內容
def delete_item():
        
    y = ""
    y = input("Product：")

    #先找到品項
    #主餐區
    getIt = False
    for meal in Menu[0][1]:
        if meal[0] == y:
            print("Which flavor do you want to delete? ")
            f = input(": ")
            for flavor in meal[1]:
                if flavor[0] == f:
                    meal[1].remove(flavor) #list刪除
            getIt = True
    if getIt == False:
        for drink in Menu[1][1]:
            if drink[0] == y:
                Menu[1][1].remove(drink) #list刪除
                getIt = True
    if getIt == False:
        print("Not found")

#新增菜單內容
def add_item():
    x,y,z,w = "","","",0
    print("(M = meal,D = drink)")
    x = input(": ").upper()
    if x == "M":

        print("Which meal do you want to add?")
        y = input(": ")

        # 是否有這個品項
        getIt = False
        for m in 主餐品項:
            if m[0]==y:
                print("Which flavor do you want to add? ")
                z = input(": ")

                #原本有沒有
                haveIt=False
                for f in m[1]:
                    if f[0] == z:
                        print("Already have.")
                        haveIt = True
                if haveIt == False:
                    w = int(input("How much is it? "))
                    m[1].append([z,w])
                getIt = True

        #沒有這個選項的話就新增
        if getIt == False:
            print("Which flavor do you want to add?")
            z = input(": ")
            print("How much is it?")
            w = int(input(": "))
            主餐品項.append([y,[[z,w]]])
            
                    
    elif x == "D":
        print("Which drink do you want to add?")
        y = input(": ")
        # 是否有這個品項
        getIt = False
        for d in 飲料品項:
            if d[0]==y:
                print("Already have.")
                getIt = True
        #沒有這個選項的話就新增
        if getIt==False:
            print("How much is it?")
            w = int(input(": "))
            飲料品項.append([y,w])

#更改菜單內容
def change_item():
    x,y,z,w = "","","",0
    print("(M = meal,D = drink)")
    x = input(": ").upper()
    if x == "M":
        y = input("Product：")
        getIt = False
        for m in 主餐品項:
            if m[0] == y:
                print("Which flavor do you want to change?")
                z = input(": ")
                haveIt = False
                for f in m[1]:
                    if f[0] == z:
                        print("How much is it?")
                        w = int(input(": "))
                        f[1] = w
                        haveIt = True
                if haveIt == False:
                    print("Don't have this flavor.")
                getIt = True
        if getIt == False:
            print("Don't have this meal.")
    elif x == "D":
        y = input("Product：")
        getIt = False
        for m in 飲料品項:
            if m[0] == y:
                print("How much is it?")
                w = int(input(": "))
                m[1] = w
                getIt = True
        if getIt == False:
            print("Don't have this drink.")
    else:
        print("Not found")

#瀏覽訂單紀錄
def inspect_orderlist():
    print('\nListType：1 = Progress,2 = Completed,3 = Cancelled')
    orderlist_type = input("： ")
    
    #進行中的訂單
    if orderlist_type == '1':
        #讀取OrderList_Progress.txt的檔案
        with open('OrderList_Progress.txt','r+') as file_object:
            orderlist = []
            for line in file_object:
                orderlist.append(line.split(' , '))
            
            #有進行中的訂單
            if(len(orderlist)>0):
                #印出所有進行中的訂單明細
                print('\n==========================')
                for order in range(len(orderlist)):
                    
                    #對訂單的content字串處理
                    content_Meallist = []
                    content_Drinklist = []
                    content_str = ''
                    store_flag = 0
                    for content in orderlist[order][2]:
                        if(content.isalnum()):
                            content_str = content_str + content
                        else:
                            if(len(content_str)>0):
                                if(content_str == 'meal'):
                                    store_flag = 0
                                    content_str = ''
                                elif(content_str == 'drink'):
                                    store_flag = 1
                                    content_str = ''
                                elif(store_flag == 0):
                                    store_flag = 0
                                    content_Meallist.append(content_str)
                                    content_str = ''
                                elif(store_flag == 1):
                                    store_flag = 1
                                    content_Drinklist.append(content_str)
                                    content_str = ''
                    
                    print('OrderID：' + str(orderlist[order][0]))
                    print('TableNum：' + str(orderlist[order][1]))
                    print('Content：')
                    
                    meal_str = ''
                    count = 0
                    for i in range(len(content_Meallist)):
                        meal_str = meal_str + content_Meallist[i]
                        count+=1
                        if(count %4 != 0):
                            meal_str = meal_str + ' - '
                        if(count%4 == 0 and count != 0):
                            print(meal_str)
                            meal_str = ''
                    
                    drink_str = ''
                    count = 0
                    for i in range(len(content_Drinklist)):
                        drink_str = drink_str + content_Drinklist[i]
                        count+=1
                        if(count %3 != 0):
                            drink_str = drink_str + ' - '
                        if(count%3 == 0 and count != 0):
                            print(drink_str)
                            drink_str = ''
                            
                    print('Status：' + orderlist[order][3].strip())
                    print('==========================')
            else:
                print('\n==========================')
                print('No order in progress.')
                print('==========================')
        
        #對訂單的操作選擇
        operator = ''
        
        #儲存已完成的訂單
        list_complete = []
        
        #儲存被取消的訂單
        list_cancel = []
        
        while(operator!="3"):
            print('\n(OrderList：1 = Modify,2 = Delete,3 = Leave)')
            operator = input("： ")
            
            #修改訂單
            if(operator == '1'):
                print('\nEnter Order_ID')
                orderID = input('： ')
                print('\n(1 = TableNum,2 = Status)')
                modify_choice = input('： ')
                
                #修改桌號
                if(modify_choice == '1'):
                    
                    #是否找到欲修改的訂單
                    succ = False
                    
                    print('New TableNum')
                    newTableNum = input('： ')
                    
                    #搜尋該訂單是否存在
                    for order in orderlist:
                        if(orderID==order[0]):
                            order[1] = newTableNum
                            succ = True
                    if(succ == True):
                        print('\n>>> Successfully Modified')
                    elif(succ == False):
                        print('\n>>> fail to edit')
                            
                #修改狀態
                elif(modify_choice == '2'):
                    
                    #是否找到欲修改的訂單
                    succ = False
                    
                    print('\nWhether the order has been completed? (Y = Yes, N = No)')
                    status_choice = input('： ').upper()
                    
                    #搜尋該訂單是否存在並設定訂單狀態
                    for order in orderlist:
                        if(orderID==order[0]):
                            status = ''
                            if(status_choice == 'Y'):
                                status = '已完成\n'
                                list_complete.append(order)
                            elif(status_choice == 'N'):
                                status = '進行中\n'
                            order[3] = status
                            succ = True
                    if(succ == True):
                        print('\n>>> Successfully Modified')
                    elif(succ == False):
                        print('\n>>> fail to edit')
            
            #刪除訂單
            if(operator == "2"):
                print('\nEnter Order_ID')
                orderID = input('： ')
                
                #是否找到欲修改的訂單
                succ = False
                
                #搜尋該訂單是否存在並設定訂單狀態
                for order in orderlist:
                    if(orderID==order[0]):
                        order[3] = '已取消\n'
                        list_cancel.append(order)
                        orderlist.remove(order)
                        succ = True
                if(succ == True):
                    print('\n>>> Successfully Modified')
                elif(succ == False):
                    print('\n>>> fail to edit')
                    
            #存入txt檔案
            if(operator == '3'):
                with open('OrderList_Progress.txt','w') as file_object: 
                    for order in orderlist:
                        if(order[3]=='進行中\n'):
                            order_str = str(order[0]) + " , " + str(order[1]) + " , " + str(order[2]) + " , " + order[3]
                            file_object.write(str(order_str))
                if(len(list_complete)>0):
                    with open('OrderList_Completed.txt','a') as file_object: 
                        for order in list_complete:
                            order_str = str(order[0]) + " , " + str(order[1]) + " , " + str(order[2]) + " , " + order[3]
                            file_object.write(str(order_str))
                if(len(list_cancel)>0):
                    with open('OrderList_Cancelled.txt','a') as file_object: 
                        for order in list_cancel:
                            order_str = str(order[0]) + " , " + str(order[1]) + " , " + str(order[2]) + " , " + order[3]
                            file_object.write(str(order_str))
    
    #已完成的訂單
    if orderlist_type == '2':
        #讀取OrderList_Completed.txt的檔案
        with open('OrderList_Completed.txt','r+') as file_object:
            orderlist = []
            for line in file_object:
                orderlist.append(line.split(' , '))
            
            if(len(orderlist)>0):
                                
                #印出所有已完成的訂單明細
                print('\n==========================')
                for order in range(len(orderlist)):
                    
                    #對訂單的content字串處理
                    content_Meallist = []
                    content_Drinklist = []
                    content_str = ''
                    store_flag = 0
                    for content in orderlist[order][2]:
                        if(content.isalnum()):
                            content_str = content_str + content
                        else:
                            if(len(content_str)>0):
                                if(content_str == 'meal'):
                                    store_flag = 0
                                    content_str = ''
                                elif(content_str == 'drink'):
                                    store_flag = 1
                                    content_str = ''
                                elif(store_flag == 0):
                                    store_flag = 0
                                    content_Meallist.append(content_str)
                                    content_str = ''
                                elif(store_flag == 1):
                                    store_flag = 1
                                    content_Drinklist.append(content_str)
                                    content_str = ''
                                    
                    print('OrderID：' + str(orderlist[order][0]))
                    print('TableNum：' + str(orderlist[order][1]))
                    print('Content：')
                    
                    meal_str = ''
                    count = 0
                    for i in range(len(content_Meallist)):
                        meal_str = meal_str + content_Meallist[i]
                        count+=1
                        if(count %4 != 0):
                            meal_str = meal_str + ' - '
                        if(count%4 == 0 and count != 0):
                            print(meal_str)
                            meal_str = ''
                    
                    drink_str = ''
                    count = 0
                    for i in range(len(content_Drinklist)):
                        drink_str = drink_str + content_Drinklist[i]
                        count+=1
                        if(count %3 != 0):
                            drink_str = drink_str + ' - '
                        if(count%3 == 0 and count != 0):
                            print(drink_str)
                            drink_str = ''
                    print('Status：' + orderlist[order][3].strip())
                    print('==========================')
            else:
                print('\n==========================')
                print('No order completed.')
                print('==========================')
    
    #取消的訂單
    if orderlist_type == '3':
        #讀取OrderList_Cancelled.txt的檔案
        with open('OrderList_Cancelled.txt','r+') as file_object:
            orderlist = []
            for line in file_object:
                orderlist.append(line.split(' , '))
            
            if(len(orderlist)>0):
                                
                #印出所有已取消的訂單明細
                print('\n==========================')
                for order in range(len(orderlist)):
                    
                    #對訂單的content字串處理
                    content_Meallist = []
                    content_Drinklist = []
                    content_str = ''
                    store_flag = 0
                    for content in orderlist[order][2]:
                        if(content.isalnum()):
                            content_str = content_str + content
                        else:
                            if(len(content_str)>0):
                                if(content_str == 'meal'):
                                    store_flag = 0
                                    content_str = ''
                                elif(content_str == 'drink'):
                                    store_flag = 1
                                    content_str = ''
                                elif(store_flag == 0):
                                    store_flag = 0
                                    content_Meallist.append(content_str)
                                    content_str = ''
                                elif(store_flag == 1):
                                    store_flag = 1
                                    content_Drinklist.append(content_str)
                                    content_str = ''
                    print('OrderID：' + str(orderlist[order][0]))
                    print('TableNum：' + str(orderlist[order][1]))
                    print('Content：')
                    
                    meal_str = ''
                    count = 0
                    for i in range(len(content_Meallist)):
                        meal_str = meal_str + content_Meallist[i]
                        count+=1
                        if(count %4 != 0):
                            meal_str = meal_str + ' - '
                        if(count%4 == 0 and count != 0):
                            print(meal_str)
                            meal_str = ''
                    
                    drink_str = ''
                    count = 0
                    for i in range(len(content_Drinklist)):
                        drink_str = drink_str + content_Drinklist[i]
                        count+=1
                        if(count %3 != 0):
                            drink_str = drink_str + ' - '
                        if(count%3 == 0 and count != 0):
                            print(drink_str)
                            drink_str = ''
                    print('Status：' + orderlist[order][3].strip())
                    print('==========================')
            else:
                print('\n==========================')
                print('No order was cancelled.')
                print('==========================')
    
#賣家操作頁面
def seller():
    operator1 = ""
    operator2 = ""
    flag1 = 0
    while True:
        print("\n(M = menu,O = orderlist,L = leave)")
        operator1 = input(": ").upper()
        if operator1 == 'M':
            while flag1 == 0:
                print("Meal：")
                for meal in Menu[0][1]:
                    print("  ",meal[0]," : ",end="")
                    for item in range(0,len(meal[1])):
                        for flavor in meal[1][item]:
                            print(flavor,"",end="")
                        if item != len(meal[1])-1:
                            print(", ",end="")
                    print()
                print()

                print("Drink：\n   ",end="")
                for drink in range(0,len(Menu[1][1])):
                    for flavor in Menu[1][1][drink]:
                        print(flavor,"",end="")
                    if drink != len(Menu[1][1])-1:
                        print(", ",end="")
                print()
                
                print("\n(D = delete,A = add,C = change,L = leave)")
                operator2 = input(": ").upper()
                if operator2 == 'D':
                    delete_item()

                elif operator2 == 'A':
                    add_item()

                elif operator2 == 'C':
                    change_item()
                        
                elif operator2 == 'L':
                    flag1 = 1
                    
                else:
                    print("Wrong")

            
        elif operator1 == 'O':
            inspect_orderlist()
                    
        elif operator1 == 'L':
            break
                
        else:
            print("Wrong")

# 輸入金錢和國家幣值代號
# 美元USD
# 人民幣 CNY
# 港幣 HKD
# 日幣 JPY
def change(money,contry):
    r = requests.get('https://www.xe.com/currencyconverter/convert/?Amount='+str(money)+'&From=TWD&To='+contry)
    start = r.text.find('<p class="result__BigRate-sc-1bsijpp-1 iGrAod">')+len('<p class="result__BigRate-sc-1bsijpp-1 iGrAod">')
    end = r.text.find('<span class="faded-digits">')
    return r.text[start:end]


#使用while迴圈，模擬自助點餐機
while True:
    if login() == False:
        print("print again.")
    else:
        print("bye~\n")
        print("Press [ENTER] to Exit...")
        while True:
            if ord(msvcrt.getch()) in [13]:
                break