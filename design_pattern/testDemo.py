class simpleLayer:
    background = [0, 0, 0, 0]
    content = "blank"

    def getContent(self):
        return self.content

    def getBackgroud(self):
        return self.background

    def paint(self, painting):
        self.content = painting

    def setParent(self, p):
        self.background[3] = p

    def fillBackground(self, back):
        self.background = back


if __name__ == "__main__":
    dog_layer = simpleLayer()
    dog_layer.paint("Dog")
    dog_layer.fillBackground([0, 0, 255, 0])
    print("Background:", dog_layer.getBackgroud())
    print("Painting:", dog_layer.getContent())
