from helper import write_to_excel_sheet
from datetime import datetime, timedelta
import boto3
import helper

current_year = datetime.now().year
current_month = datetime.now().month
current_month = current_month -1
last_month = current_month - 1

if(last_month < 1):
    last_month = 12
    current_year = current_year - 1

end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=5)

def RDS_getdata():
    client = boto3.client('cloudwatch')
    # create excel file with output
    def RDS(list, metric):
        for RDS in list:
            response = client.get_metric_statistics(
                Namespace = 'AWS/RDS',
                MetricName = metric,
                Dimensions = [
                    {
                        'Name': 'DBInstanceIdentifier',
                        'Value': RDS
                    },
                ],
                StartTime = f'{current_year}-{last_month}-01T00:00:00Z',
                EndTime = f'{current_year}-{last_month}-29T00:00:00Z',
                Period = 2592000,
                Statistics = [
                    'Average',
                ],
            )
        # check for metrices
        if (metric == "FreeStorageSpace"):
            # Store output to CSV file
            free_storage = "{:.2f}".format(response['Datapoints'][0]['Average'] / 1024 / 1024 / 1024)
            write_to_excel_sheet('RDS Storage', [RDS, free_storage], ["Instance Name / Host", "Free Storage Capacity in Gb/s"])
        
        elif (metric == "CPUUtilization"):
            cpu_utili = "{:.2f}".format(response['Datapoints'][0]['Average'])
            write_to_excel_sheet('RDS CPU', [RDS, cpu_utili], ["Instance Name / Host", "CPU Utilization Percentage"])

    listofRDS = helper.RDS
    # calling methods at specific metrices 
    RDS(listofRDS, "FreeStorageSpace")
    RDS(listofRDS, "CPUUtilization")
    helper.style_cells('RDS CPU')
    helper.style_cells('RDS Storage')
    helper.column_width('RDS CPU')
    helper.column_width('RDS Storage')