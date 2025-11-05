

def normalize(value, max_value):
    """Return normalized value"""
    return value / max_value

    # if axis=='x':
    #     return value / self.screen_width
    # elif axis=='y':
    #     return value / self.screen_height
    # elif axis=="d":
    #     max_distance = (self.screen_width**2 + self.screen_height**2)**0.5
    #     return value / max_distance
    # else:
    #     return None