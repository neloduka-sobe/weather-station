# weather-station
Station measuring light intensity and wind speed build on raspberry pi

![Photo of the weather station without sealing](https://github.com/neloduka-sobe/weather-station/blob/main/photo.jpg?raw=true)
Photo of the weather station without sealing

### Setting up
**Linux**

To download programs and make them executable 
```
git clone https://github.com/neloduka-sobe/weather-station.git
chmod +x wind_speed.py light_intensity.py
```
To run scripts every reboot add those lines to crontab using `crontab -e`
```
@reboot /path/to/weather-station/wind_speed.py <GPIO pin> </path/to/csvfile>
@reboot /path/to/weather-station/light_intensity.py <GPIO pin_a> <GPIO pin_b> </path/to/csvfile>
```

### Usage
To run programs in command line use:
```
./light_intensity.py <GPIO pin_a> <GPIO pin_b> </path/to/csvfile>
./wind_speed.py <GPIO pin> </path/to/csvfile>
```
or
```
python3 light_intensity.py <GPIO pin_a> <GPIO pin_b> </path/to/csvfile>
python3 wind_speed.py <GPIO pin> </path/to/csvfile>
```
To  run in debug mode add debug option like so
```
python3 light_intensity.py <GPIO pin_a> <GPIO pin_b> </path/to/csvfile> debug
python3 wind_speed.py <GPIO pin> </path/to/csvfile> debug
```
