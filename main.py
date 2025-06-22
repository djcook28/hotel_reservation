import pandas as pd

df = pd.read_csv("hotels.csv")


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.city = df.loc[df["id"] == self.hotel_id, "city"].squeeze()

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability.lower().strip() == "yes":
            return True
        else:
            return False

    def book(self):
        # Booking a hotel makes it unavailable
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)


class ReservationTicket:
    def __init__(self, name, hotel_object):
        self.name = name
        self.hotel = hotel_object

    def generate(self):
        print(f"""
        Thank you for your reservation!
        Here is your confirmation:
        Name: {self.name}
        Hotel: {self.hotel.name}
        Address: {self.hotel.city}
        """)


class User:
    pass

print(df)
selected_hotel = int(input("Enter the ID of the hotel you'd like to book: "))
hotel = Hotel(selected_hotel)

if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_ticket = ReservationTicket(name, hotel)
    print(reservation_ticket.generate())