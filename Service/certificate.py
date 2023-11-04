from helper import write_to_excel_sheet
from datetime import datetime
import helper
import boto3
import os

def get_cert():
    
    os.environ["HTTP_PROXY"] = "http://vpce-0ff47d7f2cd3a971b-90aepqr0.vpce-svc-09097c7d011d0dd07.eu-central-1.vpce.amazonaws.com:8081"
    os.environ["HTTPS_PROXY"] = "http://vpce-0ff47d7f2cd3a971b-90aepqr0.vpce-svc-09097c7d011d0dd07.eu-central-1.vpce.amazonaws.com:8081"
    
    # Create a session with proxy settings
    session = boto3.Session()
    
    # Create a client for ACM with the session
    client = session.client('acm')
    response = client.list_certificates()
    current_year = datetime.now().year
    current_month = datetime.now().month
    # Iterate over the certificates
    for certificate in response['CertificateSummaryList']:
        # Get the ARN and domain name of the certificate
        arn = certificate['CertificateArn']
        domain = certificate['DomainName']
        
        # Get more details about the certificate
        details = client.describe_certificate(CertificateArn=arn)
        
        # Get the expiration date of the certificate
        expiration = details['Certificate']['NotAfter']
        
        # print(current_month)
        # print(str(expiration).split("-")[1])
        year = int(str(expiration).split("-")[0])
        month = int((str(expiration).split("-")[1])[1])
        # print(year)
        # print(expiration)
        # print(month)
        # print(month, " " ,int(str(current_month)))
        if(year == current_year) and (month >= int(str(current_month))):
            # Print the domain name and expiration date
            # print(f'{domain}: {expiration}')
            write_to_excel_sheet('Server Certificate', [str(domain), str(expiration)], ["Instance Name / Host", "Expire Date"])
        elif(year > current_year):
            write_to_excel_sheet('Server Certificate', [str(domain), str(expiration)], ["Instance Name / Host", "Expire Date"])

    helper.style_cells('Server Certificate')
    helper.column_width('Server Certificate')
