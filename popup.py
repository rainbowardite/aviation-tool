import customtkinter as ctk
from distance import calculate_distance_from_timecode
from helpers import distance_to_time, get_airport_info

class ScrollablePopup(ctk.CTkToplevel):
    def __init__(self, parent, elegible_airport_ids, distances, speed):
        super().__init__(parent)

        self.title("Potential Airports")
        self.geometry("800x800")

        self.after(250, lambda: self.focus())
        #self.grab_set() removed to make base app interactable

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, width=380, height=250)
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox._textbox.configure(spacing3=8)
        self.display_airports(elegible_airport_ids, distances, speed)

        self.close_button = ctk.CTkButton(self, text="Dismiss", command=self.destroy)
        self.close_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def sort_by_distance(self, ids, distances):
        paired_data = zip(distances, ids)
        sorted_pairs = sorted(paired_data)
        sorted_distances = [d for d, i in sorted_pairs]
        sorted_ids = [i for d, i in sorted_pairs]
        return sorted_ids, sorted_distances

    def display_airports(self, elegible_airport_ids, distances, speed):
        if len(elegible_airport_ids) > 0:
            elegible_airport_ids, distances = self.sort_by_distance(elegible_airport_ids, distances)
            for index, id in enumerate(elegible_airport_ids):
                distance = distances[index]
                hours, minutes = distance_to_time(distance, int(speed))
                potential_arrival_airport = get_airport_info(id)
                time = f"{hours}:{minutes}"
                line_text = f"{(index + 1)}: {potential_arrival_airport[0].ident}, {potential_arrival_airport[0].name}, {potential_arrival_airport[0].municipality}, {potential_arrival_airport[1].name}, {potential_arrival_airport[3].length}ft, {int(distance)}nm, {time}\n"
                self.textbox.insert("end", line_text)

            self.textbox.configure(state="disabled")
