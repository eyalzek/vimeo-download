#!/usr/bin/env python

import webbrowser
import get_vimeo_urls
from Tkinter import Tk, Frame, Label, Entry, Button, BOTH, StringVar
from tkMessageBox import askokcancel, showinfo


class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        view = Frame(self)
        view.pack(fill=BOTH)
        self.parent.title("Download Vimeo")
        self.pack(fill=BOTH, expand=1)
        url = StringVar(view)
        Label(view, text='Enter page url').pack(fill=BOTH)
        Entry(view, textvariable=url, width=50).pack(fill=BOTH)
        action = lambda: self.get_links(url.get())
        Button(view, text='get links', command=action).pack(fill=BOTH)

    def get_links(self, url):
        if not url.startswith('http'):
            showinfo(title='info', message='Invalid URL entered')
            return
        results = get_vimeo_urls.gui_flow(url)
        print(results)
        if len(results) > 0:
            self.display_results(results)
        else:
            showinfo(title='info', message='No results found')

    def display_results(self, results):
        view = Frame(self)
        view.pack(fill=BOTH)
        Label(view, text='Results', fg='red').pack(fill=BOTH)
        for k, v in results.iteritems():
            self.pack_result(view, k, v)

    def pack_result(self, view, url, results):
        subview = Frame(view)
        subview.pack(fill=BOTH)
        Label(subview, text=url).pack(fill=BOTH)
        for result in results:
            link = Label(subview, text='%s quality (%sMB)' % (
                result['quality'], result['size']), fg='blue', cursor='hand2')
            link.pack(fill=BOTH)
            link.bind('<Button-1>',
                      lambda e: self.open_browser_action(result['url']))

    def open_browser_action(self, url):
        print(url)
        webbrowser.open_new(url)

    def ask_quit(self):
        if askokcancel('Quit', 'Quit the program?'):
            self.parent.destroy()


def main():
    root = Tk()
    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.ask_quit)
    root.mainloop()

if __name__ == '__main__':
    main()
