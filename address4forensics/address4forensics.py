#!/usr/bin/evn python
# -*- coding: utf-8 -*-
__author__ = "Riyan Setiadji"
__date__ = "March 11, 2016"

"""
Address Conversion:

In order to both simplify addressing mechanisms and to reduce the number of bits necessary to locate all areas within a logical space (like a partition) that hold data, 
multiple addressing techniques are used on IBM PC-compatible hard drives and in FAT file systems. 
You are to write a Unix-like command line utility that will convert between three different address types when an address of a different type is given. 
Use the following usage specifications for your utility:

address4forensics -L|-P|-C [–b offset] [-B [-s bytes]] [-l address] [-p address] [-c address -k sectors -r sectors -t tables -f sectors]

-L, --logical
    Calculate the logical address from either the cluster address or the physical address. Either –c or –p must be given.
-P, --physical
    Calculate the physical address from either the cluster address or the logical address. Either –c or –l must be given.
-C, --cluster
    Calculate the cluster address from either the logical address or the physical address. Either –l or –p must be given.
-b offset, --partition-start=offset
    This specifies the physical address (sector number) of the start of the partition, and defaults to 0 for ease in working with images of a single partition. The offset value will always translate into logical address 0.
-B, --byte-address
    Instead of returning sector values for the conversion, this returns the byte address of the calculated value, which is the number of sectors multiplied by the number of bytes per sector.
-s bytes, --sector-size=bytes
    When the –B option is used, this allows for a specification of bytes per sector other than the default 512. Has no affect on output without –B.
-l address, --logical-known=address
    This specifies the known logical address for calculating either a cluster address or a physical address. When used with the –L option, this simply returns the value given for address.
-p address, --physical-known=address
    This specifies the known physical address for calculating either a cluster address or a logical address. When used with the –P option, this simply returns the value given for address.
-c address, --cluster-known=address
    This specifies the known cluster address for calculating either a logical address or a physical address. When used with the –C option, this simply returns the value given for address. Note
        that options –k, -r, -t, and option.
-k sectors, --cluster-size=sectors
    This specifies the number of sections per cluster
-r sectors, --reserved=sectors
    This specifies the number of reserved sections in the partition
-t tables, --fat-tables=tables
    This specifies the number of the number of FAT tables, which is usually 2
-f sectors, --fat-length=sectors
    This specifies the length of each FAT table in sectors
"""

from argparse import ArgumentParser
"""
logical_address(arguments.partition_start, arguments.logical_known, arguments.cluster_known, arguments.physical_known,
                            arguments.cluster_size, arguments.reserved, arguments.fat_tables, arguments.fat_length, arguments.sector_size,
                            arguments.byte_address)
"""
def logical_address(partition_start=0, logical_known=None, cluster_known=None, physical_known=None,
                      cluster_size=None, reserved=None, fat_tables=2, fat_length=None,
                      sector_size=512, byte_address=None):
    """
    Calculate logical address
    """
    # Calculate the address.
    if physical_known:
        if byte_address:
            return (physical_known - partition_start)*sector_size
        else:
            return (physical_known - partition_start)
    elif cluster_known:
        if cluster_size and reserved and fat_tables and fat_length:
            if byte_address:
                return ((cluster_known-2)*cluster_size + reserved + fat_tables * fat_length)*sector_size
            else:
                return ((cluster_known-2)*cluster_size + reserved + fat_tables * fat_length)
        else:
            return 'Error: Missing Arguments'
    elif logical_known:
        logical = logical_known
        if byte_address:
            return logical*sector_size
        else:
            return logical
    else:
        return 'Error: Missing Arguments'

"""
physical_address(arguments.partition_start, arguments.logical_known, arguments.cluster_known, arguments.physical_known,
                             arguments.cluster_size, arguments.reserved, arguments.fat_tables, arguments.fat_length, arguments.sector_size,
                             arguments.byte_address)
"""
def physical_address(partition_start=0, logical_known=None, cluster_known=None, physical_known=None,
                       cluster_size=None, reserved=None, fat_tables=2, fat_length=None,
                       sector_size=512, byte_address=None):
    """
    Calculate the physical address
    """
    # Calculate physical address.
    if physical_known:
        if byte_address:
            return physical_known*sector_size
        else:
            return physical_known
    elif logical_known:
        if byte_address:
            return (logical_known + partition_start)*sector_size
        else:
            return logical_known + partition_start       
    elif cluster_known:
        if cluster_size and reserved and fat_tables and fat_length:
            if byte_address:
                return (partition_start + cluster_size*(cluster_known-2) + reserved + fat_tables * fat_length)*sector_size
            else:
                return (partition_start + cluster_size*(cluster_known-2) + reserved + fat_tables * fat_length)
        else:
            return 'Error: Missing Arguments.'
    else:
        return 'Error: Missing Arguments'

