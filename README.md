# MyEnergi

A small library to work with the MyEnergi API for some simple
data gathering and setting.

## Prerequisites

To obtain an API key, follow the instructions here: https://support.myenergi.com/hc/en-gb/articles/4404522743313-myenergi-API




## Python use

```
from myenergi import MyEnergi

my_e = MyEnergi("serial_number", "api_key")

first_heater = my_e.myenergi_data.eddi[0]

print(f"Heater Serial is {first_heater.sno}")
print("Boosting!")
first_heater.boost(minutes=10)
first_heater.cancel_boost()
```