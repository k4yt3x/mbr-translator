#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: FAT Record Translator
Author: K4YT3X
Date Created: March 7, 2020
Last Modified: March 19, 2020

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2020 K4YT3X
"""

# built-in imports
import readline
import sys

VERSION = '1.1.0'


def bytes_to_decimal(bytes_list: list) -> int:
    """ converts bytes into decimal format

    Arguments:
        bytes_list {list} -- a list of bytes in string format

    Returns:
        int -- the bytes in integer format
    """
    return int(f'0x{"".join(bytes_list)}', 16)


# take FAT boot record from user input and sanitize the input
record = input('FAT Partition Record: ').strip().replace(' ', '').upper()
record = [record[i:i + 2] for i in range(0, len(record), 2)]

# the FAT boot record should be at least 62 characters long
if len(record) < 62:
    print('The input data is less than 62 bytes, which is the minimal size of a FAT boot record')

    if input('Would you like to analyze this incomplete record? [y/N]: ').lower() == 'y':
        record += ['00'] * (62 - len(record))

    else:
        print('Script exiting')
        sys.exit(1)

# parse each field in the record
boot_code_jump_assembly_instruction = record[0:3]
oem_name = bytearray.fromhex(''.join(record[3:11])).decode()
bytes_per_sector = list(reversed(record[11:13]))
sectors_per_cluster = record[13]
reserved_area_size = list(reversed(record[14:16]))
number_of_fats = record[16]
max_number_of_files_in_root_directory = list(reversed(record[17:19]))
number_of_sectors = list(reversed(record[19:21]))
media_type = record[21]
size_of_each_fat = list(reversed(record[22:24]))

# render output string
output = f'''Boot Code Jump Assembly Instruction: {" ".join(boot_code_jump_assembly_instruction)}
OEM name: {oem_name}
Bytes per sector: {bytes_to_decimal(bytes_per_sector)} ({" ".join(bytes_per_sector)})
Sectors per cluster: {bytes_to_decimal(sectors_per_cluster)} ({sectors_per_cluster})
Reserved area size: {bytes_to_decimal(reserved_area_size)} ({" ".join(reserved_area_size)})
Number of FATs: {bytes_to_decimal(number_of_fats)} ({number_of_fats})
Maximum number of files in root directory: {bytes_to_decimal(max_number_of_files_in_root_directory)} ({" ".join(max_number_of_files_in_root_directory)})
Number of sectors: {bytes_to_decimal(number_of_sectors)} ({" ".join(number_of_sectors)})
Media type: {media_type}
Size of each FAT: {bytes_to_decimal(size_of_each_fat)} ({" ".join(size_of_each_fat)})
'''

# print string to stdout
print(output)

# if the rest is all padded with 0s, skip parsing
if int(''.join(record[36:]), 16) == 0x0:
    print('Rest of the data is all 0s')
    print('Further analysis skipped')
    sys.exit(0)

# start parsing FAT12/16 and FAT32 separately
# if size of each fat (bytes 22-23) is not 0, this is FAT12/16
# the script will then parse the remaining data with FAT12/16's boot sector structure
if bytes_to_decimal(size_of_each_fat) != 0:
    bios_int13h_drive_number = record[36]
    # unused_byte = record[37]
    extended_boot_signature = record[38]
    volume_serial_number = record[39:43]
    volume_label = bytearray.fromhex(''.join(record[43:54])).decode()
    file_system_type_label = bytearray.fromhex(''.join(record[54:62])).decode()

    output = f'''BIOS INT13h drive number: {bios_int13h_drive_number}
Extended boot signature: 0x{extended_boot_signature}
Volume serial number: 0x{" ".join(volume_serial_number)}
Volume label: {volume_label}
File system type label: {file_system_type_label}
'''
    print(output)

# if the file system is FAT32
else:
    size_of_each_fat = list(reversed(record[36:40]))
    # TODO
