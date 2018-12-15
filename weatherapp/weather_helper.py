from weather import Weather, Unit
import datetime

def get_db_conn():
	conn = sqlite3.connect("wapp.db")
	return conn


def get_info_by_location_name(location):

	weather = Weather(unit=Unit.CELSIUS)
	location = weather.lookup_by_location(location)

	condition = None
	if location:
		condition = location.condition

	return condition


def get_forecasts_by_location_name(location):

	weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location(location)

	forecasts = None
	if location:
		forecasts = location.forecast

	return forecasts


def fetch_data(location_str):

	weather_data = []
        weather_forecasts = get_forecasts_by_location_name(location_str)
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


def update_db(weather_app, weather_data):
	if len(weather_data):
		db_cursor = weather_app.get_db_cursor()
		for row in weather_data:
                	# print row
                        sql = "SELECT date FROM wa_location_data WHERE date='%s' AND location='%s' LIMIT 1"%(str(row["date"]), str(row["location"]))
                        db_cursor.execute(sql)
                        record = db_cursor.fetchone()
                        if not record:
                        	sql = "INSERT INTO wa_location_data(date, location, climate, high, low) "
                                sql = sql + "VALUES ('%s','%s','%s',%s,%s)"%(str(row["date"]),str(row["location"]),str(row["climate"]),str(row["high"]),str(row["low"]))
                                # self.db_cursor.executemany(sql, weather_data)
                                db_cursor.execute(sql)
                                # print "record inserted"
                        else:
                        	sql = "UPDATE wa_location_data SET climate='%s', high='%s', low='%s' WHERE date='%s' AND location='%s' LIMIT 1"%(str(row["climate"]), str(row["high"]), str(row["low"]), str(row["date"]), str(row["location"]))
                                db_cursor.execute(sql)
                                # print "record updated"


def refresh_treeview(weather_app):

	label_last_update = weather_app.get_widget("label_last_update")
	label_last_update.set_text("Last Update : ")

        liststore_forecasts = weather_app.get_gtk().ListStore(str, str, str, str)
        treeview_forecasts = weather_app.get_widget("treeview_forecasts")
        treeview_forecasts.set_model(liststore_forecasts)

	searchentry_location = weather_app.get_widget("searchentry_location")
        location_str = searchentry_location.get_text().strip()
	if location_str:

		db_cursor = weather_app.get_db_cursor()
		sql = "SELECT date, climate, high, low FROM wa_location_data WHERE location='%s' ORDER BY date LIMIT 7"%location_str
        	weather_forecasts = db_cursor.execute(sql)
        	if weather_forecasts:
        		for weather_forecast in weather_forecasts:
                		'''liststore_forecasts.append([
                        		weather_forecast.date,
                                	weather_forecast.text,
                                	weather_forecast.high,
                                	weather_forecast.low
                        	])'''
                        	liststore_forecasts.append(weather_forecast)

        		treeview_forecasts.set_model(liststore_forecasts)
			curr_time = datetime.datetime.now()
			curr_time = curr_time.strftime("%a %d-%b-%Y %I:%M:%S %p")
			label_last_update.set_text("Last Update : " + curr_time)
        		# box_top = weather_app.get_widget("box_top")
        		# box_top.pack_start(treeview_forecasts, True, True, 1)


