import os
import appuifw
import e32
import dir_iter
import graphics
try:
    os.listdir("e:\\python\\PyResizePic\\")
except:
    os.mkdir("e:\\python\\PyResizePic\\")
class Filebrowser:
    def __init__(self):
        self.script_lock = e32.Ao_lock()
        self.dir_stack = []
        self.current_dir = dir_iter.Directory_iter(e32.drive_list())

    def run(self):
        from key_codes import EKeyLeftArrow
        entries = self.current_dir.list_repr()
        if not self.current_dir.at_root:
            entries.insert(0, (u"..", u""))
        self.lb = appuifw.Listbox(entries, self.lbox_observe)
        self.lb.bind(EKeyLeftArrow, lambda: self.lbox_observe(0))
        old_title = appuifw.app.title
        self.refresh()
        self.script_lock.wait()
        appuifw.app.title = old_title
        appuifw.app.body = None
        self.lb = None
        

    def refresh(self):
        appuifw.app.title = u"pyResizePic"
        appuifw.app.menu = [(u"Change size pic", self.select), (u"about", self.about), (u"version", self.version)]
        appuifw.app.exit_key_handler = self.exit_key_handler
        appuifw.app.body = self.lb

    def do_exit(self):
        self.exit_key_handler()

    def exit_key_handler(self):
        appuifw.app.exit_key_handler = None
        self.script_lock.signal()
    def about(self):
        appuifw.note(u"made by ItsMyLive", "info")
    def version(self):
        appuifw.note(u"V 1.50", "info")
    def select(self):
        appuifw.note(u"go to picture then click select!", "info")

    def lbox_observe(self, ind = None):
        if not ind == None:
            index = ind
        else:
            index = self.lb.current()
        focused_item = 0

        if self.current_dir.at_root:
            self.dir_stack.append(index)
            self.current_dir.add(index)
        elif index == 0:                              # ".." selected
            focused_item = self.dir_stack.pop()
            self.current_dir.pop()
        elif os.path.isdir(self.current_dir.entry(index-1)):
            self.dir_stack.append(index)
            self.current_dir.add(index-1)
        else:
            item = self.current_dir.entry(index-1)
            if os.path.splitext(item)[1] == '.py':
                i = appuifw.popup_menu([u"open python", u"Delete"])
            elif os.path.splitext(item)[1] == '.jpg':
                i = appuifw.popup_menu([u"open pic",u"Delete" , u"change size pic"])
            elif os.path.splitext(item)[1] == '.png':
                i = appuifw.popup_menu([u"open pic", u"Delete", u"change size pic"])
                
            else:
                i = appuifw.popup_menu([u"Open", u"Delete"])
           
            if i == 0:
                if os.path.splitext(item)[1].lower() == u'.py':
                    execfile(item, globals())
                    self.refresh()
                    #appuifw.Content_handler().open_standalone(item)
                elif os.path.splitext(item)[1].lower() == u'.jpg':
                    appuifw.Content_handler().open(item)
                elif os.path.splitext(item)[1].lower() == u'.png':
                    appuifw.Content_handler().open(item)
                    
                else:    
                    try:
                        appuifw.Content_handler().open(item)
                    except:
                        import sys
                        type, value = sys.exc_info() [:2]
                        appuifw.note(unicode(str(type)+'\n'+str(value)), "info")
                return
            elif i == 1:
                os.remove(item)
                focused_item = index - 1
            elif i == 2:
                if os.path.splitext(item)[1].lower() == u'.jpg':
                    img=graphics.Image.open(item)
                    w=appuifw.query(u"Width", "number")
                    d = appuifw.query(u"Height", "number")
                    img=img.resize((w,d), keepaspect=0 )
                    if appuifw.query(u"do you want change name pic", "query")==True:
                        namu=appuifw.query(u"please put name pic", "text")
                        img.save("e:\\PyResizePic\\"+namu+".jpg")
                    else:
                        img.save("e:\\PyResizePic\\image.jpg")
                    appuifw.note(u"image resize successfully", "conf")
                    focused_item = index - 1
            
                elif os.path.splitext(item)[1].lower() == u'.png':
                    img=graphics.Image.open(item)
                    w=appuifw.query(u"Width", "number")
                    d = appuifw.query(u"Height", "number")
                    img=img.resize((w,d), keepaspect=0 )
                    if appuifw.query(u"do you want change name pic", "query")==True:
                        namu=appuifw.query(u"please put name pic", "text")
                        img.save("e:\\PyResizePic\\"+namu+".png")
                    else:
                        img.save("e:\\PyResizePic\\image.png")
                    appuifw.note(u"image resize successfully", "conf")
                    focused_item = index - 1

                

        entries = self.current_dir.list_repr()
        if not self.current_dir.at_root:
            entries.insert(0, (u"..", u""))
        self.lb.set_list(entries, focused_item)

   

if __name__ == '__main__':
    Filebrowser().run()
