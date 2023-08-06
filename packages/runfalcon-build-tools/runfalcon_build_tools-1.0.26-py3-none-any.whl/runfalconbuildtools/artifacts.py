from abc import ABC, abstractmethod
from enum import Enum
from runfalconbuildtools.file_utils import get_tmp_dir
from runfalconbuildtools.command_line_executor import CommandLineExecutor
from runfalconbuildtools.logger import Logger

class Artifact(ABC):
    
    def __init__(self, name:str, type:str):
        self.name = name
        self.type = type

class S3Artifact(Artifact):

    def __init__(self, name:str, bucket:str, folder:str, ext:str, version:str = '1.0.0'):
        super().__init__(name, 'AWS-S3')
        self.bucket = bucket
        self.folder = folder
        self.ext = ext
        self.version = version

    def get_simple_name(self):
        return self.name + '-' + self.version + '.' + self.ext

    def get_full_name(self):
        return self.folder + '/' + (self.version + '/' if self.version != None else '') +  self.get_simple_name()

    def get_s3_uri(self):
        return 's3://{bucket}/{artifact}' \
                .format(\
                    bucket = self.bucket, \
                    artifact = self.get_full_name())

class JmeterArtifact(S3Artifact):

    def __init__(self, version: str = '1.0.0'):
        super().__init__('apache-jmeter-runfalcon', 'runfalcon-support-artifacts', 'jmeter', 'zip', version)

class DummyArtifact(S3Artifact):

    def __init__(self, version: str = '1.0.0'):
        super().__init__('dummy', 'runfalcon-support-artifacts', 'dummy', 'txt', version)

class ArtifactsManager:

    __logger:Logger = Logger('ArtifactsManager')

    def __init__(self):
        pass

    def __get_download_from_s3_script(self, artifact:S3Artifact, output_folder:str) -> str:
        script:str = '#!/bin/bash\n'
        script += 'set -e\n'
        script += 'aws s3 cp {artifact} {output_folder}\n' \
                    .format(artifact = artifact.get_s3_uri(), \
                            output_folder = output_folder)
        return script

    def __download_artiact_from_aws_s3(self, artifact:S3Artifact) -> str:
        output_folder:str =  get_tmp_dir()
        script:str = self.__get_download_from_s3_script(artifact, output_folder)
        executor:CommandLineExecutor = CommandLineExecutor()
        self.__logger.info('Downloading {artifact} ...'.format(artifact = artifact.get_s3_uri()))
        executor.execute_script(script)
        return output_folder + '/' + artifact.get_simple_name()

    def get_artifact(self, artifact:Artifact, version:str = '1.0.0') -> str:
        if isinstance(artifact, S3Artifact):
            return self.__download_artiact_from_aws_s3(artifact)
        return None
