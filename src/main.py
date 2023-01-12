from UserHandler import DataHandler
import ProxyHandler
    

def main() -> None:
    # Read Proxies from Local
    ProxyHandler.read_proxies()
    main_data = DataHandler("myths.txt")
    main_data.save_data() # Save the Data
    # Compare Two Previous Data



if __name__ == "__main__":
    main()