import customtkinter as ctk
from customtkinter.windows.widgets.font.ctk_font import Literal
from datetime import datetime, timezone
import random
import time
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor
from file_classes import Airport
from files import initialize_airports, initialize_country, initialize_runway
from distance import get_distance, calculate_distance_from_timecode
from runway import get_runway_id
from airport import get_airport_id, get_airport_id_from_internal
from metar import get_metar
from globals import AIRCRAFTS, airports, countries, runways
from popup import ScrollablePopup
from helpers import distance_to_time, get_airport_info
from clock import find_timezone_from_input

ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aviation Tool")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.popup_window = None


        self.utc_clock_label = self.new_label("", "normal", 20, family="Courier")
        self.utc_clock_label.place(relx=0.99, rely=0.03, anchor=ctk.E)

        self.departure_label = self.new_label("Departure", "bold", 18)
        self.departure_label.place(relx=0.10, rely=0.09, anchor=ctk.W)
        self.departure_airport_info = self.new_label("", "normal", 14)
        self.departure_airport_info.place(relx=0.235, rely=0.09, anchor=ctk.W)

        self.departure_prompt = self.new_prompt("SPJC", 120)
        self.departure_prompt.place(relx=0.10, rely=0.14, anchor=ctk.W)

        self.departure_metar_button = ctk.CTkButton(
            self, text="Get METAR", command=self.get_departure_metar, width=95
        )
        self.departure_metar_button.place(relx=0.235, rely=0.14, anchor=ctk.W)

        self.departure_iata_label = self.new_label("", "normal", 12)
        self.departure_iata_label.place(relx=0.35, rely=0.14, anchor=ctk.W)

        self.departure_metar_category_label = self.new_label("", "normal", 12) # Category: VFR
        self.departure_metar_category_label.place(relx=0.40, rely=0.14, anchor=ctk.W)
        self.departure_elevation_label = self.new_label("", "normal", 12) # Elevation: 0 ft
        self.departure_elevation_label.place(relx=0.50, rely=0.14, anchor=ctk.W)
        self.departure_time_label = self.new_label("", "normal", 12) # Local Time: 00:00
        self.departure_time_label.place(relx=0.61, rely=0.14, anchor=ctk.W)

        self.departure_metar_display = self.new_label("", "normal", 12) # METAR KDFW 090159Z 14010G20KT 10SM -TSRA FEW036 BKN048CB BKN065 OVC140 22/18 A2987 RMK AO2 PK WND 25032/0125 TS ONOE MOV NE EWR 29 SLP116
        self.departure_metar_display.place(relx=0.030, rely=0.20, anchor=ctk.W)

        self.arrival_distance_label = self.new_label("", "normal", 12)
        self.arrival_distance_label.place(relx=0.08, rely=0.26, anchor=ctk.E)
        self.flight_time_label = self.new_label("", "normal", 12)
        self.flight_time_label.place(relx=0.08, rely=0.31, anchor=ctk.E)

        self.arrival_label = self.new_label("Arrival", "bold", 20)
        self.arrival_label.place(relx=0.10, rely=0.25, anchor=ctk.W)
        self.arrival_airport_info = self.new_label("", "normal", 14)
        self.arrival_airport_info.place(relx=0.235, rely=0.25, anchor=ctk.W)

        self.arrival_prompt = self.new_prompt("KCLE", 120)
        self.arrival_prompt.place(relx=0.10, rely=0.30, anchor=ctk.W)

        self.arrival_metar_button = ctk.CTkButton(
            self, text="Get METAR", command=self.get_arrival_metar, width=95
        )
        self.arrival_metar_button.place(relx=0.235, rely=0.30, anchor=ctk.W)

        self.arrival_iata_label = self.new_label("", "normal", 12)
        self.arrival_iata_label.place(relx=0.35, rely=0.30, anchor=ctk.W)

        self.arrival_metar_category_label = self.new_label("", "normal", 12)
        self.arrival_metar_category_label.place(relx=0.40, rely=0.30, anchor=ctk.W)
        self.arrival_elevation_label = self.new_label("", "normal", 12)
        self.arrival_elevation_label.place(relx=0.50, rely=0.30, anchor=ctk.W)
        self.arrival_time_label = self.new_label("", "normal", 12)
        self.arrival_time_label.place(relx=0.61, rely=0.30, anchor=ctk.W)

        self.arrival_metar_display = self.new_label("", "normal", 12) # METAR KCLE 031351Z 02012KT 10SM SCT026 22/15 A2995 RMK AO2 SLP152 T02170150 $
        self.arrival_metar_display.place(relx=0.030, rely=0.36, anchor=ctk.W)

        self.min_label = self.new_label("Minimum Time", "normal", 12)
        self.min_label.place(relx=0.10, rely=0.41, anchor=ctk.W)
        self.min_hour_prompt = self.new_prompt("00", 35)
        self.min_hour_prompt.place(relx=0.10, rely=0.45, anchor=ctk.W)
        self.min_separator_label = self.new_label(":", "normal", 12)
        self.min_separator_label.place(relx=0.14, rely=0.45, anchor=ctk.W)
        self.min_minute_prompt = self.new_prompt("30", 35)
        self.min_minute_prompt.place(relx=0.15, rely=0.45, anchor=ctk.W)

        self.max_label = self.new_label("Maximum Time", "normal", 12)
        self.max_label.place(relx=0.235, rely=0.41, anchor=ctk.W)
        self.max_hour_prompt = self.new_prompt("02", 35)
        self.max_hour_prompt.place(relx=0.235, rely=0.45, anchor=ctk.W)
        self.max_separator_label = self.new_label(":", "normal", 12)
        self.max_separator_label.place(relx=0.275, rely=0.45, anchor=ctk.W)
        self.max_minute_prompt = self.new_prompt("30", 35)
        self.max_minute_prompt.place(relx=0.285, rely=0.45, anchor=ctk.W)

        self.aircraft_select_label = self.new_label("Aircraft", "normal", 12)
        self.aircraft_select_label.place(relx=0.10, rely=0.51, anchor=ctk.W)
        self.aircraft_select_options = ["A319", "A320", "A321", "737-600", "737-700", "777-300ER"]
        self.aircraft_selector = ctk.CTkOptionMenu(
            self,
            values=self.aircraft_select_options,
            command=self.aircraft_changed,
            width=100
        )
        self.aircraft_selector.place(relx=0.10, rely=0.55, anchor=ctk.W)

        self.runway_length_prompt = self.new_prompt("Landing Distance", 140)
        self.runway_length_prompt.place(relx=0.10, rely=0.61, anchor=ctk.W)
        self.speed_prompt = self.new_prompt("Speed", 60)
        self.speed_prompt.place(relx=0.25, rely=0.61, anchor=ctk.W)

        self.check_var = ctk.StringVar(value="on")
        self.checkbox = ctk.CTkCheckBox(self, text="Airports with scheduled routes only", variable=self.check_var, onvalue="on", offvalue="off") #, command=self.checkbox_event
        self.checkbox.place(relx=0.10, rely=0.71, anchor=ctk.W)

        self.program_output = self.new_label("", "bold", 12)
        self.program_output.place(relx=0.50, rely=0.77, anchor=ctk.CENTER)

        self.clear_button = ctk.CTkButton(
            self, text="Clear", command=self.clear, width=140, height=40
        )
        self.clear_button.place(relx=0.20, rely=0.85, anchor=ctk.W)

        self.find_button = ctk.CTkButton(
            self, text="Find Airports", command=self.find_airports, width=140, height=40
        )
        self.find_button.place(relx=0.50, rely=0.85, anchor=ctk.CENTER)

        self.next_button = ctk.CTkButton(
            self, text="Find Next Airports", command=self.next_airports, width=140, height=40
        )
        self.next_button.place(relx=0.80, rely=0.85, anchor=ctk.E)

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            width=90
        )
        self.appearance_mode_optionemenu.place(relx=0.995, rely=0.97, anchor=ctk.E)
        self.appearance_mode_optionemenu.set("Dark")

    def new_label(self, text, font_weight: Literal["normal", "bold"], font_size=16, family="Arial"): # noqa: F821 # idk ??
        return ctk.CTkLabel(self, text=f"{text}", fg_color="transparent", font=ctk.CTkFont(size=font_size, weight=font_weight, family=family))

    def new_prompt(self, text, w=100, h=35):
        return ctk.CTkEntry(
            master = self,
            placeholder_text=f"{text}",
            width=w,
            height=h,
            corner_radius=8
        )

    def get_arrival_metar(self):
        update_metar("arrival")

    def get_departure_metar(self):
        update_metar("departure")

    def aircraft_changed(self, new_aircraft: str):
        self.aircraft_selector.set(new_aircraft)
        update_aircraft()

    def next_airports(self):
        new_departure = self.arrival_prompt.get()
        if new_departure != "":
            clear_for_next()
            self.departure_prompt.set(new_departure)
            find_airports()

    def find_airports(self):
        find_airports()

    def clear(self):
        self.min_hour_prompt.set("")
        self.min_minute_prompt.set("")
        self.max_hour_prompt.set("")
        self.max_minute_prompt.set("")
        clear_for_next()

    #def checkbox_event(self):
        #print("checkbox toggled ", self.check_var.get())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)


