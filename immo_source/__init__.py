class ImmoSource():
    def __init__(self):
        self.url = ""
        pass

    def update_data(self):
        pass

    def send_data(self, message=None):
        if message is not None:
            print(message)