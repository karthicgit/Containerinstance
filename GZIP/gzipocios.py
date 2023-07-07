import os
import oci
import gzip
import re

def decompress_gzip(bucket_name,namespace,object_storage_client,**kwargs):
  
    bucket_name = bucket_name
    namespace = namespace
    prefix = kwargs.get("prefix")
    #list objects in object storage
    try:
        list_objects = object_storage_client.list_objects(namespace, bucket_name,prefix=prefix).data.objects
    except oci.exceptions.ServiceError as oci_exception:
        print(oci_exception)
    #loop through objects which ends with .gz and decompress them
    for i in list_objects:
        gzip_file = i.name
        if gzip_file.endswith(".gz"):
            try:
                gzip_object = object_storage_client.get_object(namespace,bucket_name,gzip_file).data.content
                data = gzip.decompress(gzip_object)
                object_storage_client.put_object(
                    namespace_name=namespace,
                    bucket_name=bucket_name,
                    object_name=re.sub(r'\.gz$', '', gzip_file),
                    put_object_body=data)
            except oci.exceptions.ServiceError as oci_exception:
                print(oci_exception)
            except Exception as e:
                print(e)
        else:
            continue

def handler():
    try:
        signer = oci.auth.signers.get_resource_principals_signer()
        object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)

        bucket_name = os.getenv('BUCKET_NAME')
        prefix = os.getenv('PREFIX')
        namespace = object_storage_client.get_namespace().data
        decompress_gzip(bucket_name, namespace,object_storage_client,prefix=prefix)

    except oci.exceptions.ServiceError as oci_exception:
        print(oci_exception)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    handler()