def clear_arrivals():
    app.arrival_prompt.set("")
    app.arrival_airport_info.configure(text="")
    app.arrival_iata_label.configure(text="")
    app.arrival_metar_category_label.configure(text="")
    app.arrival_elevation_label.configure(text="")
    app.arrival_metar_display.configure(text="")
    app.arrival_time_label.configure(text="")

def clear_departures():
    app.departure_prompt.set("")
    app.departure_airport_info.configure(text="")
    app.departure_iata_label.configure(text="")
    app.departure_metar_category_label.configure(text="")
    app.departure_elevation_label.configure(text="")
    app.departure_metar_display.configure(text="")
    app.departure_time_label.configure(text="")

def clear_for_next():
    clear_departures()
    clear_arrivals()
    app.flight_time_label.configure(text="")
    app.arrival_distance_label.configure(text="")

def get_airports_within_limits(departure_airport: list, min_distance: float, max_distance: float):
    departure_airport_lat = departure_airport[0].lat
    departure_airport_long = departure_airport[0].long
    elegible_airport_ids = []
    distances = []
    for airport_id, airport in airports.items():
        distance = get_distance(float(departure_airport_lat), float(departure_airport_long), float(airport.lat), float(airport.long))
        if runways:
            arrival_airport_longest_runway_id = get_runway_id(runways, airport_id)
            arrival_airport_longest_runway = runways.get(arrival_airport_longest_runway_id)
            if arrival_airport_longest_runway:
                arrival_airport_longest_runway_length = arrival_airport_longest_runway.length
                min_runway_length = float(app.runway_length_prompt.get())
                if float(distance) <= max_distance and float(distance) >= min_distance and int(arrival_airport_longest_runway_length) >= min_runway_length and ((app.check_var.get() == "on" and airport.shed_serv == "yes") or app.check_var.get() == "off"):
                    elegible_airport_ids.append(airport_id)
                    distances.append(distance)
    return elegible_airport_ids, distances

