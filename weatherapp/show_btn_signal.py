import weather_helper
from sync_data import SyncData

class ShowBtnSignal:

	weather_app = None
	button_show = None

	def __init__(self, weather_app):
		print "SBS : init"
		self.weather_app = weather_app
		self.button_show = weather_app.get_widget("button_show")
		self.button_show.connect("clicked", self.show_btn_signal)


	def show_btn_signal(self, button_show):

		searchentry_location = self.weather_app.get_widget("searchentry_location")
		location_str = searchentry_location.get_text()

		if location_str == "":
			self.weather_app.show_info_dialog("Location required", "Please enter location")
                        return

                weather_info = weather_helper.get_info_by_location_name(location_str)
		label_location_info = self.weather_app.get_widget("label_location_info")

		if not weather_info:
			label_location_info.set_text("Weather info not found for : " + str(location_str))

			liststore_forecasts = self.weather_app.get_gtk().ListStore(str, str, str, str)
			treeview_forecasts = self.weather_app.get_widget("treeview_forecasts")
			treeview_forecasts.set_model(liststore_forecasts)
			return

		label_location_info.set_text(weather_info.text)

		self.show_forecasts()


	def show_forecasts(self):

		searchentry_location = self.weather_app.get_widget("searchentry_location")
                location_str = searchentry_location.get_text()

		if location_str == "":
			self.weather_app.show_info_dialog("Location required", "Please enter location")
			return

		weather_data = weather_helper.fetch_data(location_str)
                print "fetched %s records"%str(len(weather_data))
                weather_helper.update_db(self.weather_app, weather_data)
		weather_helper.refresh_treeview(self.weather_app)

                # weather_forecasts = weather_helper.get_forecasts_by_location_name(location_str)
		'''db_cursor = self.weather_app.get_db_cursor()
		weather_forecasts = db_cursor.execute("SELECT date, climate, high, low FROM wa_location_data")

		liststore_forecasts = self.weather_app.get_gtk().ListStore(str, str, str, str)
		if weather_forecasts:
                        for weather_forecast in weather_forecasts:
				liststore_forecasts.append(weather_forecast)

			treeview_forecasts = self.weather_app.get_widget("treeview_forecasts")
			treeview_forecasts.set_model(liststore_forecasts)
			box_top = self.weather_app.get_widget("box_top")
			box_top.pack_start(treeview_forecasts, True, True, 1)'''


                '''label_forecasts = self.weather_app.get_widget("label_forecasts")
		header = "Date\tClimate\tHigh\tLow\n"
		rows = ""
		if weather_forecasts:
			for weather_forecast in weather_forecasts:
				rows = rows + weather_forecast.date + "\t"
				rows = rows + weather_forecast.text + "\t"
				rows = rows + weather_forecast.high + "\t"
				rows = rows + weather_forecast.low + "\n"


                label_forecasts.set_text(header + rows)'''


