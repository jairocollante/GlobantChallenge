from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Department, Job, Hiredemployee, Logger
from .serializers import DepartmentSerializer, JobSerializer, HiredemployeeSerializer

import fastavro
from datetime import datetime



@api_view(['GET'])
def backup(request):

    queryset = Department.objects.all().values()

    schema = {
        'doc': 'Department table backup.',
        'name': 'Department',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'department', 'type': 'string'},
        ],
    }
    dep_rows = [] 
    for item in queryset:
        dep_rows.append({ "id": item["id"], 
                        "department": item["department"]})  

    with open('./challenge1/backupData/department.avro', 'wb') as out:
        fastavro.writer(out, schema,dep_rows)

        ####JOB

    queryset = Job.objects.all().values()

    schema = {
        'doc': 'Job table backup.',
        'name': 'Job',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'job', 'type': 'string'},
        ],
    }
    
    job_rows = [] 
    for item in queryset:
        job_rows.append({ "id": item["id"], 
                        "job": item["job"]})  

    with open('./challenge1/backupData/job.avro', 'wb') as out:
        fastavro.writer(out, schema, job_rows)


 ##HIRED
    queryset = Hiredemployee.objects.all().values()

    schema = {
        'doc': 'Hiredemployee table backup.',
        'name': 'Hiredemployee',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'name', 'type': 'string'},
            {'name': 'datetime', 'type': {"type": "long", "logicalType": "timestamp-millis"}},
            {'name': 'department', 'type': 'int'},
            {'name': 'job', 'type': 'int'},
        ],
    }
    
    hir_rows = [] 
    for item in queryset:
        hir_rows.append({ "id": item["id"], 
                        "name": item["name"],
                        "datetime": int(item["datetime"].timestamp() * 1000),
                        "department": item["department_id"],
                        "job":item["job_id"]
                        })

    with open('./challenge1/backupData/Hiredemployee.avro', 'wb') as out:
        fastavro.writer(out, schema, hir_rows)


    return Response("Backup realizado", status=status.HTTP_201_CREATED)


@api_view(['GET'])
def restore(request):
    with open('./challenge1/backupData/department.avro', 'rb') as f:
        reader = fastavro.reader(f)
        records = [record for record in reader] 
        
        for record in records:            
            Department.objects.create( id=record["id"], department=record["department"])


    with open('./challenge1/backupData/job.avro', 'rb') as f:
        reader = fastavro.reader(f)
        records = [record for record in reader] 
        
        for record in records:            
            Job.objects.create( id=record["id"], job=record["job"])

    
    with open('./challenge1/backupData/Hiredemployee.avro', 'rb') as f:
        reader = fastavro.reader(f)
        records = [record for record in reader] 
        
        for record in records:
            datetime_v = datetime.fromtimestamp(record["datetime"] / 1000.0)            
            Hiredemployee.objects.create( id=record["id"], 
                                          name=record["name"],
                                          datetime=datetime_v,                                          
                                          department=record["department"],
                                          job=record["job"])

    
    return Response("Restore ", status=status.HTTP_201_CREATED)







@api_view(['POST'])
def new_data(request):
    if isinstance(request.data, list):
        if (1 <= len(request.data) <= 1000):           
        
            try:
                serializer = HiredemployeeSerializer(data=request.data, many=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else :
                    print(invalid_serializer.errors)
                    serializer = DepartmentSerializer(data=request.data, many=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else :
                        serializer = JobSerializer(data=request.data, many=True)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                log = Logger(detail=serializer.errors, log= request.data)
                log.save()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            log = Logger(detail="Tama;o de listado no valido, debe ser entre 1 y 1000", log= request.data)
            log.save()
            return Response({"error": "Tama;o de listado no valido, debe ser entre 1 y 1000"}, status=status.HTTP_400_BAD_REQUEST)

            
    else:
        try:
            serializer = HiredemployeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                serializer = DepartmentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    serializer = JobSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            print(serializer.errors)
            log = Logger(detail=serializer.errors,  log= request.data)
            log.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

        except:
            log = Logger(detail=serializer.errors,  log= request.data)
            log.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        
        







