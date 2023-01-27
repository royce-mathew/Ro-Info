from DataHandler import UserData, GroupData
import ProxyHandler
import DataHandler.Util as util;
    

def main() -> None:
    # Read Proxies from Local
    ProxyHandler.read_proxies()
    main_data = UserData("data/users.txt")
    main_data.save_data() # Save the Data
    # main_data.write_file("data/all_users.txt")
    rest_users = main_data.compare_data()
    util.write_list(rest_users, "data/rest_users.txt")

    # main_data = GroupData(file_name="data/users.txt")
    # main_data.save_data() # Save the Data
    # Compare Two Previous Data



if __name__ == "__main__":
    main()