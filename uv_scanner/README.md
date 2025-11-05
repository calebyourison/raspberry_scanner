# uv_scanner
---

Once `uv` is [installed](https://docs.astral.sh/uv/getting-started/installation/) and the folder "uv_scanner" is copied to your device, you can run the script with `uv run`

The script is looking for two variables: a path to save the file, and a name for your present location.

You can navigate into the directory or use its absolute path and chain everything into a one-liner:

```bash

    # Path to script                                    # Path to save file      # Location of scan      
cd /home/raspberry/Desktop/uv_scanner && uv run main.py /home/raspberry/Desktop/ Living_Room

```

As currently configured, this will save the file locally and present two plots in your browser: one for 2.4 GHz networks and one for 5 GHz networks.

If your scan returns zero results it will continue to try until something is found, so this could potentially result in an infinite loop if run in an area with no wireless activity.

For best results, temporarily disconnect from any wireless networks prior to scanning.

Ensure you are using the correct wireless interface and designate it explicitly if needed.  By default, a Raspberry will present `wlan0`.  USB devices might be `wlan1`.

Modify as needed.  