# GPU-Z Log Exporter
It's a Prometheus exporter for GPU stats logged by GPU-Z to a file. I did it because I couldn't find any other exporter or even functionality in publicly available tools and APIs such as nvidia-smi to get all of the data that GPU-Z can get (stuff such as Hot Spot temperature and power draw for each PCIE connector separately)


## Prerequisites

- Prometheus
- GPU-Z
- .NET Framework (for relaunching GPU-Z after the log file gets too big, cause I couldn't get it to work well enouch with just python subprocesses)
- Python (I have written this in Python 3.9 and haven't tested previous versions, so it would be ideal to use this version, but it probably will run on anything above 3.5)
- Few python packages

To install dependencies in your environment run:

```bash
$ pip3 install -r requirements.txt
```

## How to run
Unpack release in your target folder, make shortcut to the **exporter.pyw** file and add it to your autostart.

You can add an **.env** file to target folder to change some global variables:  

ENV variable    | Description                                                                                           | Default value
------------    | -------------                                                                                         | -------------
PORT            | Port on which the exporter will be listening.                                                         | 7777
MAX_SIZE        | Maximal size of the log file before restarting.                                                       | 1_200_000_000
FILE_PATH       | Path of your GPU-Z log file. Make sure you have write permissions.                                    | "GPU-Z Sensor Log.txt"
GPUZ_PATH       | Path of the **RunGPU-Z.exe** file in case you want it in different location.                          | "RunGPU-Z.exe"
RESRT_TIME      | Time of the daily log file reset in %H:%M:%S format (not required, does not happen if not specified)  | None
    
You shoud have your GPU-Z installed in default location for now.

## Current flaws to be fixed

* When log file size reaches **MAX_SIZE** log file is deleted and GPU-Z is restarted in order to do so. This causes the GPU-Z starting logo to pop up for about 3 seconds, so if you are using any fullscreen 3D application it's going to be minimalized for a few seconds.
* As mentioned earlier currently there is no way to use non-default location for GPU-Z. It's a quick fix so it's going to work soon.
