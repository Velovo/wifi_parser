import xml.etree.ElementTree as ET
import os

class configuration():
	wifi = []
	password = []

def parse_file(filename):
	tree = ET.parse(filename)
	network_list = tree.getroot()[1]
	conf = configuration()
	for network in network_list:
		try:
			conf.wifi.append(network[0][1].text.replace('"', ''))
		except:
			conf.wifi.append(None)
		try:
			conf.password.append(network[0][4].text.replace('"', ''))
		except:
			conf.password.append(None)
	return (conf)

def output(conf):
	longest_name = len(max(conf.wifi, key=len))
	print(' ' * (longest_name - len('wifi name')), end='')
	print('wifi name | password')
	for i in range(len(conf.wifi)):
		print(' ' * (longest_name - len(conf.wifi[i])), end='')
		print(conf.wifi[i], end='')
		print(' | ', end='')
		if conf.password[i] != None:
			print(conf.password[i])
		else:
			print()

def set_newfilename(path_to_wifi_config):
	while path_to_wifi_config == None:
		path_to_wifi_config = input('Enter path to wifi configuration: ')
		if os.path.isfile(path_to_wifi_config) == True:
			fd = open('./conf', 'w+')
			fd.write(path_to_wifi_config)
			fd.close
			return (path_to_wifi_config)
		else:
			print('Error: file not found')
			path_to_wifi_config = None

def getfilname():
	path_to_wifi_config = None
	if os.path.isfile('./conf') == False:
		print('No configuration file found.')
		return (set_newfilename(path_to_wifi_config))
	else:
		fd = open('./conf')
		path_to_wifi_config = fd.readline()
		if os.path.isfile(path_to_wifi_config) == True:
			return (path_to_wifi_config)
		else:
			print('Error: file not found')
			return (set_newfilename(None))

if __name__ == '__main__':
	filename = getfilname()
	conf = parse_file(filename)
	output(conf)