def check_min_runway_length(airport_id):
    arrival_airport_longest_runway_id = get_runway_id(runways, airport_id)
    arrival_airport_longest_runway = runways.get(arrival_airport_longest_runway_id)
    if arrival_airport_longest_runway:
        arrival_airport_longest_runway_length = arrival_airport_longest_runway.length
        return float(arrival_airport_longest_runway_length) >= float(app.runway_length_prompt.get())
    else:
        return False

def random_airport():
    def get_airport():
        random_number = random.randint(0, len(airports))
        airport_id = get_airport_id_from_internal(airports, random_number)
        airport = airports.get(airport_id)
        return airport

    airport = get_airport()

    while airport and app.check_var.get() == "on" and airport.shed_serv == "no":
        airport = get_airport()

    while airport and not check_min_runway_length(airport.id):
        airport = get_airport()

    if airport: return airport.ident

def handle_result(future):
    try:
        app.program_output.configure(text="")
        data = future.result()
        elegible_airport_ids = data[0]
        distances = data[1]

        if len(elegible_airport_ids) <= 0:
            app.program_output.configure(text="No available airports for selection.")

        ScrollablePopup(app, elegible_airport_ids, distances, int(app.speed_prompt.get()))

    except Exception as e:
        print(f"Thread generated an exception: {e}")
        app.program_output.configure(text=f"Thread generated an exception: {e}")

