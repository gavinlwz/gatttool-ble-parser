# gatttool-ble-parser
Gatttool is fantastic for reading BLE devices. It gets all of the raw input and output that a user could ever want.   
However, I believe that it can be even better for BLE! With the  <a href = "https://www.bluetooth.com/specifications/bluetooth-core-specification">specificiations </a> 
being needed in order to understand the IoT device, I thought it would be nice to have a few scripts to get a better understanding what is going on! 

## gattFinder.py 
This file takes in either a characteristics file or a primary file, which have slightly different outputs. From here, the script will compare all of the uuids and gather information about 
what is going on! Even if properties are not listed, it will at least for a unique uuid for the company that created the spec, allowing for further research to be conducted. 
 
## Useful Scipts 
In the process of writing the parser script for the different specifications, I also found it useful to change 
all of the values from hex to ascii. So, **decode.sh** is for that. Further, **hexToDecimal** changes all 
hex characters into their decimal equivalent. This is useful for settings values. 

## Files
Primary.txt and characteristics.txt are sample outputs that are from gatttool that I used to create this. 

# Happy Hacking! 
Feel free to make a PR to change something or use this! 
