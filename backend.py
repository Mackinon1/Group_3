import random
import math
import time
import pandas as pd

# ----------------------------
# Simulation speed
# ----------------------------
SIMULATION_STEP = 0.2

# ----------------------------
# Locations dictionary
# ----------------------------
locations_coords = {
    "Kisumu": (10, 20),
    "Nyeri": (50, 75),
    "Juja": (70, 40),
    "Nairobi": (90, 10),
    "Mombasa": (95, 95)
}

# ----------------------------
# Helper functions
# ----------------------------
def distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def get_valid_input(prompt, cast_type=str, condition=lambda x: True, error_msg="Invalid input."):
    while True:
        try:
            value = cast_type(input(prompt).strip())
            if not condition(value):
                print(error_msg)
                continue
            return value
        except ValueError:
            print(error_msg)

def select_location(prompt):
    while True:
        loc_name = input(prompt).strip()
        if loc_name in locations_coords:
            return locations_coords[loc_name]
        print(f"Invalid location. Options: {', '.join(locations_coords.keys())}")

# ----------------------------
# User classes
# ----------------------------
class User:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print(f"Hello, {self.name}")

class Passenger(User):
    def __init__(self, name, age, gender, national_id, current_location, destination):
        super().__init__(name)
        self.age = age
        self.gender = gender
        self.national_id = national_id
        self.current_location = current_location
        self.destination = destination
        self.ride_history = []

class Driver(User):
    def __init__(self, name, age, national_id, license_number,
                 car_reg_number, car_model, car_seats, car_color, current_location):
        super().__init__(name)
        self.age = age
        self.national_id = national_id
        self.license_number = license_number
        self.car_reg_number = car_reg_number
        self.car_model = car_model
        self.car_seats = car_seats
        self.car_color = car_color
        self.current_location = current_location
        self.available = False
        self.on_trip = False
        self.speed = random.randint(5, 15)
        self.ride_history = []

class Admin(User):
    def __init__(self, name, access_code):
        super().__init__(name)
        self.access_code = access_code
    def authenticate(self):
        return self.access_code == "1234"

class Engineer(User):
    def __init__(self, name, passcode):
        super().__init__(name)
        self.passcode = passcode
    def authenticate(self):
        return self.passcode == "eng123"

# ----------------------------
# Base Station class
# ----------------------------
class BaseStation:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.status = "Active"
        self.connected_drivers = []
        self.connected_passengers = []

# ----------------------------
# Global lists
# ----------------------------
drivers_list = []
passengers_list = []

# ----------------------------
# Base stations
# ----------------------------
base_stations = [
    BaseStation("Aswan Station", locations_coords["Kisumu"]),
    BaseStation("Cairo Station", locations_coords["Nyeri"]),
    BaseStation("Luxor Station", locations_coords["Juja"]),
    BaseStation("Giza Station", locations_coords["Nairobi"]),
    BaseStation("Alexandria Station", locations_coords["Mombasa"])
]

# ----------------------------
# Passenger function
# ----------------------------
def passenger(drivers_list, passengers_list, location_names_map):
    while True:
        try:
            name = input("Enter your name: ").strip()
            age = get_valid_input("Enter your age: ", int, lambda x: x >= 18, "Passenger must be at least 18.")
            gender = input("Enter your gender: ").strip()
            national_id = get_valid_input(
                "Enter your ID number: ",
                str,
                lambda x: x.isdigit() and len(x) <= 8,
                "ID must be numeric with max 8 digits."
            )
            current_location = select_location(f"Enter your current location (options: {', '.join(location_names_map.keys())}): ")
            destination = select_location(f"Enter your destination (options: {', '.join(location_names_map.keys())}): ")

            p = Passenger(name, age, gender, national_id, current_location, destination)
            passengers_list.append(p)
            break
        except ValueError as e:
            print(e)

    p.greet()
    while True:
        print("\nWhat would you like to do?")
        print("1 - Request a ride")
        print("2 - View ride history")
        print("3 - Set a new destination")
        print("4 - Exit")

        action = input("Enter choice (1/2/3/4): ").strip()

        if action == "1":
            available_drivers = [d for d in drivers_list if d.available and not d.on_trip]
            if not available_drivers:
                print("No available drivers at the moment.")
                continue

            closest_driver = min(
                available_drivers,
                key=lambda d: distance(d.current_location, p.current_location)
            )
            print(f"{closest_driver.name} is your chauffeur today.")

            # Approach pickup
            dist = distance(closest_driver.current_location, p.current_location)
            remaining_dist = dist
            while remaining_dist > 0:
                time.sleep(SIMULATION_STEP)
                remaining_dist -= closest_driver.speed * 0.5
                remaining_dist = max(0, remaining_dist)
                eta = remaining_dist / closest_driver.speed
                print(f"Driver {closest_driver.name} is {remaining_dist:.2f} kms away, ETA {eta:.1f} minutes", end="\r")
            print(f"\n{closest_driver.name} has arrived at pickup.")

            # Ride to destination
            dist_to_dest = distance(p.current_location, p.destination)
            remaining_dist = dist_to_dest
            while remaining_dist > 0:
                time.sleep(SIMULATION_STEP)
                remaining_dist -= closest_driver.speed * 0.5
                remaining_dist = max(0, remaining_dist)
                eta = remaining_dist / closest_driver.speed
                print(f"Heading to destination: {remaining_dist:.2f} kms remaining, ETA {eta:.1f} minutes", end="\r")

            dest_name = [k for k,v in location_names_map.items() if v == p.destination][0]
            print(f"\n{p.name}, you have arrived at {dest_name}")

            ride_record = {"Chauffeur": closest_driver.name, "From": p.current_location, "To": p.destination}
            p.ride_history.append(ride_record)
            closest_driver.ride_history.append(ride_record)
            closest_driver.current_location = p.destination
            p.current_location = p.destination

        elif action == "2":
            print("\n--- Ride History ---")
            if not p.ride_history:
                print("No rides yet.")
            else:
                for ride in p.ride_history:
                    start_name = [k for k,v in location_names_map.items() if v == ride["From"]]
                    end_name = [k for k,v in location_names_map.items() if v == ride["To"]]
                    print(f"From {start_name[0] if start_name else ride['From']} to {end_name[0] if end_name else ride['To']} with {ride['Chauffeur']}")
        elif action == "3":
            new_dest = select_location(f"Enter new destination (options: {', '.join(location_names_map.keys())}): ")
            p.destination = new_dest
            print("Destination updated.")
        elif action == "4":
            break
        else:
            print("Invalid choice, try again.")

