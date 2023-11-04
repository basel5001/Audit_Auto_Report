from prometheus_api_client import PrometheusConnect
from urllib3.exceptions import InsecureRequestWarning
from helper import write_to_excel_sheet
from urllib3 import disable_warnings
import helper
import boto3


disable_warnings(InsecureRequestWarning)
def servers_getperformance():
    # try:
    # path = './Server-Performance'
    # if os.path.exists(path):
    #     print(f'{path} exists')
    # else:
    #     os.Mkdir(path)

    # Create dictionaries for use
    names_dict = {}
    linux_cpu_dict = {}
    linux_mem_dict = {}
    linux_disk_dict = {}
    win_cpu_dict = {}
    win_mem_dict = {}
    win_disk_dict = {}

    # this part gets the names of the ips
    instances = helper.Dev_ids
    ec2 = boto3.resource('ec2')
    for instance_name in instances:
        instance_id = instances[instance_name]
        instance = ec2.Instance(instance_id)
        ip_address = instance.private_ip_address
        names_dict[instance_name] = ip_address


    # Connect to prometheus endpoint
    prom = PrometheusConnect(url="https://prometheus.iaprobotics-dev.vodafone.com", disable_ssl=True)
    # get query from promotheus for CPU
    linux_cpu_query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[15d])) * 100)'
    win_cpu_query = '100 - (avg(irate(windows_cpu_time_total{mode="idle"}[30d])) by (instance)) * 100'
    # get query from promotheus for Memory
    linux_mem_query = '100.0 - (100 * node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)'
    win_mem_query = '100.0 - (100 * windows_os_physical_memory_free_bytes / windows_cs_physical_memory_bytes)'
    # get query from promotheus for Disk
    linux_disk_query = '(node_filesystem_size_bytes-node_filesystem_free_bytes) *100/(node_filesystem_avail_bytes + (node_filesystem_size_bytes-node_filesystem_free_bytes))'
    win_disk_query = '100 - (100 * windows_logical_disk_free_bytes{volume=~"C:"} / windows_logical_disk_size_bytes{volume=~"C:"})'

    # Cailling quarys
    result_linux_cpu = prom.custom_query(linux_cpu_query)
    result_linux_mem = prom.custom_query(linux_mem_query)
    result_linux_disk = prom.custom_query(linux_disk_query)

    result_win_cpu = prom.custom_query(win_cpu_query)
    result_win_mem = prom.custom_query(win_mem_query)
    result_win_disk = prom.custom_query(win_disk_query)

    # Saving output to dict
    def get_data_quary(quary, dict):
        # check quary for disk utilization
        if quary == result_linux_disk:
            for ip in quary:
                if ip ['metric']['mountpoint'].split(':')[0] == '/':
                    vm_ip = str(ip['metric']['instance']).split(':')[0]
                    value = "{:.2f}".format((float(ip['value'][1])))
                    dict[vm_ip] = value
        # check quary for CPU/Memory
        else:
            for ip in quary:
                vm_ip = str(ip['metric']['instance']).split(':')[0]
                value = "{:.2f}".format((float(ip['value'][1])))
                dict[vm_ip] = value

    # Save output to a csv/excel file
    def set_data_file(sheet_name, toprow, data):
        for name in names_dict:
            for ip in data:
                    # compare name ip with ip of prometheus and match name with ip
                if names_dict[name] == ip:
                    #     writer.writerow([name, ip, promothesusdict[ip] + "%"])
                    data_to_write = [name, ip, float(data[ip])]
                    try:
                        write_to_excel_sheet(sheet_name, data_to_write, ["Instance Name", "Private IP", f"{toprow}"])
                        # print(f'{data_to_write} written to {file_path}/{sheet_name}')
                    except Exception as e:
                        print(f'{data_to_write} could not be written to {sheet_name}: {e}')

    def set_data_file_custom(sheet_name, toprow, toprow2, toprow3, data, data2, data3):
    # with open(f'./Server-Performance/{filename}.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Instance Name", "Private IP", f"{toprow}"])

        for name in names_dict:
            for ip in data and data2 and data3:
                # compare name ip with ip of prometheus and match name with ip
                if names_dict[name] == ip:
                    data_to_write = [name, ip, data[ip], data2[ip], data3[ip]]
                    try:
                        write_to_excel_sheet(sheet_name, data_to_write, [
                            "Instance Name", 
                            "Private IP", 
                            "CPU Utilization Percentage", 
                            "Memory Utilization Percentage", 
                            "Disk Utilization Percentage"
                            ])
                        # print(f'{data_to_write} written to {file_path}/{sheet_name}')
                    except Exception as e:
                        print(f'{data_to_write} could not be written to {sheet_name}: {e}')


    # Writing to dicts for linux
    get_data_quary(result_linux_cpu, linux_cpu_dict)
    get_data_quary(result_linux_mem, linux_mem_dict)
    get_data_quary(result_linux_disk, linux_disk_dict)

    # Writing to dicts for Win
    get_data_quary(result_win_cpu, win_cpu_dict)
    get_data_quary(result_win_mem, win_mem_dict)
    get_data_quary(result_win_disk, win_disk_dict)

    print("Writing to file please wait ... ")
    # Writing to files Linux
    set_data_file('linux server CPU', 'CPU Utilization', linux_cpu_dict)
    set_data_file('linux server Memory', 'Memory Utilization', linux_mem_dict)
    set_data_file('linux server Disk', 'Disk Utilization', linux_disk_dict)
    
    # Create Charts
    helper.create_chart('linux server CPU', 3, 22)
    helper.create_chart('linux server Memory', 3, 20)
    helper.create_chart('linux server Disk', 3, 20)
    
    # format cells
    helper.style_cells('linux server CPU')
    helper.style_cells('linux server Memory')
    helper.style_cells('linux server Disk')
    
    helper.column_width('linux server CPU')
    helper.column_width('linux server Memory')
    helper.column_width('linux server Disk')
    
    # Writing to files Win
    set_data_file_custom(
        'Windows Server', 'CPU Utilization', 'Memory Utilization', 
        'Disk Utilization', win_cpu_dict, win_mem_dict, win_disk_dict)
        
    helper.style_cells('Windows Server')
    helper.column_width('Windows Server')
    # print("Finished =)")
