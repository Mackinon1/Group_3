# Bolt.py
import Backend

def main():
    print("="*50)
    print(" Group 3 Ride Hailer")
    print("="*50)

    while True:
        print("\nChoose user type:")
        print("1 - Passenger")
        print("2 - Driver")
        print("3 - Admin")
        print("4 - Engineer")
        print("5 - Exit")

        choice = input("Enter option: ").strip()

        if choice == "1":
            Backend.passenger(
                Backend.drivers_list,
                Backend.passengers_list,
                Backend.locations_coords
            )
        elif choice == "2":
            Backend.driver(
                Backend.drivers_list,
                Backend.passengers_list,
                Backend.locations_coords
            )
        elif choice == "3":
            Backend.admin(Backend.passengers_list, 
                          Backend.drivers_list, 
                          Backend.base_stations
                          )
        elif choice == "4":
            Backend.engineer(
                Backend.base_stations
            )
        elif choice == "5":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
