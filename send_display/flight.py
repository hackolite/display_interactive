class Flight:
    def __init__(self, name, time):
        self.name = name + "_" + time.strftime('%Y_%m_%d_%H_%M') 
        self.time = time

    def get_name(self):
        return self.name +"_" + self.time.strftime('%Y_%m_%d_%H_%M') 

    def set_name(self, new_name):
        self.name = new_name

    def get_time(self):
        return self.time

    def set_time(self, new_time):
        self.time = new_time

    def __str__(self):
        return f"Flight {self.name} at {self.time.strftime('%Y %m %d %H:%M')} UTC"