from datetime import datetime
import time

#utc_now = datetime.utcnow()
#seconds_now = (60 * 60 * utc_now.hour) + (60 * utc_now.minute) + utc_now.second
#utc_ny = (13 * 60 * 60) + (60 * 30)

#t = utc_ny - seconds_now

# define the countdown func.
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

    print('Fire in the hole!!')



# function call
#countdown(int(t))
