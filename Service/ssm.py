import boto3
from botocore.exceptions import ClientError
from time import sleep


class SSM:
    def __init__(self, logger, aws_region):
        self.logger = logger
        self.ssm_client = boto3.client("ssm", region_name=aws_region)

    def get_parameter(self, parametername):
        self.logger.info("Retrieving value from parameter store.")
        try:
            response = self.ssm_client.get_parameter(
                Name=parametername, WithDecryption=True
            )
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code == 200:
                self.logger.info("SSM get parameter connection established.")
                parameter = response["Parameter"]
                for key in parameter:
                    if key == "Value":
                        self.logger.info("Parameter retrieved successfully.")
                        return parameter[key]
            else:
                self.logger.warning(f"An error occurred. Status code: {status_code}")
        except ClientError as error:
            self.logger.exception(f"An error occurred while trying to get parameter.")
            raise error

    def ad_user_creation(
        self, username, password, firstname, lastname, ad_instance_id, ssm_ad_document
    ):
        try:
            self.logger.info(f"Checking if username already exist in Active Directory.")
            response = self.ssm_client.send_command(
                InstanceIds=[ad_instance_id],
                DocumentName=ssm_ad_document,
                Parameters={
                    "Username": [username],
                    "Password": [password],
                    "Firstname": [firstname],
                    "Lastname": [lastname],
                },
            )
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code == 200:
                self.logger.info(f"SSM send command status code: {status_code}")
                command_id = response["Command"]["CommandId"]
                self.logger.info(f"SSM Command ID: {command_id}")
                return command_id
            else:
                self.logger.warning(f"An error occurred. Status code: {status_code}")
        except ClientError as error:
            self.logger.exception(f"An error occurred while trying to create AD user.")
            raise error

    def command_invocation(self, command_id, ad_instance_id):
        try:
            sleep(3)
            response = self.ssm_client.get_command_invocation(
                CommandId=command_id, InstanceId=ad_instance_id
            )
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code == 200:
                self.logger.info(f"SSM invocation command status code: {status_code}")
                while response["Status"] == "InProgress":
                    sleep(5)
                    response = self.ssm_client.get_command_invocation(
                        CommandId=command_id, InstanceId=ad_instance_id
                    )
                    status = response["Status"]
                    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
                    if status_code == 200:
                        self.logger.info(f"Checking the status of SSM Document.")
                        self.logger.info(f"SSM Invocation status code: {status_code}")
                        self.logger.info(f"SSM Document status: {status}")
                        outputcontent = response["StandardOutputContent"]
                        errorcontent = response["StandardErrorContent"]
                        if outputcontent != "":
                            user_exist = outputcontent.split("-")[0].strip()
                            info = outputcontent.split("-")[1].split("\n")[0].strip()
                            info_ = outputcontent.split("-")[1].split("\n")[1].strip()
                            self.logger.info(
                                f"Outputcontent from SSM Document: {info} {info_}"
                            )
                        if errorcontent != "":
                            self.logger.info(
                                f"Errorcontent from SSM Document: {errorcontent}"
                            )
                    else:
                        self.logger.warning(
                            f"An error occurred. Invocation status code: {status_code}"
                        )
                        self.logger.info(f"SSM Document status: {status}")
            return user_exist
        except ClientError as error:
            self.logger.exception(
                f"An error occurred while checking SSM document status."
            )
            raise error