# ----------------------------
# Driver function
# ----------------------------
def driver(drivers_list, passengers_list, location_names_map):
    while True:
        try:
            name = input("Enter your name: ").strip()
            age = get_valid_input("Enter your age: ", int, lambda x: 21 <= x <= 60, "Driver age must be between 21 and 60.")
            national_id = get_valid_input(
                "Enter your ID number: ",
                str,
                lambda x: x.isdigit() and len(x) <= 8,
                "ID must be numeric with max 8 digits."
            )
            license_number = get_valid_input(
                "Enter your driver license number: ",
                str,
                lambda x: x.isdigit() and len(x) <= 8,
                "License number must be numeric with max 8 digits."
            )
            car_reg = input("Enter your car registration number: ").strip()
            car_model = input("Enter your car model: ").strip()
            car_seats = get_valid_input("Enter your car seats: ", int, lambda x: x > 0, "Seats must be a positive integer.")
            car_color = input("Enter your car color: ").strip()
            current_location = select_location(f"Enter your current location (options: {', '.join(location_names_map.keys())}): ")

            d = Driver(name, age, national_id, license_number, car_reg, car_model, car_seats, car_color, current_location)
            drivers_list.append(d)
            break
        except ValueError as e:
            print(e)

    d.greet()
    while True:
        print("\nWhat would you like to do?")
        print("1 - Go online")
        print("2 - View ride history")
        print("3 - Exit")

        action = input("Enter choice: ").strip()

        if action == "1":
            available_passengers = [p for p in passengers_list if p.current_location != p.destination]
            if not available_passengers:
                print("No passengers available at the moment.")
                continue

            assigned_passenger = random.choice(available_passengers)

            pickup_name = [k for k,v in locations_coords.items() if v == assigned_passenger.current_location][0]
            destination_name = [k for k,v in locations_coords.items() if v == assigned_passenger.destination][0]

            print(f"Assigned passenger: {assigned_passenger.name}, Pick up: {pickup_name}, Destination: {destination_name}")

            # Approach pickup
            dist = distance(d.current_location, assigned_passenger.current_location)
            remaining_dist = dist
            while remaining_dist > 0:
                time.sleep(SIMULATION_STEP)
                remaining_dist -= d.speed * 0.5
                remaining_dist = max(0, remaining_dist)
                eta = remaining_dist / d.speed
                print(f"Distance to passenger: {remaining_dist:.2f} kms, ETA {eta:.1f} minutes", end="\r")
            print(f"\n{assigned_passenger.name} has arrived at pickup.")

            # Ride to destination
            dist_to_dest = distance(assigned_passenger.current_location, assigned_passenger.destination)
            remaining_dist = dist_to_dest
            while remaining_dist > 0:
                time.sleep(SIMULATION_STEP)
                remaining_dist -= d.speed * 0.5
                remaining_dist = max(0, remaining_dist)
                eta = remaining_dist / d.speed
                print(f"Heading to destination: {remaining_dist:.2f} kms remaining, ETA {eta:.1f} minutes", end="\r")
            print(f"\n{assigned_passenger.name}, you have delivered {assigned_passenger.name} to {destination_name}")

            ride_record = {"Passenger": assigned_passenger.name, "From": assigned_passenger.current_location, "To": assigned_passenger.destination}
            assigned_passenger.ride_history.append(ride_record)
            d.ride_history.append(ride_record)
            d.current_location = assigned_passenger.destination
            assigned_passenger.current_location = assigned_passenger.destination

        elif action == "2":
            print("\n--- Ride History ---")
            if not d.ride_history:
                print("No rides yet.")
            else:
                for ride in d.ride_history:
                    print(f"Passenger: {ride['Passenger']} From {ride['From']} To {ride['To']}")
        elif action == "3":
            break
        else:
            print("Invalid choice. Try again.")

