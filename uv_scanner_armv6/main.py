# 32 bit armv6 workaround

def main():
    import os
    import subprocess
    from parse import compile as parse_compile
    from datetime import datetime
    import csv

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("location")
    parser.add_argument("kuma_url")

    args = parser.parse_args()

    location: str = args.location

    directory: str = args.directory

    filename: str = directory + f"{location} {datetime.now().strftime("%Y-%m-%d_%H-%M")}.csv"

    wireless_interface: str = "get"  # Set explicitly if needed "wlan0" "wlan1" etc


    def get_wireless_interfaces(net_path: str = "/sys/class/net") -> list[str] | None:
        """
        Returns a list of wireless interface names by checking /sys/class/net, or other designated path

        :param net_path: directory for installed network interface
        :type net_path: str

        :return: list of valid wireless interfaces or None if not found
        :rtype: list[str], None
        """

        if not os.path.isdir(net_path):
            print("Invalid interface path")
            return None

        wireless_interfaces: list[str] = []

        for iface in os.listdir(net_path):
            if os.path.isdir(os.path.join(net_path, iface, "wireless")):
                wireless_interfaces.append(iface)

        if len(wireless_interfaces) == 0:
            print("Unable to locate valid wireless interface")
            return None

        else:
            return wireless_interfaces


    def iwlist_command(interface: str = "get") -> str:
        """
        Return raw string text output of command 'iwlist <interface> scan'

        :param interface: name of wireless interface or 'get' to run get_wireless_interfaces()
        :type interface: str

        :return: raw string output of subprocess command
        :rtype: str
        """
        if interface == "get":
            interface_list: list[str] | None = get_wireless_interfaces()
            if interface is None:
                return "No valid interface"
            else:
                interface: str = interface_list[0]

        command: list[str] = ["iwlist", interface, "scan"]

        raw_output: subprocess.CompletedProcess = subprocess.run(
            args=command, stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE
        )

        output_data: str = str(raw_output)

        fail_conditions: list[str] = [
            "Network is down",
            "Interface doesn't support scanning",
            "Failed",
        ]

        for condition in fail_conditions:
            if condition in output_data:
                output_data: str = f"ERROR: {output_data}"
                return output_data

        return output_data


    def get_cells(iwlist_string: str) -> list[str]:
        """
        Return a list of strings from joined lines for each cell in string output of 'iwlist (interface) scan'

        :param iwlist_string: string output of 'iwlist <interface> scan' command
        :type iwlist_string: str

        :return: list of raw strings, one for each cell discovered during scan: empty list if nothing found
        :rtype: list[str]
        """

        cell_lines: list[str] = []

        # Account for escape line variation
        if "\\n" in iwlist_string and "\n" not in iwlist_string:
            iwlist_string = iwlist_string.encode().decode("unicode_escape")

        cells: list[str] = iwlist_string.split("Cell")

        for cell in cells[1:]:
            pieces = cell.splitlines()
            cleaned: str = "+".join([item.strip() for item in pieces])
            cell_lines.append(cleaned)

        return cell_lines


    def parse_cells(cells: list[str]) -> list[dict[str, str]]:
        """
        Parse string outputs of cells and return a list of dictionaries for appropriate keys/values

        :param cells: list of raw strings, one for each cell discovered during scan or None
        :type cells: list[str]

        :return: list of dictionaries with parsed values for appropriate fields
        :rtype: list[dict[str, str]]
        """

        output: list[dict[str, str]] = []

        cell_template: str = (
            "{cell} - Address: {mac}+"
            "Channel:{channel}+"
            "Frequency:{frequency_GHz} {frequency_info}+"
            "Quality={quality}  Signal level={signal_dBm} dBm+"
            "Encryption key:{encryption_key}+"
            "ESSID:{essid}+"
            "{remaining_info}"
        )

        compiled_cell_template = parse_compile(cell_template)


        for line in cells:
            parsed_values: dict[str, str] = compiled_cell_template.parse(line).named
            output.append(parsed_values)

        return output


    def add_time_and_location(cells:list[dict[str, str|float|int]], scan_location:str) -> list[dict[str, str]]:
        """Add time and location keys to each dict, drop remaining info"""
        current_time = datetime.now()

        for cell in cells:
            cell["time"] = str(current_time)
            cell["location"] = scan_location
            quality_split = cell["quality"].split('/')
            quality_decimal:float = int(quality_split[0])/int(quality_split[1])
            cell["quality_decimal"] = quality_decimal
            del cell["cell"]
            del cell["remaining_info"]
            del cell["frequency_info"]
            del cell["encryption_key"]

        return cells

    def scan(scan_location:str) -> list[dict[str, str]]:
        """Scan/parse"""
        text = iwlist_command(interface=wireless_interface)
        base_cells = get_cells(text)
        parsed_cells = parse_cells(base_cells)
        pre_csv = add_time_and_location(parsed_cells, scan_location)

        return pre_csv

    def retry_scan(attempts: int = 5) -> list[dict[str, str]]:
        """Try n number of times if initial scan produces no results"""
        scan_data = scan(location)

        for attempt in range(1, attempts + 1):
            if len(scan_data) > 0:
                return scan_data
            else:
                print(f"Attempt {attempt} produced an empty scan, retrying")
                scan_data = scan(location)

        print("All attempts produced an empty scan")

        return scan_data

    def write_to_csv(cells: list[dict[str, str|int|float]], csv_path) -> None:
        """Write to a local file"""

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cells[0].keys())
            writer.writeheader()
            writer.writerows(cells)

    data = retry_scan(attempts=5)

    write_to_csv(data, csv_path=filename)

if __name__ == "__main__":
    main()