class Buffer:
    def __init__(self, name, generator):
        self.top = 0
        self.name = name
        self.observers = []
        self.content = []
        self.generator = generator
        self.generator.observers.append(self)
        self.update() 

    def update(self):
        self.content = self.generator.render()
        for o in self.observers:
            o.update()

    def scroll(self, lines):
        """
        moves down top by the specified number of lines which also can be
        negative
        """
        if self.top + lines >= 0:
            if self.top + lines < len(self.content):
                self.top += lines
            else:
                self.top = len(self.content) - 1
        else:
            self.top = 0

    def render(self, width, height):
        """
        renders a buffer to an array of strings, each not exceeding <width> and
        not exceeding a total number of <height>. skips the first <top> lines
        """
        lines = []
        for c in self.content:
            if len(c) > width:
                # truncate long lines
                lines.append(c[:width-1])
            else:
                lines.append(c)

        rendered_lines = lines[self.top:self.top+height]

        # padding 
        if len(rendered_lines) < height:
            for i in range(height - len(rendered_lines)):
                rendered_lines.append("~")

        rendered_str = ""

        for line in rendered_lines:
            rendered_str += line.encode("utf-8") + "\n"

        return rendered_str
