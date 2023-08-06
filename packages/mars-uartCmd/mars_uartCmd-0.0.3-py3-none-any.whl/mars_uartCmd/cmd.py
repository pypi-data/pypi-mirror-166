import sys
import time

import numpy as np
import serial
from tqdm import tqdm

SLEEP = 0.3  # sleep 0.3sec for each read/write


class CMD:
    def __init__(self, serial: serial):
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4
        self.endian = "big"
        self.value = None
        self.serial = serial

    def read(self):
        write_cmd = f"{self.cmd}=?".encode("ascii")
        self.serial.write(write_cmd)
        read_data = self.serial.read(self.byteSize)
        # print(read_data)
        if self.dtype == np.str:
            self.value = read_data.decode("ascii")
        else:
            self.value = np.frombuffer(read_data, dtype=self.dtype)
            if sys.byteorder != self.endian:
                self.value = self.value.copy().byteswap(inplace=True)
            # self.value = self.value[0]
        time.sleep(SLEEP)
        return self.value

    def write(self, inputs):
        if self.dtype == np.str:
            write_data = inputs.encode("ascii")
        else:
            self.value = np.array(inputs).astype(self.dtype)
            if sys.byteorder != self.endian:
                self.value = self.value.byteswap(inplace=True)
            write_data = self.value.tobytes()
        write_head = f"{self.cmd}=".encode("ascii")
        write_tail = "?".encode("ascii")
        # print(write_data)
        write_cmd = write_head + write_data + write_tail
        self.serial.write(write_cmd)
        time.sleep(SLEEP)


class A1:
    def __init__(self, serial: serial):
        self.cmd = __class__.__name__
        self.dtype = np.int16
        self.byteSize = 2457600
        self.endian = "little"
        self.value = []
        self.serial = serial

    def read(self):
        buffer = []
        for i in tqdm(range(0, 2457600, 24576)):
            write_head = f"{self.cmd}=".encode("ascii")
            write_addr = np.array(i).copy().byteswap(inplace=True).tobytes()
            write_tail = "?".encode("ascii")
            write_cmd = write_head + write_addr + write_tail
            self.serial.write(write_cmd)
            read_data = self.serial.read(24576)
            value = np.frombuffer(read_data, dtype=self.dtype)
            if sys.byteorder != self.endian:
                value = value.copy().byteswap(inplace=True)
            buffer.append(value)
            time.sleep(SLEEP)
        self.value = np.concatenate(buffer)
        return self.value

    def write(self, inputs):
        self.value = np.array(inputs).astype(self.dtype)
        if sys.byteorder != self.endian:
            self.value = self.value.byteswap(inplace=True)
        data = self.value.tobytes()
        for i in tqdm(range(0, 2457600, 24576)):
            write_addr = np.array(i).copy().byteswap(inplace=True).tobytes()
            write_data = data[i : i + 24576]
            write_head = f"{self.cmd}=".encode("ascii")
            write_tail = "?".encode("ascii")
            write_cmd = write_head + write_addr + write_data + write_tail
            self.serial.write(write_cmd)
            # wait OK?
            ack = self.serial.read(3).decode("ascii")
            if ack != "OK?":
                raise ValueError("ack != OK?")
            time.sleep(SLEEP)


class CFG:
    def __init__(self, serial: serial):
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4
        self.endian = "big"
        self.value = []
        self.serial = serial

    def read(self):
        write_cmd = f"{self.cmd}=LOAD?".encode("ascii")
        self.serial.write(write_cmd)
        time.sleep(SLEEP)

    def write(self):
        write_cmd = f"{self.cmd}=SAVE?".encode("ascii")
        self.serial.write(write_cmd)
        print("write config, need ~30sec")
        # wait OK?
        ack = self.serial.read(3).decode("ascii")
        if ack != "OK?":
            raise ValueError("ack != OK?")
        time.sleep(SLEEP)


class FRS(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4


class FMS(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4


class GMS(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 2


class LGV(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4


class HGV(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4


class SMS(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4


class STP(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.int16
        self.byteSize = 2


class VTP(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.int16
        self.byteSize = 2


class VZF(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 2


class SFD(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4


class HUP(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 1


class PLP(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 1


class LGP(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 1


class SMP(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 1


class HTC(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 8


class HBC(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 8


class TUS(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 4


class LGR(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.uint8
        self.byteSize = 51200


class AL1(A1):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.int16
        self.byteSize = 2457600


class AL2(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 40


class AH1(A1):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.int16
        self.byteSize = 2457600


class AH2(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 40


class A1B(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 1


class A21(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 4


class A22(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 4


class A23(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 4


class A24(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 4


class A25(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 4


class A26(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 4


class A27(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.float32
        self.byteSize = 4


class A2B(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 1


class A31(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.uint8
        self.byteSize = 1


class A3B(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 1


class VOM(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 3


class RTC(CMD):
    def __init__(self, serial: serial):
        super().__init__(serial)
        self.cmd = __class__.__name__
        self.dtype = np.str
        self.byteSize = 14
