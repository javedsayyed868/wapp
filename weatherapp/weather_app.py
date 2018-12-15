#!/usr/bin/python
import os, sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

from initialize_all import InitializeAll
from show_btn_signal import ShowBtnSignal
from dialog_info import DialogInfo
from sync_data import SyncData

class WeatherApp:

	def __init__(self):

		print "WA : init"
		self.builder = Gtk.Builder()
		InitializeAll(self)
		ShowBtnSignal(self)
		#SyncData(self)
		Gtk.main()


	def set_db_conn(self, db_conn):
		self.db_conn = db_conn
	def get_db_conn(self):
                return self.db_conn


	def set_db_cursor(self, db_cursor):
        	self.db_cursor = db_cursor
        def get_db_cursor(self):
                return self.db_cursor


	def get_gtk(self):
		return Gtk
	def get_gdk(self):
                return Gdk


	def get_widget(self, widget):
		return self.builder.get_object(widget)


	def show_info_dialog(self, title, msg):
		di = DialogInfo(self.get_widget("window_main"), title, msg)
                response = di.run()
		di.destroy()
		return response


	def list_prop(self, obj):
                properties = dir(obj)
                print type(obj)
                print "\t\n" . join(properties)


	def show(self):
		Gtk.main()


'''if __name__ == "__main__":
	try:
		print "main started"
		weather_app = WeatherApp()
		# Gtk.main()
	except Exception as ex:
		print "Something went wrong : " + str(ex)'''
