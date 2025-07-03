import pandas as pd

hotel_df = pd.read_csv("hotels.csv")
credit_card_dict = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
card_security_df = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = hotel_df.loc[hotel_df["id"] == self.hotel_id, "name"].squeeze()
        self.city = hotel_df.loc[hotel_df["id"] == self.hotel_id, "city"].squeeze()

    def available(self):
        availability = hotel_df.loc[hotel_df["id"] == self.hotel_id, "available"].squeeze()
        if availability.lower().strip() == "yes":
            return True
        else:
            return False

    def book(self):
        # Booking a hotel makes it unavailable
        hotel_df.loc[hotel_df["id"] == self.hotel_id, "available"] = "no"
        hotel_df.to_csv("hotels.csv", index=False)


class SpaHotel(Hotel):
    def book(self):
        return


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


class SpaTicket:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def generate(self):
        return(f"""Thank you for your Spa Reservation
        Here is your Spa Reservation Details:
        Name: {self.name}
        Spa Location: {self.location}""")


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, cvc, expiry, name):
        card_data = {"number": self.number, "expiration": expiry, "holder": name, "cvc": cvc}
        if (card_data in credit_card_dict):
            return True
        return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = card_security_df.loc[card_security_df["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        return False


class User:
    pass


def add_spa_package(name, location):
    user_selection = input("Would you like to add a Spa Package y/n?")
    if (user_selection == 'y'):
        spa_res = SpaTicket(name, location)
        print(spa_res.generate())
    else:
        return

while True:
    print(hotel_df)
    try:
        selected_hotel = int(input("Enter the ID of the hotel you'd like to book: "))
        hotel = Hotel(selected_hotel)
    except:
        print("Non valid response.  Try again")
        continue

    if hotel.available():
        name = input("Enter your full name: ").strip().upper()
        credit_card_number = input("Enter your Credit Card Number: ")
        credit_card_expiry = input("Enter the expiry date (##/##): ")
        credit_card_cvc = input("Enter the CVC: ")
        credit_card_password = input("Enter the security password: ")
        credit_card = SecureCreditCard(credit_card_number)
        if(credit_card.validate(cvc=credit_card_cvc, expiry=credit_card_expiry, name=name)):
            if (credit_card.authenticate(credit_card_password)):
                hotel.book()
                reservation_ticket = ReservationTicket(name, hotel)
                print(reservation_ticket.generate())
                add_spa_package(name, hotel.name)
                break
            else:
                print("Your credit card could not be authenticated")
        else:
            print("Your credit card could not be validated")
    else:
        print("Hotel is not available")