permission:
	chmod +x address4forensics/address4forensics
	chmod +x address4forensics/address4forensics.py
	chmod +x mac_conversion/mac_conversion
	chmod +x mac_conversion/mac_conversion.py
	chmod +x task2/task2
	chmod +x task2/task2.py

test_address4forensics:
	python address4forensics/address4forensics.py -L -b 128 --physical-known=12345678
	python address4forensics/address4forensics.py -P --partition-start=128 -c 58 -k 4 -r 6 -t 2 -f 16

test_mac_conversion:
	python mac_conversion/mac_conversion.py -T -f mac_conversion/test.txt
	python mac_conversion/mac_conversion.py -D -h 0x4f42

test_task2:
	python task2/task2.py task2/TestImage1.img
	python task2/task2.py task2/TestImage2.img

clean:
	rm MD5*
	rm SHA1*