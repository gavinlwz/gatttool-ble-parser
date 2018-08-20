import sys
import requests

URLS = ['https://bluetooth.com/specifications/gatt/characteristics','https://bluetooth.com/specifications/gatt/declarations', 'https://bluetooth.com/specifications/gatt/descriptors',' https://bluetooth.com/specifications/gatt/services']

def open_file(filename):
	bluetooth_characteristics = open(filename)
	return bluetooth_characteristics

def parse_bluetooth_characteristics(data_file):
	parsed_bluetooth_data = []
	for line in data_file.readlines():
		line = line.split(" ")
		handle = line[1]
		uuid = line[3]
		parsed_bluetooth_data.append([handle,uuid])
	return parsed_bluetooth_data

def parse_bluetooth_primary(data_file):
	parsed_bluetooth_data = []
	for line in data_file.readlines():
		line = line.split(" ")
		handle = line[2]
		uuid = line[8]
		parsed_bluetooth_data.append([handle,uuid])
	return parsed_bluetooth_data	

def get_docs_link(raw_tags):
	close_to_link = raw_tags.split("href=")[1]
	for index in range(len(close_to_link)):
		if(close_to_link[index] == '>'):
			return "https://www.bluetooth.com/specifications/gatt/" + close_to_link[1:index-1]

def get_property_name(raw_tags):
	bluetooth_property = ''
	isRecording = False
	for char in raw_tags:
		if(char == ">"):
			isRecording = True
		elif(char == "<" and isRecording):
			return bluetooth_property[1:]
		
		if(isRecording):
			bluetooth_property += char
	return char

def gatt_info_request(domain):
	specs_list = []	
	raw_html_page = requests.get(domain)
	raw_tags = raw_html_page.content.split("<tr>")[2:-1] # just getting the pages content.
	for specification in raw_tags:
		docs_info = specification.split("<td>")[1]
		doc_link = get_docs_link(docs_info)
		bluetooth_property = get_property_name(docs_info)
		
		#Just want the 4 digit specs code from the site.
		spec_property_key = specification.split("<td>")[3].split('<')[0][2:] 
		specs_list.append([spec_property_key, bluetooth_property,doc_link])
	
	# Looks like this:
	# [Spec Number, Name, Docs Link] for each entry
	return specs_list

def get_vendor_info():
	full_vendor_info = []
	vendor_url = "https://bluetooth.com/specifications/assigned-numbers/16-bit-uuids-for-members"
	raw_html_page = requests.get(vendor_url).content.split('["')[1:-1]
	for vendor in raw_html_page: 
		vendor_info = vendor.replace('"','').replace(']','')
		vendor_info = vendor_info.split(',')
		uuid = shorten_uuid(vendor_info[1])
		full_vendor_info.append([uuid,"vendor--" + vendor_info[2]])
	return full_vendor_info
	
	
def gatt_information(domain_list):
	full_specs_list = []	
	for domain in domain_list:
		full_specs_list = full_specs_list + gatt_info_request(domain)
	return full_specs_list


def find_matches(parsed_bluetooth_characteristics, specifications_bluetooth):
	comparison_list = []
	for spec in parsed_bluetooth_characteristics:
		comparison_list.append([spec[0],shorten_uuid(spec[1]).upper()])

	print "Handle -- uuid -- vendor/purpose"
	for result in comparison_list:
		for spec in specifications_bluetooth:
			if(result[1] == spec[0]):
				print result[0], result[1], spec[1]

def shorten_uuid(uuid):
	uuid = uuid.split("-")[0]
	fresh_uuid = ""
	isRecording = False
	for char in uuid:
		if(char != '0' and char != 'x'):
			isRecording=True
		if(isRecording):
			fresh_uuid += char
	return fresh_uuid
			

def parse_data(filename):
	bluetooth_characteristics_file = open_file(filename)
	parsed_bluetooth_characteristics= parse_bluetooth_characteristics(bluetooth_characteristics_file)
	specifications_bluetooth = gatt_information(URLS)
	return parsed_bluetooth_characteristics, specifications_bluetooth

if __name__ == '__main__':
	if(len(sys.argv) == 1):
		print "Need parameters"
	else:
		
		# need to allow the primary vs char-desc to be here. 
		vendor_info = get_vendor_info()
		results, specs = parse_data(sys.argv[1])
		find_matches(results, specs + vendor_info)


