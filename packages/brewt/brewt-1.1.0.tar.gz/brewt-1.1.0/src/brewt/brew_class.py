import uuid
import time
import math
import dbus
import os
import multiprocessing
from multiprocessing import Value
import datetime

class Brew:

    def __init__(self, name, brew_data):
        self.name = name
        self.id = int(uuid.uuid4().fields[0])
        self.brew_time = brew_data[self.name]["brew_time"]
        self.age_time = brew_data[self.name]["age_time"]
        self.age_type = brew_data[self.name]["age_type"]
        self.distill = brew_data[self.name]["distill"]
        self.ingred = brew_data[self.name]["ingred"]
        self.name = self.name.replace("_"," ")
        self.notif_code = self.name[0:3] + str(self.id)[-4:-1]
        # shared memory value for reporting to /t
        self.time_remaining = Value('i', 0)

    def notif_timer(self, state, time_remaining):
        # notification system info https://dbus.freedesktop.org/doc/dbus-python/
        item = "org.freedesktop.Notifications"
        notify_int = dbus.Interface(
            dbus.SessionBus().get_object(item, "/"+item.replace(".", "/")), item)
        
        # state checks
        if state == "brew":
            total_time = self.brew_time * 60
            state_str = f"remaining for brewing."
            end_str = "now "
            if self.distill is not None:
                end_str = end_str + f"distill {self.distill} times, then "
            if self.age_time is not None:
                end_str = end_str + f"age {self.name} for {self.age_time} years in {self.age_type} wood barrel."
            else:
                end_str = f"brewing is now complete!"
        elif state == "age":
            total_time = self.age_time * 60 * 20
            state_str = f"remaining for aging."
            end_str = f"aging is now complete!"
        else:
            return print("no state information discovered for this item.")
            
        time_remaining.value = total_time
        time_remaining_pre = 5

        for s in range(0, 5):
            notify_int.Notify(
                f"brewt", f"{self.id}", u"🍶", f"{self.name}", f"starting timer in {time_remaining_pre} seconds...", [], {"urgency": 1}, 0)
            time.sleep(1)
            time_remaining_pre = 5 - (s + 1)

        for s in range(0, total_time):
            # drift protection appropriated from https://codereview.stackexchange.com/questions/199743/countdown-timer-in-python
            target= datetime.datetime.now()
            one_second_later = datetime.timedelta(seconds=1)

            # kill signal test
            

            # format time remaining string
            if time_remaining.value >= 60:
                hours_str = ""
                days_str = ""
                minutes = math.floor(time_remaining.value/ 60)
                seconds= time_remaining.value % 60
                if minutes > 59: 
                    hours = math.floor(minutes / 60)
                    hours_str = f"{hours}h "
                    minutes = minutes % 60
                    if hours > 24:
                        days = math.floor(hours / 24)
                        days_str = f"{days}d "
                formatted_time = f"{days_str}{hours_str}{minutes}m {seconds}s"
            else:
                formatted_time = time_remaining.value

            # send notification each second  
            notify_int.Notify(
                f"brewt", f"{self.id}", u"🍶", f"{self.name}", f"{formatted_time} {state_str}", [], {"urgency": 1}, 0)
            target += one_second_later
            time.sleep((target - datetime.datetime.now()).total_seconds())
            time_remaining.value = total_time - (s + 1)

        # end notification lives for one minute
        notify_int.Notify(
        f"brewt", f"{self.id}", u"🍶", f"{self.name}", f"{end_str}", [], {"urgency": 1}, 60000)

        print('\a', end="")

    def start_timer(self, state):
        self.timer = multiprocessing.Process(target=self.notif_timer, args=(state, self.time_remaining))
        self.timer.start()
