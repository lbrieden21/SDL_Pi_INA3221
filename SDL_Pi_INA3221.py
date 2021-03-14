#!/usr/bin/env python

# SDL_Pi_INA3221.py Python Driver Code
# SwitchDoc Labs March 4, 2015
# V 1.2


# encoding: utf-8

from gpiozero import Button

import smbus

# constants

# =========================================================================
# I2C ADDRESS/BITS
# -----------------------------------------------------------------------*/
INA3221_ADDRESS = (0x40)  # 1000000 (A0+A1=GND)
INA3221_READ = (0x01)
# =========================================================================*/

# =========================================================================
# CONFIG REGISTER (R/W)
# -----------------------------------------------------------------------*/
INA3221_REG_CONFIG = (0x00)
# /*---------------------------------------------------------------------*/
INA3221_CONFIG_RESET = (0x8000)  # Reset Bit

INA3221_CONFIG_ENABLE_CHAN1 = (0x4000)  # Enable Channel 1
INA3221_CONFIG_ENABLE_CHAN2 = (0x2000)  # Enable Channel 2
INA3221_CONFIG_ENABLE_CHAN3 = (0x1000)  # Enable Channel 3

INA3221_CONFIG_AVG2 = (0x0800)  # AVG Samples Bit 2 - See table 3 spec
INA3221_CONFIG_AVG1 = (0x0400)  # AVG Samples Bit 1 - See table 3 spec
INA3221_CONFIG_AVG0 = (0x0200)  # AVG Samples Bit 0 - See table 3 spec

INA3221_CONFIG_VBUS_CT2 = (0x0100)  # VBUS bit 2 Conversion time - See table 4 spec
INA3221_CONFIG_VBUS_CT1 = (0x0080)  # VBUS bit 1 Conversion time - See table 4 spec
INA3221_CONFIG_VBUS_CT0 = (0x0040)  # VBUS bit 0 Conversion time - See table 4 spec

INA3221_CONFIG_VSH_CT2 = (0x0020)  # Vshunt bit 2 Conversion time - See table 5 spec
INA3221_CONFIG_VSH_CT1 = (0x0010)  # Vshunt bit 1 Conversion time - See table 5 spec
INA3221_CONFIG_VSH_CT0 = (0x0008)  # Vshunt bit 0 Conversion time - See table 5 spec

INA3221_CONFIG_MODE_3 = (0x0004)  # Operating Mode bit 2 - See table 6 spec
INA3221_CONFIG_MODE_2 = (0x0002)  # Operating Mode bit 1 - See table 6 spec
INA3221_CONFIG_MODE_1 = (0x0001)  # Operating Mode bit 0 - See table 6 spec

# =========================================================================*/

# =========================================================================
# SHUNT VOLTAGE REGISTER (R)
# -----------------------------------------------------------------------*/
INA3221_REG_SHUNTVOLTAGE_1 = (0x01)
# =========================================================================*/

# =========================================================================
# BUS VOLTAGE REGISTER (R)
# -----------------------------------------------------------------------*/
INA3221_REG_BUSVOLTAGE_1 = (0x02)
# =========================================================================*/

# =========================================================================
# CRITICAL ALERT LIMIT REGISTER (R/W)
# -----------------------------------------------------------------------*/
INA3221_REG_CRITALERTLIMIT_1 = (0x07)
# =========================================================================*/

# =========================================================================
# WARNING ALERT LIMIT REGISTER (R/W)
# -----------------------------------------------------------------------*/
INA3221_REG_WARNINGALERTLIMIT_1 = (0x08)
# =========================================================================*/

# =========================================================================
# SHUNT VOLTAGE SUM REGISTER (R)
# -----------------------------------------------------------------------*/
INA3221_REG_SHUNTVOLTAGESUM = (0x0D)
# =========================================================================*/

# =========================================================================
# SHUNT VOLTAGE SUM REGISTER LIMIT (R/W)
# -----------------------------------------------------------------------*/
INA3221_REG_SHUNTVOLTAGESUMLIMIT = (0x0E)
# =========================================================================*/

# =========================================================================
# MASK/ENABLE REGISTER (R/W)
# -----------------------------------------------------------------------*/
INA3221_REG_MASKENABLE = (0x0F)
# ---------------------------------------------------------------------*/
INA3221_REG_MASKENABLE_RESERVED = (0x8000)  # Rserved

