#!/usr/bin/python
from  .file_handle import *  
from .ot_class import *  


class OT : 
    def __init__(self,key):
        self.key= key
        self.ot_instance = ot(self.key)

    def scan_sites(self,col_num_site,col_num_org,number_of_pages):
        self.ot_instance.get_scan_sites(col_num_site = col_num_site, col_num_org = col_num_org, number_of_pages = number_of_pages)

    def retrieve_api(self,col_num,script_type,write_to_file):
        self.ot_instance.get_api_key_retrieve(col_num = col_num,script_type = script_type ,write_to_file = write_to_file)

    def site_attributes(self,extract_attr,write_to_file,search_domain_list):
        self.ot_instance.get_site_attributes(extract_attr = extract_attr ,write_to_file= write_to_file,search_domain_list = search_domain_list)

    def publish_ot_script(self,col_num,script_type):
        self.ot_instance(col_num = col_num ,script_type = script_type) 
 

