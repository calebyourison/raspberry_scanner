# uv_scanner
---

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

Copy the folder to your device and unzip.
 ```bash
curl -L -o uv_scanner.zip https://github.com/calebyourison/raspberry_scanner/releases/download/uv_scanner/uv_scanner.zip

unzip uv_scanner.zip
 ```

You can run the script with `uv run`.

The script is looking for two variables: a path to save the file, and a name for your present location.

You can navigate into the directory or use its absolute path and chain everything into a one-liner:

```bash

    # Path to script                                    # Path to save file      # Location of scan      
cd /home/raspberry/Desktop/uv_scanner && uv run main.py /home/raspberry/Desktop/ Living_Room

```

As currently configured, this will save the file locally and present two plots in your browser: one for 2.4 GHz networks and one for 5 GHz networks.

It will run a total of 5 scan attempts until at least one network is found.

For best results, temporarily disconnect from any wireless networks prior to scanning.

Ensure you are using the correct wireless interface and designate it explicitly if needed.  By default, a Raspberry will present `wlan0`.  USB devices might be `wlan1`.

Modify as needed.  