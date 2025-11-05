def main():
    from raspberry_wifi_scanner.data_collection import scan
    from raspberry_wifi_scanner.dataframe_functions import split_by_band
    from raspberry_wifi_scanner.plotting import plot_curves
    from datetime import datetime
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("location")

    args = parser.parse_args()

    location = args.location

    directory = args.directory

    filename = directory + f"{location} {datetime.now().strftime("%Y-%m-%d_%H-%M")}.csv"

    wireless_interface = "get" # Set explicitly if needed "wlan0" "wlan1" etc

    data = scan(interface=wireless_interface, location=location)

    # In case nothing is found
    while data.shape[0] == 0:
        print("Nothing found on scan")
        data = scan(location=location)

    data.to_csv(filename, index=False)
    two_ghz, five_ghz = split_by_band(data)

    two_ghz_networks = plot_curves(two_ghz, "2.4 GHz")
    five_ghz_networks = plot_curves(five_ghz, "5 GHz")

    two_ghz_networks.show()
    five_ghz_networks.show()

if __name__ == "__main__":
    main()

# cd /path/to/uv/project/ && uv run main.py /path/to/save/file/ scan_location