from datetime import datetime, time
from datetime import datetime, timedelta


def is_trading_hours():
    start_time = time(9, 30)  # 9:30 AM
    end_time = time(16, 0)    # 4:00 PM
    now = datetime.now().time()

    # Python handles 24-hour format automatically
    if start_time <= now <= end_time:
        return True
    else:
        return False

def is_weekend():
    today = datetime.now().weekday()
    if today == 5 or today == 6:
        return False
    else:
     return True
 
 
def sleepUntilOpen():
    now = datetime.now()
    target_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
    if now >= target_time:
        # If the target time has passed, move to the next day
        target_time += timedelta(days=1)
    return int((target_time - now).total_seconds())