def find_airports():
    app.program_output.configure(text="")
    departure_airport_value = app.departure_prompt.get()
    if departure_airport_value:
        departure_airport = get_airport_info(get_airport_id(airports, departure_airport_value.strip()))
    else:
        departure_airport_value = random_airport()
        departure_airport = get_airport_info(get_airport_id(airports, str(departure_airport_value).strip()))
        app.departure_prompt.delete(0, "end")
        app.departure_prompt.insert(0, f"{departure_airport_value}")

    update_metar("departure")

    min_hour = app.min_hour_prompt.get()
    min_minute = app.min_minute_prompt.get()

    max_hour = app.max_hour_prompt.get()
    max_minute = app.max_minute_prompt.get()

    if min_minute == "":
        min_minute = "30"
        app.min_minute_prompt.set("30")
    if min_hour == "":
        min_hour = "00"
        app.min_hour_prompt.set("00")

    if max_hour == "":
        max_hour = "00"
        app.max_hour_prompt.set("00")

    if max_minute == "":
        max_minute = "30"
        app.max_minute_prompt.set("30")
        max_hour = "02"
        app.max_hour_prompt.set("02")

    min_time = f"{min_hour}:{min_minute}"
    max_time = f"{max_hour}:{max_minute}"

    speed = int(app.speed_prompt.get())

    min_distance = calculate_distance_from_timecode(speed, min_time)
    max_distance = calculate_distance_from_timecode(speed, max_time)

    app.program_output.configure(text=f"Finding airports between {min_time} ({min_distance}nm) and {max_time} ({max_distance}nm) from {departure_airport[0].ident}")

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(get_airports_within_limits, departure_airport, min_distance, max_distance)
    future.add_done_callback(handle_result)

def metar_thread(airport, phase):
    metar_json = get_metar(airport)
    if metar_json:
        station_data = metar_json[0]
        raw_metar = station_data.get('rawOb')
        flt_cat = station_data.get('fltCat')

        if phase == "departure":
            app.departure_metar_display.configure(text=raw_metar)
            app.departure_metar_category_label.configure(text=f"Category: {flt_cat}")
        else:
            app.arrival_metar_display.configure(text=raw_metar)
            app.arrival_metar_category_label.configure(text=f"Category: {flt_cat}")
    else:
        if phase == "departure":
            app.departure_metar_display.configure(text=f"No current data available for {airport[0].ident}")
            app.departure_metar_category_label.configure(text="Category: N/A")
        else:
            app.arrival_metar_display.configure(text=f"No current data available for {airport[0].ident}")
            app.arrival_metar_category_label.configure(text="Category: N/A")