INA3221_REG_MASKENABLE_SCC1 = (0x4000)  # Summation Channel Control 1
INA3221_REG_MASKENABLE_SCC2 = (0x2000)  # Summation Channel Control 2
INA3221_REG_MASKENABLE_SCC3 = (0x1000)  # Summation Channel Control 3

INA3221_REG_MASKENABLE_WEN = (0x0800)  # Enable Warning Alert Latch
INA3221_REG_MASKENABLE_CEN = (0x0400)  # Enable Critical Alert Latch

INA3221_REG_MASKENABLE_CF1 = (0x0200)  # Critical-alert Flag Indicator 1
INA3221_REG_MASKENABLE_CF2 = (0x0100)  # Critical-alert Flag Indicator 2
INA3221_REG_MASKENABLE_CF3 = (0x0080)  # Critical-alert Flag Indicator 3

INA3221_REG_MASKENABLE_SF = (0x0040)  # Summation-alert Flag Indicator

INA3221_REG_MASKENABLE_WF1 = (0x0020)  # Warning-alert Flag Indicator 1
INA3221_REG_MASKENABLE_WF2 = (0x0010)  # Warning-alert Flag Indicator 2
INA3221_REG_MASKENABLE_WF3 = (0x0008)  # Warning-alert Flag Indicator 3

INA3221_REG_MASKENABLE_PVF = (0x0004)  # Power-valid-alert Flag Indicator
INA3221_REG_MASKENABLE_TCF = (0x0002)  # Timing-control-alert Flag Indicator
INA3221_REG_MASKENABLE_CVRF = (0x0001)  # Conversion-ready Flag
# =========================================================================*/

# =========================================================================
# POWER-VALID UPPER-LIMIT REGISTER (R/W)
# -----------------------------------------------------------------------*/
INA3221_REG_PVUPPER = (0x10)
# =========================================================================*/

# =========================================================================
# POWER-VALID LOWER-LIMIT REGISTER (R/W)
# -----------------------------------------------------------------------*/
INA3221_REG_PVLOWER = (0x11)
# =========================================================================*/

SHUNT_RESISTOR_VALUE = (0.1)  # default shunt resistor value of 0.1 Ohm

INA3221_PIN_PV = 6
INA3221_PIN_CRIT = 13
INA3221_PIN_WARN = 19
INA3221_PIN_TC = 26


