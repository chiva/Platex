#=============================================================================#
# Author: Santiago Reig                                                       #
# Date:   02.12.2011                                                          #
#                                                                             #
# Description: Platex Arduino firmware                                        #
#                                                                             #
#=============================================================================#


#====================================================================#
#  Settings                                                          #
#====================================================================#
set(FIRMWARE_NAME PlatexFirmata)

set(${FIRMWARE_NAME}_BOARD uno)               # Arduino Target board
set(${FIRMWARE_NAME}_SRCS PlatexFirmata.cpp)  # Firmware sources


#====================================================================#
#  Target generation                                                 #
#====================================================================#
generate_arduino_firmware(${FIRMWARE_NAME})
