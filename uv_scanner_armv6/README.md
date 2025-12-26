# uv_scanner on armv6
---

**Variants of Raspberry Pi running on armv6 32 bit can sometimes present challenges for package installation.
This workaround falls back to the lightweight `parse` library and will save a .csv file to a local directory
for use on a different machine that can perform analysis and plotting.
Designed for headless installations that are only collecting periodic data.**

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

Copy the folder to your device and unzip.
 ```bash
curl -L -o uv_scanner_armv6.zip https://github.com/calebyourison/raspberry_scanner/releases/download/uv_scanner_armv6/uv_scanner_armv6.zip

unzip uv_scanner_armv6.zip
 ```

You can run the script with `uv run`.

The script is looking for two variables: a path to save the file, and a name for your present location.

You can navigate into the directory or use its absolute path and chain everything into a one-liner:

```bash

    # Path to script folder                             # Path to save file      # Location of scan      
cd /home/raspberry/Desktop/uv_scanner && uv run main.py /home/raspberry/Desktop/ Living_Room

```

As currently configured, this will save the .csv file locally but will not display any plots.

It will run a total of 5 scan attempts until at least one network is found.

For best results, temporarily disconnect from any wireless networks prior to scanning.

Ensure you are using the correct wireless interface and designate it explicitly if needed.  By default, a Raspberry will present `wlan0`.  USB devices might be `wlan1`.

Modify as needed.  