class SDL_Pi_INA3221():

    ###########################
    # INA3221 Code
    ###########################
    def __init__(
        self,
        twi=1,
        addr=INA3221_ADDRESS,
        shunt_resistor=SHUNT_RESISTOR_VALUE,
        config=None
    ):
        self._bus = smbus.SMBus(twi)
        self._addr = addr
        self._pv = Button(INA3221_PIN_PV)
        self._crit = Button(INA3221_PIN_CRIT)
        self._warn = Button(INA3221_PIN_WARN)
        self._tc = Button(INA3221_PIN_TC)

        if config is None:
            self._config = self.get_config()
        else:
            self._write_register_little_endian(INA3221_REG_CONFIG, config)
            self._config = config

    def _write(self, register, data):
        self._bus.write_byte_data(self._addr, register, data)

    def _read(self, data):
        returndata = self._bus.read_byte_data(self._addr, data)
        return returndata

    def _read_register_little_endian(self, register):

        result = self._bus.read_word_data(self._addr, register) & 0xFFFF
        lowbyte = (result & 0xFF00) >> 8
        highbyte = (result & 0x00FF) << 8
        switchresult = lowbyte + highbyte
        return switchresult

    def _write_register_little_endian(self, register, data):
        data = data & 0xFFFF
        # reverse configure byte for little endian
        lowbyte = data >> 8
        highbyte = (data & 0x00FF) << 8
        switchdata = lowbyte + highbyte
        self._bus.write_word_data(self._addr, register, switchdata)

    def _get_bus_voltage_raw(self, channel):
        # Gets the raw bus voltage (16-bit signed integer, so +-32767)
        value = self._read_register_little_endian(INA3221_REG_BUSVOLTAGE_1 + (channel - 1) * 2)
        if value > 32767:
            value -= 65536
        return value

    def _get_shunt_voltage_raw(self, channel):
        # Gets the raw shunt voltage (16-bit signed integer, so +-32767)
        value = self._read_register_little_endian(INA3221_REG_SHUNTVOLTAGE_1 + (channel - 1) * 2)
        if value > 32767:
            value -= 65536
        return value

    # public functions

    def reset(self):
        self._write_register_little_endian(INA3221_REG_CONFIG, INA3221_CONFIG_RESET)

    def powerdown(self):
        self.set_config(INA3221_CONFIG_MODE_3)

    def get_config(self):
        value = self._read_register_little_endian(INA3221_REG_CONFIG)
        return value

    def set_config(self, value):
        self._write_register_little_endian(INA3221_REG_CONFIG, value)
        self._config = value

    def print_config(self):
        averagingmodes = [
            '000-1',
            '001-4',
            '010-16',
            '011-64',
            '100-128',
            '101-256',
            '110-512',
            '111-1024',
        ]
        conversiontimes = [
            '000-140 us',
            '001-204 us',
            '010-332 us',
            '011-588 us',
            '100-1.1 ms',
            '101-2.116 ms',
            '110-4.156 ms',
            '111-8.244 ms',
        ]
        operatingmodes = [
            '000-Power down',
            '001-Shunt voltage, single-shot (triggered)',
            '010-Bus voltage, single-shot (triggered)',
            '011-Shunt and bus, single-shot (triggered)',
            '100-Power down',
            '101-Shunt voltage, continuous',
            '110-Bus voltage, continuous',
            '111-Shunt and bus, continuous (default)',
        ]

        configreset = (self._config & INA3221_CONFIG_RESET) >> 15
        enablechannel1 = (self._config & INA3221_CONFIG_ENABLE_CHAN1) >> 14
        enablechannel2 = (self._config & INA3221_CONFIG_ENABLE_CHAN2) >> 13
        enablechannel3 = (self._config & INA3221_CONFIG_ENABLE_CHAN3) >> 12
        averagingmode = (self._config & (
            INA3221_CONFIG_AVG2 | INA3221_CONFIG_AVG1 | INA3221_CONFIG_AVG0
        )) >> 9
        busvoltagecvrtime = (self._config & (
            INA3221_CONFIG_VBUS_CT2 | INA3221_CONFIG_VBUS_CT1 | INA3221_CONFIG_VBUS_CT0
        )) >> 6
        shuntvoltagecvrtime = (self._config & (
            INA3221_CONFIG_VSH_CT2 | INA3221_CONFIG_VSH_CT1 | INA3221_CONFIG_VSH_CT0
        )) >> 3
        mode = (self._config & (
            INA3221_CONFIG_MODE_3 | INA3221_CONFIG_MODE_2 | INA3221_CONFIG_MODE_1
        )) >> 0

        print("Config Register {0:<3} {1:<3} {2:<3} {3:<3} {4:<8} {5:<13} {6:<13} {7}".format(
            'RST', 'CH1', 'CH2', 'CH3', 'AVERAGES', 'VBUSCT', 'VSHCT', 'MODE',
        ))
        print("                {0:>3} {1:>3} {2:>3} {3:>3} {4:<8} {5:<13} {6:<13} {7}".format(
            configreset,
            enablechannel1,
            enablechannel2,
            enablechannel3,
            averagingmodes[averagingmode],
            conversiontimes[busvoltagecvrtime],
            conversiontimes[shuntvoltagecvrtime],
            operatingmodes[mode],
        ))

    def print_alert_levels(self):
        warnalertch1 = self.get_warn_alert_mv(1)
        warnalertch2 = self.get_warn_alert_mv(2)
        warnalertch3 = self.get_warn_alert_mv(3)
        critalertch1 = self.get_crit_alert_mv(1)
        critalertch2 = self.get_crit_alert_mv(2)
        critalertch3 = self.get_crit_alert_mv(3)

        print("Alert Levels (mV) {0:>8} {1:>8} {2:>8} {3:>8} {4:>8} {5:>8}".format(
            'WarnCh1', 'CritCh1', 'WarnCh2', 'CritCh2', 'WarnCh3', 'CritCh3'
        ))
        print("                  {0:8.2f} {1:8.2f} {2:8.2f} {3:8.2f} {4:8.2f} {5:8.2f}".format(
            warnalertch1, critalertch1, warnalertch2, critalertch2, warnalertch3, critalertch3
        ))

    def get_bus_voltage_v(self, channel):
        # Gets the Bus voltage in volts
        value = self._get_bus_voltage_raw(channel)
        # Same as float(value >> 3) * 0.008
        return value * 0.001

    def get_shunt_voltage_mv(self, channel):
        # Gets the shunt voltage in mV (so +-168.3mV)
        value = self._get_shunt_voltage_raw(channel)
        # Same as float(value >> 3) * 1000 * 0.00004
        return value * 0.005

    def get_current_ma(self, channel):
        # Gets the current value in mA, taking into account the config settings and current LSB
        value = self.get_shunt_voltage_mv(channel) / SHUNT_RESISTOR_VALUE
        return value

    def set_crit_alert_mv(self, channel, value):
        register = INA3221_REG_CRITALERTLIMIT_1 + (channel - 1) * 2
        # Same as int(value / (1000 * 0.00004)) << 3
        value = int(value / .04) << 3
        self._write_register_little_endian(register, value)

    def get_crit_alert_mv(self, channel):
        # Gets the critical alert status
        value = self._read_register_little_endian(INA3221_REG_CRITALERTLIMIT_1 + (channel - 1) * 2)
        # Same as float(value >> 3) * 1000 * 0.00004
        return value * 0.005

    def set_warn_alert_mv(self, channel, value):
        register = INA3221_REG_WARNINGALERTLIMIT_1 + (channel - 1) * 2
        # Same as int(value / (1000 * 0.00004)) << 3
        value = int(value / .04) << 3
        self._write_register_little_endian(register, value)

    def get_warn_alert_mv(self, channel):
        # Gets the warn alert status
        value = self._read_register_little_endian(
            INA3221_REG_WARNINGALERTLIMIT_1 + (channel - 1) * 2)
        # Same as float(value >> 3) * 1000 * 0.00004
        return value * 0.005

    def get_shunt_voltage_sum_mv(self):
        # Gets the shunt voltage sum
        value = self._read_register_little_endian(INA3221_REG_SHUNTVOLTAGESUM)
        if value > 32767:
            value -= 65536
        # Same as float(value >> 3) * 1000 * 0.00004
        return value * 0.005

    def set_shunt_voltage_sum_limit(self, value):
        value = int(value / 0.00004) << 1
        self._write_register_little_endian(INA3221_REG_SHUNTVOLTAGESUMLIMIT, value)

    def get_shunt_voltage_sum_limit(self):
        # Gets the shunt voltage sum limit
        value = self._read_register_little_endian(INA3221_REG_SHUNTVOLTAGESUMLIMIT)
        if value > 32767:
            value -= 65536
        return value * 0.005

    def set_power_on_valid_lower(self, value):
        value = int(value / .008) << 3
        self._write_register_little_endian(INA3221_REG_PVLOWER, value)

    def get_power_on_valid_lower(self):
        value = self._read_register_little_endian(INA3221_REG_PVLOWER)
        if value > 32767:
            value -= 65536
        return value * 0.001

    def set_power_on_valid_upper(self, value):
        value = int(value / .008) << 3
        self._write_register_little_endian(INA3221_REG_PVUPPER, value)

    def get_power_on_valid_upper(self):
        value = self._read_register_little_endian(INA3221_REG_PVUPPER)
        if value > 32767:
            value -= 65536
        return value * 0.001

    def set_mask_enable(self, data):
        self._write_register_little_endian(INA3221_REG_MASKENABLE, data)

    def get_mask_enable(self):
        # Gets the value of the Mask/Enable register
        value = self._read_register_little_endian(INA3221_REG_MASKENABLE)
        return value

    def get_pv_pin(self):
        return self._pv.is_pressed

    def get_crit_pin(self):
        return self._crit.is_pressed

    def get_warn_pin(self):
        return self._warn.is_pressed

    def get_pv_flag(self):
        return self.get_mask_enable() & INA3221_REG_MASKENABLE_PVF

    def get_tc_flag(self):
        return self.get_mask_enable() & INA3221_REG_MASKENABLE_TCF

    def get_crit_flag(self, channel):
        flags = {
            1: INA3221_REG_MASKENABLE_CF1,
            2: INA3221_REG_MASKENABLE_CF2,
            3: INA3221_REG_MASKENABLE_CF3,
        }
        return self.get_mask_enable() & flags[channel]

    def get_warn_flag(self, channel):
        flags = {
            1: INA3221_REG_MASKENABLE_WF1,
            2: INA3221_REG_MASKENABLE_WF2,
            3: INA3221_REG_MASKENABLE_WF3,
        }
        return self.get_mask_enable() & flags[channel]
