from csv import reader
import os
import csv 
import pandas as pd 


class file_handle:
    def __init__(self,file_name):
        self.file_name=file_name

    def append_dict(self,site_info,header_list):
        if isinstance(site_info,dict):
            writer_header = False
            if not os.path.isfile(self.file_name):
                writer_header = True
            with open (self.file_name,mode='a',newline='') as f :
                fieldnames = header_list
                writer = csv.DictWriter( f,fieldnames=fieldnames)
                if writer_header == True:
                    writer.writeheader()  
                writer.writerow(site_info)    
        else:
            for site_dict in site_info:
                self.append_dict(site_dict,header_list)

    def read_by_col(self,col_num) :
        result_list=[]
        with open (self.file_name,mode='r',newline='') as f :
            fhandle=reader(f)
            fhandle=list(fhandle)
            fhandle = fhandle[1:]
            try:
                for col in fhandle:
                    result_list.append(col[col_num-1])
            except :
                print ('Error ! : Remove unused rows from the CSV file')
                exit()
            return result_list


    def get_file_headers(self):
        header_list = []
        with open (self.file_name,mode='r',newline='') as f :
            fhandle=reader(f)
            fhandle=list(fhandle)
            fhandle = fhandle[0]
            for row in fhandle:
                header_list.append(row)
            return header_list



    def write_to_column(self, header_name, write_list,header_list):
        data_dict= {}
        key_list =[] 
        for index, header in enumerate (header_list):
            data_dict[header] = self.read_by_col(index+1)
        for key in write_list:
            key_list.append(key)
        data_dict[header_name] = key_list
        try:
            data_frame = pd.DataFrame(data_dict)
            data_frame.to_csv(self.file_name, mode='w',index=False)
        except:
            print ('nothing to log ') 
 
# print (f' This module is {__name__}')