class Review:
    def __init__(self, idr, brand, variety, style, origin, stars):
        self.idr = idr
        self.brand = brand
        self.variety = variety
        self.style = style
        self.origin = origin
        self.stars = stars

    def __str__(self):
        return "{}: {}, Varieties: {}, Style: {} Stars: {}".format(self.idr, self.brand, self.variety, self.style, self.stars)