"""
cluster_address(arguments.partition_start, arguments.logical_known, arguments.cluster_known, arguments.physical_known,
                            arguments.cluster_size, arguments.reserved, arguments.fat_tables, arguments.fat_length)
"""
def cluster_address(partition_start=0, logical_known=None, cluster_known=None, physical_known=None,
                      cluster_size=None, reserved=None, fat_tables=2, fat_length=None):
    """
    Calculate the cluster address
    """
    # Calculate the address.
    if cluster_known:
        return cluster_known
    elif logical_known:
        return (logical_known - (reserved + fat_tables * fat_length))//(cluster_size+2)
    elif physical_known and cluster_size and reserved and fat_tables and fat_length:
        return (physical_known - partition_start - (reserved + fat_tables * fat_length))//(cluster_size+2)
    else:
        return 'Error: Missing Arguments'

def address4forensics(arguments):
    """
    Given mutually exclusive group argument from the user,
    Calculate logical, physical, or cluster address using the rest of the arguments
    """
    if arguments.logical:
		print(logical_address(arguments.partition_start, arguments.logical_known, arguments.cluster_known, arguments.physical_known,
                            arguments.cluster_size, arguments.reserved, arguments.fat_tables, arguments.fat_length, arguments.sector_size,
                            arguments.byte_address))
    elif arguments.physical:
		print(physical_address(arguments.partition_start, arguments.logical_known, arguments.cluster_known, arguments.physical_known,
                             arguments.cluster_size, arguments.reserved, arguments.fat_tables, arguments.fat_length, arguments.sector_size,
                             arguments.byte_address))
    elif arguments.cluster:
		print(cluster_address(arguments.partition_start, arguments.logical_known, arguments.cluster_known, arguments.physical_known,
                            arguments.cluster_size, arguments.reserved, arguments.fat_tables, arguments.fat_length))
    else:
        print('Error: Invalid Arguments.')
        print('Address Conversion: \
            \n\nIn order to both simplify addressing mechanisms and to reduce the number of bits necessary to locate all areas within a logical space (like a partition) that hold data,\
            \nmultiple addressing techniques are used on IBM PC-compatible hard drives and in FAT file systems. \
            \nYou are to write a Unix-like command line utility that will convert between three different address types when an address of a different type is given. \
            \nUse the following usage specifications for your utility: \
            \naddress4forensics -L|-P|-C [–b offset] [-B [-s bytes]] [-l address] [-p address] [-c address -k sectors -r sectors -t tables -f sectors] \
            \n\n-L, --logical \
            \n\tCalculate the logical address from either the cluster address or the physical address. Either –c or –p must be given. \
            \n-P, --physical \
            \n\tCalculate the physical address from either the cluster address or the logical address. Either –c or –l must be given. \
            \n-C, --cluster \
            \n\tCalculate the cluster address from either the logical address or the physical address. Either –l or –p must be given. \
            \n-b offset, --partition-start=offset \
            \n\tThis specifies the physical address (sector number) of the start of the partition, and defaults to 0 for ease in working with images of a single partition. The offset value will always translate into logical address 0. \
            \n-B, --byte-address\
            \n\tInstead of returning sector values for the conversion, this returns the byte address of the calculated value, which is the number of sectors multiplied by the number of bytes per sector. \
            \n-s bytes, --sector-size=bytes \
            \n\tWhen the –B option is used, this allows for a specification of bytes per sector other than the default 512. Has no affect on output without –B. \
            \n-l address, --logical-known=address \
            \n\tThis specifies the known logical address for calculating either a cluster address or a physical address. When used with the –L option, this simply returns the value given for address. \
            \n-p address, --physical-known=address \
            \n\tThis specifies the known physical address for calculating either a cluster address or a logical address. When used with the –P option, this simply returns the value given for address. \
            \n-c address, --cluster-known=address \
            \n\tThis specifies the known cluster address for calculating either a logical address or a physical address. When used with the –C option, this simply returns the value given for address. Note that options –k, -r, -t, and option. \
            \n-k sectors, --cluster-size=sectors \
            \n\tThis specifies the number of sections per cluster \
            \n-r sectors, --reserved=sectors \
            \n\tThis specifies the number of reserved sections in the partition \
            \n-t tables, --fat-tables=tables \
            \n\tThis specifies the number of the number of FAT tables, which is usually 2 \
            \n-f sectors, --fat-length=sectors \
            \n\tThis specifies the length of each FAT table in sectors')



if __name__ == "__main__":
    """
    Main Function

    1. Getting the arguments from the user
    2. Insert the given arguments into address4forensics function

    """
    parser = ArgumentParser()
    functional = parser.add_mutually_exclusive_group()
    functional.add_argument('-L','--logical', action='store_true')
    functional.add_argument('-C','--cluster', action='store_true')
    functional.add_argument('-P','--physical',action='store_true')
    parser.add_argument('-b', '--partition-start', type=int, default=0)
    parser.add_argument('-B', '--byte-address', action='store_true')
    parser.add_argument('-s', '--sector-size', type=int, default=512)
    parser.add_argument('-l', '--logical-known', type=int)
    parser.add_argument('-p', '--physical-known', type=int)
    parser.add_argument('-c', '--cluster-known', type=int)
    parser.add_argument('-k', '--cluster-size', type=int)
    parser.add_argument('-r', '--reserved', type=int)
    parser.add_argument('-t', '--fat-tables', type=int, default=2)
    parser.add_argument('-f', '--fat-length', type=int)
    arguments = parser.parse_args() 	
    address4forensics(arguments)


