from gi.repository import Gtk, Gdk, WebKit

class Browser(object):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("browser.glade")
        screen = Gdk.Screen.get_default()
        self.window = builder.get_object("window")
        self.window.set_default_size(screen.get_width(), screen.get_height())
        self.window.show()
        self.go_back_button = builder.get_object("go_back")
        self.go_forward_button = builder.get_object("go_forward")
        self.refresh_button = builder.get_object("refresh")
        self.scrolledwindow = builder.get_object("scrolledwindow")
        self.url = builder.get_object("entry")
        self.search_entry = builder.get_object("search_entry")
        self.view = WebKit.WebView()
        self.scrolledwindow.add(self.view)
        self.view.open("https://google.com.br")
        self.view.show()
        
        # connect webkit signals
        self.view.connect("load-committed", self.check_buttons)
        self.view.connect("title-changed", self.change_title)
        
        #connect gtk signals
        builder.connect_signals({
                                "gtk_main_quit": Gtk.main_quit,
                                "on_entry_activate": self.go_,
                                "on_search_activate": self.search,
                                "go_back_clicked": self.go_back,
                                "go_forward_clicked": self.go_forward,
                                "refresh_clicked": self.refresh,
                                })
                                
    def go_(self, widget):
        """Load the page request"""
        link = self.url.get_text()
        if link.startswith("http://"):
            self.view.open(link)
        else:
            self.view.open("http://" + link)
        self.view.show()
        
    def search(self, widget):
        text = self.search_entry.get_text()
        text = text.replace(" ", "+")
        self.url.set_text("http://www.google.com.br/search?q=" + text)
        self.search_entry.set_text("")
        self.go_(self)

            
    def check_buttons(self, widget, data):
        """check if buttons go_back and go_foward are avaiable and
           updates the url bar with current link"""
        uri = widget.get_main_frame().get_uri()
        self.url.set_text(uri)
        self.go_back_button.set_sensitive(self.view.can_go_back())
        self.go_forward_button.set_sensitive(self.view.can_go_forward())
        
        
    def change_title(self, widget, data, arg):
        """ defines page title """
        title = widget.get_main_frame().get_title()
        self.window.set_title("HeschExplorer - %s" % title)
        
        
    def go_back(self, widget):
        self.view.go_back()
        
        
    def go_forward(self, widget):
        self.view.go_forward()
        
        
    def refresh(self, widget):
        self.view.reload()
        
if __name__ == "__main__":
    browser = Browser()
    Gtk.main()