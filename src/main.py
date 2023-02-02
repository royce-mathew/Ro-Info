from DataHandler import UserData, GroupData
import ProxyHandler
import DataHandler.Util as util;
import Compare;

def main() -> None:
    # Read Proxies from Localunchecked_users
    ProxyHandler.read_proxies()
    main_data = UserData("data/unchecked_users.txt")
    # main_data.save_data() # Save the Data / Write to output json
    main_data.save_csv() # Append New Data

    # user_json = main_data.get_data() # get user_data
    # chart_points = Compare.get_comparisons(user_json, 0); # Calculate the chart points
    # # util.save_json(chart_points, "data/comparisons.json"); # Save the comparisons in a json file
    # util.write_csv(chart_points, "data/comparisons.csv"); # Save comparisons in a csv file

    # Store unchecked users
    unchecked = main_data.store_unchecked()
    util.write_list(unchecked, "data/unchecked_users.txt")

    # main_data = GroupData(file_name="data/users.txt")
    # main_data.save_data() # Save the Data
    # Compare Two Previous Data



if __name__ == "__main__":
    main()