import sys
import threading
import time


class UserNotFoundError(Exception):
    pass


class Cooldown:

    # if len(sys.argv) > 1 and :
    #     cooldown_time = int(sys.argv[1])
        
    # else:
    cooldown_time = 20

        

    instances = [] # class instances


    def __init__(self, name):

        self.name = name
        # Cooldown.users.append(name)
        self.on_cooldown = False
        self.start_time = 0
        Cooldown.instances.append(self)

        

    def end(self):

        self.on_cooldown = False


    def start(self):
        if not self.on_cooldown:
            self.start_time = time.time()
            timer = threading.Timer(Cooldown.cooldown_time, self.end)
            timer.start() # do not exexutes

            self.on_cooldown = True


    # calulate how much time is left to end cooldown
    def time_remaining(self):
        
        elapsed = time.time() - self.start_time
        remaining = self.cooldown_time - elapsed
        remaining = int(remaining)

        return max(0, remaining)


    @staticmethod
    def find_user(name) -> 'Cooldown':

        user = Cooldown
        for user in Cooldown.instances:

            if user.name == name:
                return user
        
        return Cooldown(name)
            
        # raise UserNotFoundError(f"No user found with name: {name}")


        