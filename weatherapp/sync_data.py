import sqlite3
import gobject
import time
import weather_helper

class SyncData:

	def __init__(self, weather_app):
		print "SD : init"
		self.weather_app = weather_app
		db_conn = weather_app.get_db_conn() # sqlite3.connect("wapp.db")
                db_cursor = weather_app.get_db_cursor() # db_conn.cursor()
		self.db_conn = db_conn
		self.db_cursor = db_cursor

		gobject.threads_init()
		self.thread = gobject.timeout_add(5000, self.run)
		# self.run()


	def get_conn(self):
		return self.db_conn
	def get_cursor(self):
		return self.db_cursor


	def run(self):
		print "thread running"
		searchentry_location = self.weather_app.get_widget("searchentry_location")
                location_str = searchentry_location.get_text().strip()

                if location_str <> "":
                	print "fetching data for : %s"%location_str
                        weather_data = self.fetch_data(location_str)
                        print "fetched %s records"%str(len(weather_data))
                        if len(weather_data):
				for row in weather_data:
					#print row
					sql = "SELECT date FROM wa_location_data WHERE date='%s' AND location='%s' LIMIT 1"%(str(row["date"]), str(row["location"]))
					self.db_cursor.execute(sql)
					record = self.db_cursor.fetchone()
					if not record:
						sql = "INSERT INTO wa_location_data(date, location, climate, high, low) "
						sql = sql + "VALUES ('%s','%s','%s',%s,%s)"%(str(row["date"]),str(row["location"]),str(row["climate"]),str(row["high"]),str(row["low"]))
                                		# self.db_cursor.executemany(sql, weather_data)
						print "sql : %s"%sql
						self.db_cursor.execute(sql)
						print "record inserted"
					else:
						sql = "UPDATE wa_location_data SET climate='%s', high='%s', low='%s' WHERE date='%s' AND location='%s' LIMIT 1"%(str(row["date"]), str(row["location"]))
						print "sql : %s"%sql
						self.db_cursor.execute(sql)
						print "record updated"
				

		return True


	def run_old(self):

		print "sleeping 5sec..."
                time.sleep(5)

		while True:
			searchentry_location = self.weather_app.get_widget("searchentry_location")
			location_str = searchentry_location.get_text().strip()

			if location_str <> "":
				print "fetching data for : %s"%location_str
				weather_data = self.fetch_data(location_str)
				print "fetched %s records"%str(len(weather_data))
				if len(weather_data):
					sql = "INSERT INTO wa_location_data VALUES (?,?,?,?,?)"
					self.db_cursor.executemany(sql, weather_data)
					print "inserted %s records"%str(len(weather_data))

			#print "sleeping 5sec..."
			#time.sleep(5)


	def fetch_data(self, location_str):

		weather_data = []
		weather_forecasts = weather_helper.get_forecasts_by_location_name(location_str)
                if weather_forecasts:
                        for weather_forecast in weather_forecasts:
				'''row = (
					location_str,
					weather_forecast.date,
					weather_forecast.text,
					int(weather_forecast.high),
					int(weather_forecast.low)
				)'''
				row = {}
                                row["date"] = weather_forecast.date
				row["location"] = location_str
                                row["climate"] = weather_forecast.text
                                row["high"] = weather_forecast.high
                                row["low"] = weather_forecast.low
				weather_data.append(row)

		return weather_data

