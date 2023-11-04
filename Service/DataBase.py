from helper import write_to_excel_sheet
import datetime
import helper
import pyodbc
import helper


def Database_getdata():
    # def lambda_handler(event, context):
    #     # TODO implement

    # sqs_handler= SQS(logger)
    # ews_sqs_name = "vdf-dev-01-sqs-rca-send-emails"
    str_quary= helper.str_quary
    str_tablescount_quary = helper.str_tablescount_quary
    # ssm = boto3.client('ssm', region_name='eu-central-1') 
    # DB_username = 'mssqladmin'
    # DB_password = '4NhKDSrJ0nFKnD3o2OA1wOzMk'
    username = helper.DB_username
    password = helper.DB_password
    server = helper.DB_server
    port ='1433'
    driver ='ODBC Driver 17 for SQL Server'
    database = 'UiPath20'
    quary_output=[['job Name','Run Date','Status']]
    table_count_output="table Name, Rows Count \r\n"
    cnxn = pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute(str_quary)
    row = cursor.fetchone()
    str_html= "\r\n"
    jobs =[]
    schduled_jobs = ['ArchiveQueueItems','Archive RobotLicense Logs' ,'Archive TenantNotifications','Archive Jobs','Archive AuditLogs and AuditLogEntities','Archive Actions Cleanup','Archive Ledger and LedgerDeliveries']
    while row:
        if row[0] != "syspolicy_purge_history":
            if 'succeeded' in row[2] :
                str_html =str_html+ row[0] + " :  " + " Success. \r\n"
                jobs.append(row[0])
            else :
                str_html =str_html+ row[0] + " :  " + " Failed. \r\n"
                jobs.append(row[0])

        row = cursor.fetchone()
    missed_jobs_count = 0
    missed_jobs =""
    for job in schduled_jobs :
        if job in jobs :
            missed_jobs_count = missed_jobs_count
        else:
            missed_jobs_count = missed_jobs_count + 1
            missed_jobs = missed_jobs + job +", "
    if missed_jobs_count >0 :
        str_html = "Hi All,  \r\nData Base Current Table Rows counts attached on mail 'DB_Tables_Counts.CSV',  \r\nAnd this is a list of The scheduled DB jobs that's run last 7 days with thier status: " + str_html + "\r\nAnd there is a missed jobs didn't run during 7 days there count is : "+ str(missed_jobs_count) + ",\r\nThis missed jobs names is : "+missed_jobs+". \r\nThanks,"
    else :
        str_html = "Hi All,  \r\nThe Data Base Current Table Rows counts attached on mail 'DB_Tables_Counts.CSV',  \r\nAnd this is a list of The scheduled DB jobs that's run last 7 days with thier status: " + str_html + " \r\nThanks,"
    # print(str_html)
    now = datetime.datetime.utcnow() # now is a datetime object
    cursor_tables = cnxn.cursor()
    cursor_tables.execute(str_tablescount_quary)
    tables_row = cursor_tables.fetchone()
    flag1 = 0

    while tables_row:
        # table_count_output = table_count_output + tables_row[0] + "," + str(tables_row[1]) + "\r\n"
        if(flag1 < 127) or (int(tables_row[1]) > 0):
            # str("0" if cursor_tables.fetchone() is None else cursor_tables.fetchone())
            tables_row = cursor_tables.fetchone()
            # print(tables_row)
            # print(type(tables_row))
            # print(flag1)
            flag1 = flag1 + 1
            flag = 0
            row = str(tables_row[0])
            count = int(tables_row[1])
            for R in helper.DataBaseRec:
                if (R in row) and (count != 0) and (flag == 0):
                    write_to_excel_sheet('Records', [row, count], ["Table Name", "Row Count"])
                    flag = 1
        else:
            break
    helper.style_cells('Records', 10000, 100000)
    helper.column_width('Records')
