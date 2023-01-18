from DataHandler import UserData, GroupData
import ProxyHandler
    

def main() -> None:
    # Read Proxies from Local
    ProxyHandler.read_proxies()
    main_data = UserData("data/users.txt")
    main_data.save_data() # Save the Data
    main_data.write_file()
    # main_data = GroupData(file_name="data/users.txt")
    # main_data.save_data() # Save the Data
    # Compare Two Previous Data



if __name__ == "__main__":
    main()