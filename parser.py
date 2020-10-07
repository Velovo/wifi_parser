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
			for element in network[0]:
				if element.attrib['name'] == 'SSID':
					conf.wifi.append(element.text.replace('"', ''))
		except:
			conf.wifi.append(None)
		try:
			for segment in network:
				for element in segment:
					if element.attrib['name'] == 'PreSharedKey':
						if element.text == None:
							conf.password.append(None)
						else:
							conf.password.append(element.text.replace('"', ''))
					if segment.tag == 'WifiEnterpriseConfiguration' and len(conf.password) > 0:
						if element.attrib['name'] == 'Identity' and len(conf.wifi) == len(conf.password):
							conf.password[len(conf.password) - 1] = element.text
						if element.attrib['name'] == 'Password' and len(conf.wifi) == len(conf.password) and conf.password[len(conf.password) - 1] != None:
							conf.password[len(conf.password) - 1] = conf.password[len(conf.password) - 1] + ':' + element.text
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
			fd = open('/data/data/com.termux/files/home/wifi_parser/conf', 'w+')		# fd = open('./conf', 'w+') 	
			fd.write(path_to_wifi_config)
			fd.close
			return (path_to_wifi_config)
		else:
			print('Error: file not found')
			path_to_wifi_config = None

def getfilname():
	path_to_wifi_config = None
	if os.path.isfile('/data/data/com.termux/files/home/wifi_parser/conf') == False:	# if os.path.isfile('./conf') == False:
		print('No configuration file found.')
		return (set_newfilename(path_to_wifi_config))
	else:
		fd = open('/data/data/com.termux/files/home/wifi_parser/conf')					# fd = open('./conf')
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
