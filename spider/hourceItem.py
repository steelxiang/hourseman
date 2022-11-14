

class Item:

    def __int__(self):
        self.sumPrice=None
        self.aviPrice=None
        self.cell=None
        self.area=None
        self.size=None
        self.model=None
        self.link=None
        self.year=None
        self.layer=None
        self.source=None
        self.time=None
        self.hid=None
        self.type=None

    def __str__(self):
       return self.sumPrice+','+self.aviPrice+','+self.cell+','+self.area+','+self.size+','+self.model+','+self.link+','+self.year+','+self.layer+','+self.source+','+self.time+','+self.hid+','+self.type
