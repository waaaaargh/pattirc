from datetime import datetime

class Message():
    def __init__(self, id, authorname, text, time):
        self.id = id
        self.authorname = authorname
        self.text = text
        self.time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    def render(self):
        return "%s: %s" % (self.authorname, self.text)
