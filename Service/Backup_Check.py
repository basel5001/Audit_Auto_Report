from helper import write_to_excel_sheet
import helper
import boto3
import os

def list_backup_vaults():
    os.environ["HTTP_PROXY"] = "http://vpce-0ff47d7f2cd3a971b-90aepqr0.vpce-svc-09097c7d011d0dd07.eu-central-1.vpce.amazonaws.com:8081"
    os.environ["HTTPS_PROXY"] = "http://vpce-0ff47d7f2cd3a971b-90aepqr0.vpce-svc-09097c7d011d0dd07.eu-central-1.vpce.amazonaws.com:8081"
    # Create a session with proxy settings
    session = boto3.Session()
    # Create a Boto3 session with the specified profile
    # Create a Boto3 client for AWS Backup
    backup_client = boto3.client('backup')
    
    # List backup vaults
    # response = backup_client.list_backup_vaults()
    
    # Extract the vaults from the response
       
    # Get all backup plans
    response = backup_client.list_backup_plans()
    
    # Iterate over each backup plan
    for backup_plan in response['BackupPlansList']:
        # Get backup plan details
        backup_plan_details = backup_client.get_backup_plan(BackupPlanId=backup_plan['BackupPlanId'])
        plan = backup_plan['BackupPlanName']

        # Iterate over each rule in the backup plan
        for rule in backup_plan_details['BackupPlan']['Rules']:
            Rule = rule['RuleName']
            Retention = str(rule['Lifecycle']['DeleteAfterDays'])
            write_to_excel_sheet('BackUp Plans', [Rule, Retention, plan], ['Backup Rules', 'Retention Periods Days', 'BackUp Plans'])
            
    
    response = backup_client.list_protected_resources()
    resources = response['Results']
    # print(resources)
    # Print the resource details
    for resource in resources:
        Name = f"{resource['ResourceName']}"
        # print(f"Resource ID: {resource['ResourceArn']}")
        Type = f"{resource['ResourceType']}"
        LastBUT = f"{resource['LastBackupTime']}"
        write_to_excel_sheet('BackedUp Resources', [Name, Type, LastBUT], ['Resource Name', 'Resource Type', 'Last Backup Time'])
     
    
    backup_plans = backup_client.list_backup_plans()['BackupPlansList']
# For each backup plan, get the associated resources and retention period
    # for plan in backup_plans:
    #     backup_plan = backup_client.get_backup_plan(BackupPlanId=plan['BackupPlanId'])['BackupPlan']
    #     selection = backup_client.get_backup_selection(BackupPlanId=plan['BackupPlanId'], SelectionId=backup_plan['Rules'][0]['TargetBackupVaultName'])
    #     for resource in selection['ListOfTags']:
    #         # print(f"Resource Type: {resource['ConditionType']}")
    #         res = resource['ConditionType']
    #         # print(f"Associated Backup Plan: {backup_plan['BackupPlanName']}")
    #         bkplan = backup_plan['BackupPlanName']
    #         # print(f"Retention Period: {backup_plan['Rules'][0]['Lifecycle']['DeleteAfterDays']} days")
    #         Retper = backup_plan['Rules'][0]['Lifecycle']['DeleteAfterDays']
    #         write_to_excel_sheet('BackedUp Resources Custom', [res, bkplan, Retper], ['Resource Type', 'BackUp Plan', 'Retention Period'])

            # print("------------------------")
def getBackup():
    # Call the function to list AWS Backup vaults in the specified profile
    list_backup_vaults()
    helper.style_cells('BackUp Plans')
    helper.style_cells('BackedUp Resources')
    helper.column_width('BackUp Plans')
    helper.column_width('BackedUp Resources')
    
    helper.style_cells('BackedUp Resources Custom')
    helper.column_width('BackedUp Resources Custom')


    