import sys
sys.path.append('./Service')
from ServerPerform import servers_getperformance
from DataBase import Database_getdata
from helper import create_excel_file
from Liceofficial import get_licence
from Backup_Check import getBackup
from certificate import get_cert
from RDS import RDS_getdata
from FSx import getFSx
import numpy as np
import helper

def lambda_handler(event, context):
    print(" ====================== Starting and Creating Files ====================== ")
# Create Excel Sheet
    create_excel_file([
        'linux server CPU',
        'linux server Memory',
        'linux server Disk',
        'Windows Server',
        'Records',
        'RDS CPU',
        'RDS Storage',
        'FSx Storage',
        'Server Certificate',
        'Server Licence',
        'BackUp Plans',
        'BackedUp Resources',
        'BackedUp Resources Custom'
    ], helper.file_path)
    
# Create Excel Sheet for Charts
    # create_excel_file([
    #     'CPU Linux Chart',
    #     'Memory Linux Chart',
    #     'Disk Linux Chart',
    # ], helper.file_chart)
    
# Implementig the Services
    servers_getperformance()
    print("Servers Done")
    
    get_licence()
    print("Licences Done")

    getFSx()
    print("FSx Done")

    RDS_getdata()
    print("RDS Done")

    Database_getdata()
    print("DataBase Done")

    get_cert()
    print("Certificate Done")

    getBackup()
    print("BackUp Done")
    
# Upload Excel Sheet to S3 Bucket
    helper.uploadfile()
    print(" ====================== Finished and Files Uploaded to 's3://audit-iap-automation' ====================== ")