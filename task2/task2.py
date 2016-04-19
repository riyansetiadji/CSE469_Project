#!/usr/bin/evn python
# -*- coding: utf-8 -*-
__author__ = "Riyan Setiadji"
__date__ = "March 13, 2016"

import argparse
import hashlib
import ntpath
import sys
import struct
import os

VBR_STRUCT_FORMAT = "HBHBHHBHHHIII"
MBR_STRUCT_FORMAT = "BBHBBHII"

TYPES = {
    0x01: 'DOS 12-bit FAT',
    0x04: 'DOS 16-bit FAT for partitions smaller than 32 MB',
    0x05: 'Extended partition',
    0x06: 'DOS 16-bit FAT for partitions larger than 32 MB',
    0x07: 'NTFS',
    0x08: 'AIX bootable partition',
    0x09: 'AIX data partition',
    0x0B: 'DOS 32-bit FAT',
    0x0C: 'DOS 32-bit FAT for interrupt 13 support',
    0x17: 'Hidden NTFS partition (XP and earlier)',
    0x1B: 'Hidden FAT32 partition',
    0x1E: 'Hidden VFAT partition',
    0x3C: 'Partition Magic recovery partition',
    0x66: 'Novell partitions',
    0x67: 'Novell partitions',
    0x68: 'Novell partitions',
    0x69: 'Novell partitions',
    0x81: 'Linux',
    0x82: 'Linux swap partition (can also be associated with Solaris partitions)',
    0x83: 'Linux native file system (Ext2, Ext3, Reiser, xiafs)',
    0x86: 'FAT16 volume/stripe set (Windows NT)',
    0x87: 'High Performace File System (HPFS) fault-tolerant mirrored partition or NTFS volume/stripe set',
    0xA5: 'FreeBSD and BSD/386',
    0xA6: 'OpenBSD',
    0xA9: 'NetBSD',
    0xC7: 'Typical of a corrupted NTFS volume/stripe set',
    0xEB: 'BeOS'
}


def md5_sha1(input_file, file_name):
    """
    Given input file and the file name,
    Calculate the MD5 and SHA1 hash of that file and write it to their respective text files.
    And print the result to the console
    """

    #MD5
    md5 = hashlib.md5(input_file).hexdigest()
    md5_file = open('MD5-' + file_name + '.txt','w')
    md5_file.write(md5)
    md5_file.close()

    #SHA1
    sha1 = hashlib.sha1(input_file).hexdigest()
    sha1_file = open('SHA1-' + file_name + '.txt', 'w')
    sha1_file.write(sha1)
    sha1_file.close()

    #Print to console
    print '\nChecksums:'
    print '=================================================='
    print 'MD5: ' + md5 + '\n'
    print 'SHA1: ' + sha1
    print '=================================================='

def get_mbr(input_file):
    mbr_struct = struct.Struct("<" + MBR_STRUCT_FORMAT)
    mbr_from_file = input_file[:512]
    content = mbr_from_file[446:510]
    content_list = [    mbr_struct.unpack(content[:16]),
                        mbr_struct.unpack(content[16:32]),
                        mbr_struct.unpack(content[32:48]),
                        mbr_struct.unpack(content[48:64])   ]
    for entry in content_list:
        print '(0{0:x}) '.format(entry[3]) +  (TYPES.get(entry[3]) + ', ' + str(entry[6]).zfill(10) + ', ' + str(entry[7]).zfill(10))
    return content_list
    
def get_vbr(input_file, mbr):
    for i, content in enumerate(mbr):
        if TYPES.get(content[3]) == 'DOS 16-bit FAT for partitions smaller than 32 MB' or TYPES.get(content[3]) == 'DOS 16-bit FAT for partitions larger than 32 MB' or TYPES.get(content[3]) == 'DOS 32-bit FAT' or TYPES.get(content[3]) == 'DOS 32-bit FAT for interrupt 13 support':
            vbr_content = input_file[ (content[6]*512) : ((content[6]*512) +512) ]
            vbr_struct = struct.Struct("<" + VBR_STRUCT_FORMAT).unpack(vbr_content[11:40])

            bytes_per_sector = vbr_struct[0]            
            sectors_per_cluster = vbr_struct[1]
            reserved_area_size = vbr_struct[2]
            number_of_FAT=vbr_struct[3]

            if "DOS 16" in TYPES.get(content[3]):
                root_sector = vbr_struct[4] * 32 / bytes_per_sector
                sector_per_fat = vbr_struct[7]
                clusters = reserved_area_size + (number_of_FAT * sector_per_fat) + root_sector + content[6]
            elif "DOS 32" in TYPES.get(content[3]):
                root_sector = 0
                sector_per_fat = vbr_struct[12]
                clusters = reserved_area_size + (number_of_FAT * sector_per_fat) + content[6]

            print '=================================================='
            print 'Partition ' + str(i) + '(' + TYPES.get(content[3]) + ')'
            print 'Reserved area: Start sector: ' + str(0) + ' Ending sector: ' + str(reserved_area_size - 1) + ' Size: ' + str(reserved_area_size) + ' sectors'
            print 'Sectors per cluster: ' + str(sectors_per_cluster) + ' sectors'
            print 'FAT area: Start sector: ' + str(reserved_area_size) + ' Ending sector: ' + str(reserved_area_size - 1 + (number_of_FAT*sector_per_fat))
            print '# of FATs: ' + str(number_of_FAT)
            print 'The size of each FAT: ' + str(sector_per_fat) + ' sectors'
            print 'The first sector of cluster 2: ' + str(clusters) + ' sectors'            

def main():
    try:
        image_file = sys.argv[1]
    except:
        print "Error: file not found"
        sys.exit(0)

    if not os.path.isfile(image_file):
        print "Error: unrecognized file"
        sys.exit(0)

    input_file = open(image_file, 'rb').read()
    file_name = ntpath.basename(image_file).split('.')[0]
    
    #Calculate MD5 and SHA1 hash
    md5_sha1(input_file, file_name)

    #MBR and vbr
    mbr = get_mbr(input_file)
    vbr = get_vbr(input_file, mbr)

if __name__ == '__main__':
    main()