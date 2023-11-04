from helper import write_to_excel_sheet
from datetime import datetime
import boto3
import helper

# create connection to get metrices from cloudwatch
client = boto3.client('cloudwatch')
listofFSx = helper.FSX
current_year = datetime.now().year
current_month = datetime.now().month
last_month = current_month - 1

if(last_month < 1):
    last_month = 12
    current_year = current_year - 1

def getFSx():
    def FSxgetdata(list, metric):
        # create csv file with output
        # loop through FSx servers and get average monthly usage
        for fs in list:
            response = client.get_metric_statistics(
                Namespace = 'AWS/FSx',
                MetricName = metric,
                Dimensions = [
                    {
                        'Name': 'FileSystemId',
                        'Value': helper.FSX[fs]
                    },
                ],
                StartTime = f'{current_year}-{last_month}-01T00:00:00Z',
                EndTime = f'{current_year}-{current_month}-01T00:00:00Z',
                Period = 2592000,
                Statistics = [
                    'Maximum',
                ],
            )
            # filter output to get GB
            average_storage_usage_in_bytes = response['Datapoints'][0]['Maximum']
            average_storage_usage_in_gb = "{:.2f}".format(average_storage_usage_in_bytes / 1024 / 1024 / 1024)
            write_to_excel_sheet('FSx Storage', [fs, average_storage_usage_in_gb], ["Instance Name / Host", "Free Storage Capacity in Gb/s"])
            

    FSxgetdata(listofFSx, 'FreeStorageCapacity')
    # FSxgetdata(listofRDS, "CPUUtilization", "CPU Utilization")
    # FSxgetdata(listofFSx, "Memory", "Memory Utilization")
    helper.style_cells('FSx Storage')
    helper.column_width('FSx Storage')