from datetime import datetime

def get_time():
    now = datetime.now()
    nowtime = str(now.strftime("%Y-%m-%d %H:%M"))
    return nowtime

def hello():
    current_time = datetime.now().time()

    if datetime.strptime('06:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('09:00:00',
                                                                                             '%H:%M:%S').time():
        greeting = '早上好'
    elif datetime.strptime('09:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('11:00:00',
                                                                                               '%H:%M:%S').time():
        greeting = '上午好'
    elif datetime.strptime('11:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('13:00:00',
                                                                                               '%H:%M:%S').time():
        greeting = '中午好'
    elif datetime.strptime('13:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('18:00:00',
                                                                                               '%H:%M:%S').time():
        greeting = '下午好'
    elif (datetime.strptime('18:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('23:59:59','%H:%M:%S').time()
          or datetime.strptime('00:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('05:59:59', '%H:%M:%S').time()):
        greeting = '晚上好'
    else:
        greeting = '时间不在范围内'

    return greeting

if __name__ == "__main__":
    print(get_time()[0:10])