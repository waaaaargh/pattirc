import time
import threading
import curses

from buffer import Buffer
from client import Client

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
        self.dontupdate.acquire()
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

        # render current buffer
        if len(self.buffers) > 0:
            currentbuffer = self.buffers[self.buffer_index]
            blankline = ""
            for i in range(numcols):
                blankline += " "
            self.screen.addstr(1,0, blankline)
            self.screen.addstr(1,0, currentbuffer.name)
            self.screen.addstr(2,0, currentbuffer.render(width=numcols,
                height=numlines-4))    

        self.dontupdate.release()
        
    def receive_command(self):
        numlines, numcols = self.get_termsize()

        # clear command line
        cl = ""
        for i in range(numcols-1):
            cl += " "

        self.screen.addstr(numlines-1, 0, cl)

        # get command w/ visual response
        self.dontupdate.acquire()
        curses.echo()
        curses.curs_set(1)
        self.screen.addstr(numlines-1, 0, ":")
        command = self.screen.getstr(numlines-1, 1)
        curses.curs_set(0)
        curses.noecho()
        self.dontupdate.release()

        if command == 'q':
            self.running = False
        else:
            self.screen.addstr(numlines-1,0,"received unknown command:\"%s\"" %
                    (command,))

    def create_message(self):
        numlines, numcols = self.get_termsize()

        # clear command line
        cl = ""
        for i in range(numcols-1):
            cl += " "

        self.dontupdate.acquire()
        self.screen.addstr(numlines-1, 0, cl)

        # get command w/ visual response

        curses.echo()
        curses.curs_set(1)
        self.screen.addstr(numlines-1, 0, "# ")
        message = self.screen.getstr(numlines-1, 1)
        curses.curs_set(0)
        curses.noecho()
        channel = self.buffers[self.buffer_index].generator
        channel.send_message(message)
        self.dontupdate.release()

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
            elif c == ord('i'):
                self.create_message()
            elif c == ord(':'):
                self.receive_command()

        self.quitting.set()
        self.quit_curses()

    @staticmethod
    def refresh_messages(channels, signal):
        while not signal.is_set():
            for channel in channels:
                channel.retrieve_messages()
                channel.update()
            time.sleep(5)

    def update(self):
        self.drawscreen()


    def __init__(self, access_token):
        self.running = True
        self.buffers = []
        self.buffer_index = 0
        self.client = Client(access_token=access_token)
        self.client.get_my_channels()
        for channel in self.client.channels:
            tmp = Buffer(channel.name, channel)
            tmp.observers.append(self)
            self.buffers.append(tmp)

        self.dontupdate = threading.Lock()
        self.quitting = threading.Event()
        self.updatethread = threading.Thread(target=Window.refresh_messages,
                args=(self.client.channels, self.quitting))
        self.updatethread.start()
        self.init_curses()
