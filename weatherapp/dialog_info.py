import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DialogInfo(Gtk.Dialog):

	def __init__(self, parent, title, msg):
		#Gtk.Dialog.__init__(self, "My Dialog", parent, 0, 
			#(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
		#)
		Gtk.Dialog.__init__(self, title, parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        	self.set_default_size(150, 100)

        	label = Gtk.Label(msg)

        	box = self.get_content_area()
        	box.add(label)
        	self.show_all()


