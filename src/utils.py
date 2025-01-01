from datetime import datetime, time
from datetime import datetime, timedelta



 
def sleepUntilOpen():
    now = datetime.now()
    target_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
    if now >= target_time:
        # If the target time has passed, move to the next day
        target_time += timedelta(days=1)
    return int((target_time - now).total_seconds())
