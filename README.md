# ECU Simulator

This Python tool simulates some vehicle diagnostic services.  

## Supported Services

### OBD-II

| Service | PID    |          Description                   |
|:-------:|:-----: |:---------------------------------------|
| 0x01    | 0x00   | List of supported PIDs in service 0x01 |
| 0x01    | 0x05   | Engine coolant temperature |
| 0x01    | 0x0D   | Vehicle speed |
| 0x01    | 0x2F   | Fuel tank level input |
| 0x01    | 0x51   | Fuel type |
| 0x03    | -      | Request DTCs |
| 0x09    | 0x00   | List of supported PIDs in service 0x09 |
| 0x09    | 0x02   | Vehicle Identification Number (VIN) |
| 0x09    | 0x0A   | ECU name |

### UDS

| Service |          Description                                   |
|:-------:|:-------------------------------------------------------|
| 0x10    | ECUReset. Reset types: 0x01, 0x02, 0x03, 0x04 and 0x05 |

## Addressing

**OBD:** Functional. See options `obd_broadcast_address` and `obd_ecu_address` in `ecu_config.json`.

**UDS:** Physical. See option `obd_ecu_address` in `ecu_config.json`.

## Requirements 

## Test Environment  

## Usage 

The ecu-simulator try to set up the CAN interface and load the ISO-TP linux kernel module (you need to configure `can_interface`, `can_interface_type`, `can_bitrate`, and `isotp_ko_file_path` in `ecu_config.json`). To perform this task, the tool must be started with root privileges:   

`sudo python3 ecu-simulator.py`

If you do not want to start the tool with root privileges, you can do the following:

```
# set up CAN hardware interface
sudo sh can_setup.sh

# or set up CAN virtual interface 
sudo sh vcan_setup.sh

# and then start the tool without sudo
python3 ecu-simulator.py
``` 




