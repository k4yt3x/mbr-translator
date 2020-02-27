#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: MBR Record Translator
Author: K4YT3X
Date Created: February 11, 2020
Last Modified: February 26, 2020

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2020 K4YT3X
"""

import sys
import readline

VERSION = '1.0.0'

# full mapping: https://en.wikipedia.org/wiki/Partition_type
DOS_PARTITION_MAPPING = {'0x00': 'Empty',
                         '0x01': 'FAT12, CHS',
                         '0x04': 'FAT16, 16–32 MB, CHS',
                         '0x05': 'Microsoft Extended, CHS',
                         '0x06': 'FAT16, 32 MB–2GB, CHS',
                         '0x07': 'NTFS',
                         '0x0b': 'FAT32, CHS',
                         '0x0c': 'FAT32, LBA',
                         '0x0e': 'FAT16, 32 MB–2GB, LBA',
                         '0x0f': 'Microsoft Extended, LBA',
                         '0x11': 'Hidden FAT12, CHS',
                         '0x14': 'Hidden FAT16, 16–32 MB, CHS',
                         '0x16': 'Hidden FAT16, 32 MB–2GB, CHS',
                         '0x1b': 'Hidden FAT32, CHS',
                         '0x1c': 'Hidden FAT32, LBA',
                         '0x1e': 'Hidden FAT16, 32 MB–2GB, LBA',
                         '0x42': 'Microsoft MBR. Dynamic Disk',
                         '0x82': 'Solaris x86',
                         '0x82': 'Linux Swap',
                         '0x83': 'Linux',
                         '0x84': 'Hibernation',
                         '0x85': 'Linux Extended',
                         '0x86': 'NTFS Volume Set',
                         '0x87': 'NTFS Volume Set',
                         '0xa0': 'Hibernation',
                         '0xa1': 'Hibernation',
                         '0xa5': 'FreeBSD',
                         '0xa6': 'OpenBSD',
                         '0xa8': 'Mac OSX',
                         '0xa9': 'NetBSD',
                         '0xab': 'Mac OSX Boot',
                         '0xb7': 'BSDI',
                         '0xb8': 'BSDI swap',
                         '0xee': 'EFI GPT Disk',
                         '0xef': 'EFI System Partition',
                         '0xfb': 'Vmware File System',
                         '0xfc': 'Vmware swap',
                         }
SECTOR_SIZE = 512


def bytes_to_decimal(bytes_list: list) -> int:
    """ converts bytes into decimal format

    Arguments:
        bytes_list {list} -- a list of bytes in string format

    Returns:
        int -- the bytes in integer format
    """
    return int(f'0x{"".join(bytes_list)}', 16)


# take MBR partition record from user input and sanitize the input
record = input('MBR Partition Record: ').strip().replace(' ', '').upper()
record = [record[i:i+2] for i in range(0, len(record), 2)]

# the MBR record should be exactly 32 characters long
if len(''.join(record)) != 32:
    print('Invalid input')
    sys.exit(1)

# parse each field in the record
boot_code = record[0]
starting_chs_address = bytes_to_decimal(record[3:0:-1])
partition_type = record[4]
ending_chs_address = bytes_to_decimal(record[7:4:-1])
starting_lba_address = bytes_to_decimal(record[11:7:-1])
size_in_sectors = bytes_to_decimal(record[15:11:-1])

# render output string
output = f'''Boot Code: 0x{boot_code}
Starting CHS Address: {starting_chs_address}
Partition Type: {DOS_PARTITION_MAPPING.get(f"0x{partition_type}", f"0x{partition_type}")}
Ending CHS Address: {ending_chs_address}
Starting LBA Address: {starting_lba_address}
Size in Sectors: {size_in_sectors}

Assumed Sector Size: {SECTOR_SIZE}B
Partition Size: {size_in_sectors * SECTOR_SIZE}B
Partition Size: {size_in_sectors * SECTOR_SIZE / 1024}KB
Partition Size: {size_in_sectors * SECTOR_SIZE / 1024 ** 2}MB
Partition Size: {size_in_sectors * SECTOR_SIZE / 1024 ** 3}GB
'''

# print string to stdout
print(output)
