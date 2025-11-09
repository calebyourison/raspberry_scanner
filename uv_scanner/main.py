def main():
    from raspberry_wifi_scanner.data_collection import scan
    from raspberry_wifi_scanner.dataframe_functions import split_by_band
    from raspberry_wifi_scanner.plotting import plot_curves
    import pandas as pd
    from datetime import datetime
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("location")

    args = parser.parse_args()

    location: str = args.location

    directory: str = args.directory

    filename: str = directory + f"{location} {datetime.now().strftime("%Y-%m-%d_%H-%M")}.csv"

    wireless_interface: str = "get" # Set explicitly if needed "wlan0" "wlan1" etc

    def retry_scan(attempts: int = 5) -> pd.DataFrame:
        """Retry n times if scan yields zero rows"""
        scan_data: pd.DataFrame = scan(interface=wireless_interface, location=location)

        for attempt in range(1, attempts + 1):
            if scan_data.shape[0] > 0:
                return scan_data
            else:
                print(f"Attempt {attempt} produced an empty scan, retrying")
                scan_data: pd.DataFrame = scan(interface=wireless_interface, location=location)

        print("All attempts produced an empty scan")

        return scan_data

    data: pd.DataFrame = retry_scan(attempts=5)

    data.to_csv(filename, index=False)
    two_ghz, five_ghz = split_by_band(data)

    two_ghz_networks = plot_curves(two_ghz, "2.4 GHz")
    five_ghz_networks = plot_curves(five_ghz, "5 GHz")

    two_ghz_networks.show()
    five_ghz_networks.show()

if __name__ == "__main__":
    main()

# cd /path/to/uv/project/ && uv run main.py /path/to/save/file/ scan_location