def update_metar(phase):
    def set_time_distance(airport):
        if app.departure_prompt.get() != "":
            departure_airport_id = get_airport_id(airports, app.departure_prompt.get().strip())
            departure_airport = get_airport_info(departure_airport_id)
            distance = get_distance(float(departure_airport[0].lat), float(departure_airport[0].long), float(airport[0].lat), float(airport[0].long))
            hour, minute = distance_to_time(distance, int(app.speed_prompt.get()))
            time = f"{hour}:{minute}"
            app.flight_time_label.configure(text=f"{time}")
            app.arrival_distance_label.configure(text=f"{int(distance)}nm")

    airport = ""
    if phase == "departure" and app.departure_prompt.get():
        app.departure_metar_display.configure(text="Fetching METAR")
        airport = get_airport_info(get_airport_id(airports, app.departure_prompt.get().strip()))

        app.departure_airport_info.configure(text=f"{airport[0].name}, {airport[0].municipality} {airport[1].name}")
        app.departure_elevation_label.configure(text=f"Elevation: {airport[0].elev} ft")
        update_location(app.departure_time_label, app.departure_prompt.get())

        if str(airport[0].iata) == "0":
            if str(airport[0].local_code) != 0:
                label_string = f"{airport[0].local_code}"
            elif str(airport[0].gps_code) != 0:
                label_string = f"{airport[0].gps_code}"
            elif str(airport[0].icao) != 0:
                label_string = f"{airport[0].icao}"
            elif str(airport[0].ident) != 0:
                label_string = f"{airport[0].ident}"
            else:
                label_string = "---"

            app.departure_iata_label.configure(text=label_string)
        else:
            app.departure_iata_label.configure(text=f"{airport[0].iata}")
    elif phase == "arrival" and app.arrival_prompt.get():
        app.arrival_metar_display.configure(text="Fetching METAR")
        airport = get_airport_info(get_airport_id(airports, app.arrival_prompt.get().strip()))

        set_time_distance(airport)
        app.arrival_airport_info.configure(text=f"{airport[0].name}, {airport[0].municipality} {airport[1].name}")
        app.arrival_elevation_label.configure(text=f"Elevation: {airport[0].elev} ft")
        update_location(app.arrival_time_label, app.arrival_prompt.get())

        if str(airport[0].iata) == "0":
            if str(airport[0].local_code) != 0:
                label_string = f"{airport[0].local_code}"
            elif str(airport[0].gps_code) != 0:
                label_string = f"{airport[0].gps_code}"
            elif str(airport[0].icao) != 0:
                label_string = f"{airport[0].icao}"
            elif str(airport[0].ident) != 0:
                label_string = f"{airport[0].ident}"
            else:
                label_string = "---"

            app.arrival_iata_label.configure(text=label_string)
        else:
            app.arrival_iata_label.configure(text=f"{airport[0].iata}")

    if airport:
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(metar_thread, airport, phase)
        future.add_done_callback(lambda f: "")
    else:
        phrase = "Wrong ICAO code or airport has no METAR"
        if phase == "departure":
            app.departure_metar_display.configure(text=phrase)
        else :
            app.arrival_metar_display.configure(text=phrase)


def update_aircraft():
    for aircraft, data in AIRCRAFTS.items():
        if app.aircraft_selector.get() == aircraft:
            app.speed_prompt.delete(0, "end")
            app.speed_prompt.insert(0, f"{data.get("speed")}")
            app.runway_length_prompt.delete(0, "end")
            app.runway_length_prompt.insert(0, f"{data.get("length")}")

def update_location(clock_label, location_prompt):
    global after_id

    if location_prompt != "utc":
        airport = get_airport_info(get_airport_id(airports, str(location_prompt).strip()))
        new_location = f"{airport[0].municipality}, {airport[1].name}"
    else:
        new_location = str(location_prompt)

    timezone = find_timezone_from_input(new_location)
    if timezone:
        app.after_cancel(str(after_id))
        update_clock(clock_label, timezone)

def update_clock(clock_label, new_location="local"):
    global after_id
    if new_location == "local" or new_location == "":
        now = datetime.now().astimezone()
        formatted_time = now.strftime("%H:%M")
    elif new_location == "utc":
        utc_struct = time.gmtime()
        day_number = datetime.now(timezone.utc).strftime("%d")
        formatted_time = time.strftime("%H:%M", utc_struct)
        formatted_time = f"{day_number} {formatted_time}"
    else:
        zone_info = datetime.now(ZoneInfo(new_location))
        formatted_time = zone_info.strftime("%H:%M")

    if new_location != "utc":
        clock_string = f"Local Time: {formatted_time}"
    else:
        clock_string = f"{formatted_time}Z"

    clock_label.configure(text=clock_string)
    after_id = app.after(1000, update_clock, clock_label, new_location)

if __name__ == "__main__":
    after_id = ""
    airports = initialize_airports()
    countries = initialize_country()
    runways = initialize_runway()

    app = App()
    update_clock(app.utc_clock_label, "utc")
    update_aircraft()
    app.aircraft_selector.set(app.aircraft_select_options[0])

    app.mainloop()
