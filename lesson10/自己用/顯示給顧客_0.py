import datetime
import calendar

def calculate_shipping_date(year, month, week):
    """計算給定年份、月份和週次的星期一日期"""
    first_day_of_month = datetime.date(year, month, 1)
    first_weekday = first_day_of_month.weekday()
    first_monday = first_day_of_month + datetime.timedelta(days=(7-first_weekday) % 7)
    shipping_date = first_monday + datetime.timedelta(weeks=week-1)

    if shipping_date.month != month:
        raise ValueError("輸入的週次超出了該月的範圍。")
    
    return shipping_date

def weekday_to_chinese(weekday):
    """將星期數字轉換為中文"""
    weekdays = ["一", "二", "三", "四", "五", "六", "日"]
    return weekdays[weekday]

def shipment_form():
    year = int(input("請輸入年份："))
    
    month = input("請輸入月份（1-12）：")
    if month.isdigit() and 1 <= int(month) <= 12:
        month = int(month)
    else:
        print("輸入的月份不正確。")
        return
    
    week = input("請輸入週次（1-4/5）：")
    if week.isdigit() and 1 <= int(week) <= 5:
        week = int(week)
    else:
        print("輸入的週次不正確。")
        return
    
    items_with_quantities = {}
    print("請依次輸入品項及其最大出貨量，輸入'完成'結束輸入：")
    while True:
        item = input("請輸入品項（輸入'完成'結束輸入）：")
        if item == '完成':
            break
        max_quantity = input(f"請輸入{item}的最大出貨量：")
        if max_quantity.isdigit():
            items_with_quantities[item] = int(max_quantity)
        else:
            print("輸入的最大出貨量不正確，請重新輸入。")
    
    try:
        shipping_date = calculate_shipping_date(year, month, week)
        weekday = weekday_to_chinese(shipping_date.weekday())
        print(f"\n親愛的客戶您好！\n本次可出貨的日期為：{shipping_date.strftime('%Y-%m-%d')}，星期{weekday}（{shipping_date.strftime('%A')}）")
        for item, quantity in items_with_quantities.items():
            print(f"可出貨的品項為：{item}，可以出貨的最大量為：{quantity}")
        print("\n感謝您的訂購，謝謝！")
    except ValueError as e:
        print(e)

# 執行表單函數
shipment_form()