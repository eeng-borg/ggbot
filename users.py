
class User:

    cooldown = 10


    def __init__(self, name):

        self.name = name
        # User.users.append(name)
        self.has_colldown_ended = True
        