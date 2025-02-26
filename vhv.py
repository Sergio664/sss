

class comp:

    def __init__(self, processor, videocard, motherboard, rem):
        self.processor = processor
        self.videocard = videocard
        self.motherboard = motherboard
        self.rem = rem
        self.price = 20000

    def info(self):
        print(f"Информация об компьютере:\n"
              f"{self.processor}, {self.videocard},{self.motherboard},{self.rem}\n"
              f"{self.price}")


komp = comp("I7 13700K", "4090TI", "GYGABITE B760", "VIPER 32gb")
komp.info()
