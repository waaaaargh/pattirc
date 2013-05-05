import curses

from buffer import Buffer

class Window:
    def init_curses(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.start_color()
        curses.cbreak()
        self.screen.keypad(0)
        curses.curs_set(0)

    def quit_curses(self):
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()


    def update(self):
        pass


    def get_termsize(self):
        numlines = curses.tigetnum("lines")
        numcols = curses.tigetnum("cols")
        return (numlines, numcols)

    def drawscreen(self):
        # determine terminal width and height
        numlines, numcols = self.get_termsize()

        # define colors
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        

        # render title bar
        tbtext = "pattirc v0.0"
        tbtext_padded = tbtext
        for i in range(numcols - len(tbtext)):
            tbtext_padded = tbtext_padded + " "
        self.screen.addstr(0, 0, tbtext_padded, curses.color_pair(1))
        self.screen.refresh()

        # render currend buffer
        if len(self.buffers) > 0:
            currentbuffer = self.buffers[self.buffer_index]
            self.screen.addstr(1,0, currentbuffer.title)
            self.screen.addstr(2,0, currentbuffer.render(width=numcols,
                height=numlines-4))    

        
    def receive_command(self):
        numlines, numcols = self.get_termsize()

        # clear command line
        cl = ""
        for i in range(numcols-1):
            cl += " "

        self.screen.addstr(numlines-1, 0, cl)

        # get command w/ visual response

        curses.echo()
        curses.curs_set(1)
        self.screen.addstr(numlines-1, 0, ":")
        command = self.screen.getstr(numlines-1, 1)
        curses.curs_set(0)
        curses.noecho()

        if command == 'q':
            self.running = False
        else:
            self.screen.addstr(numlines-1,0,"received unknown command:\"%s\"" %
                    (command,))


    def mainloop(self):
        while self.running:
            self.drawscreen()
            c = self.screen.getch()
            if c == ord('h'):
                if self.buffer_index > 0:
                    self.buffer_index -= 1
            elif c == ord('l'):
                if self.buffer_index < len(self.buffers) - 1:
                    self.buffer_index += 1
            elif c == ord('j'):
                if self.buffer_index < len(self.buffers) - 1:
                    self.buffers[self.buffer_index].scroll(5)
            elif c == ord('k'):
                if self.buffer_index < len(self.buffers) - 1:
                    self.buffers[self.buffer_index].scroll(-5)
            elif c == 21:        # Ctrl+u
                self.buffers[self.buffer_index].scroll(-50)
            elif c == 4:        # Ctrl+d
                self.buffers[self.buffer_index].scroll(50)
            elif c == ord(':'):
                self.receive_command()
            # use this for debugging.
            #else:
                #self.buffers[self.buffer_index].content.append(
                        #"Key Pressed:" + str(c))

        self.quit_curses()

    def __init__(self):
        self.running = True
        self.buffers = []
        self.buffer_index = 0
        for i in range(3):
            self.buffers.append(Buffer("Buffer "+str(i)))
        self.init_curses()
