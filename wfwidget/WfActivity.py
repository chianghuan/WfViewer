class WfActivity:
    x = 0.0
    y = 0.0
    aid = -1
    def __init__(self, x, y, aid, width=0, height=0, color="grey"):
        self.x=x
        self.y=y
        self.color=color
        self.aid=aid

    def setArttribute(self, **attr):
        self.attributes=attr

    def setPosition(self, x, y):
        self.x=x
        self.y=y

    def setSize(self, width, height):
        self.width=width
        self.height=height

    def getPosition(self):
        return (self.x, self.y)

    def getN(self):
        return (self.x+WfActivity.width/2, self.y)

    def getE(self):
        return (self.x+WfActivity.width, self.y+WfActivity.height/2)

    def getS(self):
        return (self.x+WfActivity.width/2, self.y+WfActivity.height)

    def getW(self):
        return (self.x, self.y+WfActivity.height/2)