# ----------------------------
# Admin function
# ----------------------------
def admin(passengers_list, drivers_list, base_stations):
    username = input("Enter admin username: ").strip()
    password = input("Enter admin passcode: ").strip()
    a = Admin(username, password)
    if not a.authenticate():
        print("Access denied!")
        return
    a.greet()

    while True:
        print("\nAdmin options:")
        print("1 - Passengers")
        print("2 - Drivers")
        print("3 - Base Stations")
        print("4 - Exit")

        action = input("Enter choice: ").strip()
        if action == "1":
            print("\n1 - List all passengers\n2 - Search passenger by name")
            sub = input("Enter choice: ").strip()
            if sub == "1":
                if not passengers_list:
                    print("No passengers registered.")
                else:
                    df = pd.DataFrame([{
                        "Name": p.name,
                        "Age": p.age,
                        "Gender": p.gender,
                        "ID": p.national_id,
                        "Current Location": [k for k,v in locations_coords.items() if v==p.current_location][0],
                        "Destination": [k for k,v in locations_coords.items() if v==p.destination][0]
                    } for p in passengers_list])
                    print(df)
            elif sub == "2":
                search_name = input("Enter passenger name to search: ").strip()
                found = [p for p in passengers_list if p.name.lower() == search_name.lower()]
                if not found:
                    print("Passenger not found.")
                else:
                    p = found[0]
                    df = pd.DataFrame([{
                        "Name": p.name,
                        "Age": p.age,
                        "Gender": p.gender,
                        "ID": p.national_id,
                        "Current Location": [k for k,v in locations_coords.items() if v==p.current_location][0],
                        "Destination": [k for k,v in locations_coords.items() if v==p.destination][0]
                    }])
                    print(df)
            else:
                print("Invalid option.")

        elif action == "2":
            print("\n1 - All driver info\n2 - Active drivers only")
            sub = input("Enter choice: ").strip()
            if sub == "1":
                if not drivers_list:
                    print("No drivers registered.")
                else:
                    df = pd.DataFrame([{
                        "Name": d.name,
                        "Age": d.age,
                        "ID": d.national_id,
                        "License": d.license_number,
                        "Car": f"{d.car_color} {d.car_model} ({d.car_reg_number})",
                        "Seats": d.car_seats,
                        "Available": d.available,
                        "On Trip": "Yes" if d.on_trip else "No",
                        "Town": [k for k,v in locations_coords.items() if v==d.current_location][0]
                    } for d in drivers_list])
                    print(df)
            elif sub == "2":
                active_drivers = [d for d in drivers_list if d.available]
                if not active_drivers:
                    print("No active drivers.")
                else:
                    df = pd.DataFrame([{
                        "Name": d.name,
                        "Available": d.available,
                        "On Trip": "Yes" if d.on_trip else "No",
                        "Town": [k for k,v in locations_coords.items() if v==d.current_location][0]
                    } for d in active_drivers])
                    print(df)
            else:
                print("Invalid option.")

        elif action == "3":
            # Show base station info
            data = []
            for bs in base_stations:
                town_name = [k for k,v in locations_coords.items() if v == bs.location]
                data.append({
                    "Name": bs.name,
                    "Location": town_name[0] if town_name else bs.location,
                    "Status": bs.status,
                    "Connected Drivers": len(bs.connected_drivers),
                    "Connected Passengers": len(bs.connected_passengers)
                })
            print(pd.DataFrame(data))

        elif action == "4":
            break
        else:
            print("Invalid choice.")

# ----------------------------
# Engineer function
# ----------------------------
def engineer(base_stations):
    username = input("Enter engineer username: ").strip()
    passcode = input("Enter engineer passcode: ").strip()
    eng = Engineer(username, passcode)
    if not eng.authenticate():
        print("Access denied!")
        return
    print(f"\nWelcome Engineer {eng.name}!")

    while True:
        print("\nEngineer options:")
        print("1 - View all base stations info")
        print("2 - Search base station by name")
        print("3 - Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            data = []
            for bs in base_stations:
                town_name = [k for k, v in locations_coords.items() if v == bs.location]
                data.append({
                    "Name": bs.name,
                    "Location": town_name[0] if town_name else bs.location,
                    "Status": bs.status,
                    "Connected Drivers": len(bs.connected_drivers),
                    "Connected Passengers": len(bs.connected_passengers)
                })
            print(pd.DataFrame(data))

        elif choice == "2":
            search_name = input("Enter base station name to search: ").strip()
            matched = [bs for bs in base_stations if bs.name.lower() == search_name.lower()]
            if matched:
                bs = matched[0]
                town_name = [k for k, v in locations_coords.items() if v == bs.location]
                print(pd.DataFrame([{
                    "Name": bs.name,
                    "Location": town_name[0] if town_name else bs.location,
                    "Status": bs.status,
                    "Connected Drivers": len(bs.connected_drivers),
                    "Connected Passengers": len(bs.connected_passengers)
                }]))
            else:
                print("Base station not found.")

        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")
