#import os
import os.path
import site
import sqlite3
#import gobject
from gi.repository import GObject as gobject
#import threading, time #, GObject
#import threading, time 
#from gi.repository import GObject
import weather_helper

class InitializeAll:

	def __init__(self, weather_app):

		print "IA : init"
                # weather_app.builder.add_from_file(os.getcwd() + "/weatherapp/assets/weather-app.glade")
                # weather_app.builder.add_from_file("weatherapp/assets/weather-app.glade")

		self.weather_app = weather_app

		path_found = False
		site_packages = site.getsitepackages()
		if site_packages:
			for site_package in site_packages:
				if os.path.exists(site_package + "/weatherapp/assets/weather-app.glade"):
					weather_app.builder.add_from_file(site_package + "/weatherapp/assets/weather-app.glade")
					path_found = True
					break

		# path_found = False
		if not path_found:
			weather_app.builder.add_from_file("assets/weather-app.glade")
			# weather_app.builder.add_from_file("weather-app.glade")

                weather_app.window_main = weather_app.get_widget("window_main")
		weather_app.window_main.resize(300,380)
                weather_app.window_main.show_all()
                weather_app.window_main.connect("destroy", weather_app.get_gtk().main_quit)

		treeview_forecasts = weather_app.get_widget("treeview_forecasts")
                for i, col_title in enumerate(["Date", "Climate", "High", "Low"]):

                	renderer_text = weather_app.get_gtk().CellRendererText()
                        column = weather_app.get_gtk().TreeViewColumn(col_title, renderer_text, text=i)
                        treeview_forecasts.append_column(column)

		# box_top = weather_app.get_widget("box_top")
                # box_top.pack_start(treeview_forecasts, True, True, 1)

		self.create_db()
		gobject.threads_init()
                self.sync_thread = gobject.timeout_add(10000, self.run)

                #GObject.threads_init()
                #thread = threading.Thread(target=self.run)


	def create_db(self):

		db_conn = sqlite3.connect("wapp.db")
                db_cursor = db_conn.cursor()

		print "Creating table"
		try:
			# Create table
			sql = "CREATE TABLE IF NOT EXISTS wa_location_data "
			sql = sql + "(date DATE, location text, climate text, high text, low text)"
			db_cursor.execute(sql)
			print "Table created successfully"
		except Exception as ex:
			print "Fail to create table : %s"%str(ex)

		# db_cursor.close()
		# db_conn.close()
		self.weather_app.set_db_conn(db_conn)
		self.weather_app.set_db_cursor(db_cursor)


	def run(self):
                print "thread running"
                #time.sleep(5)
                searchentry_location = self.weather_app.get_widget("searchentry_location")
                location_str = searchentry_location.get_text().strip()

                if location_str <> "":
                        print "fetching data for : %s"%location_str
                        weather_data = weather_helper.fetch_data(location_str)
                        print "fetched %s records"%str(len(weather_data))
			weather_helper.update_db(self.weather_app, weather_data)

		weather_helper.refresh_treeview(self.weather_app)

		return True
