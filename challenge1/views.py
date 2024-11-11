from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Department, Job, Hiredemployee, Logger
from .serializers import DepartmentSerializer, JobSerializer, HiredemployeeSerializer

from fastavro import writer, parse_schema



@api_view(['GET'])
def backup(request):

    dep_rows = list(Department.objects.values())

    schema = {
        'doc': 'Department table backup.',
        'name': 'Department',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'department', 'type': 'string'},
        ],
    }
    parsed_schema = parse_schema(schema)    

    with open('department.avro', 'wb') as out:
        writer(out, parsed_schema, dep_rows)

        ####JOB

    job_rows = list(Job.objects.values())

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
    parsed_schema = parse_schema(schema)    

    with open('job.avro', 'wb') as out:
        writer(out, parsed_schema, job_rows)


 ##HIRED

    hir_rows = list(Hiredemployee.objects.values())

    print(hir_rows[0])

    schema = {
        'doc': 'Hiredemployee table backup.',
        'name': 'Hiredemployee',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'name', 'type': 'string'},
            {'name': 'datetime', 'type': 'string'},
            {'name': 'department', 'type': 'int'},
            {'name': 'job', 'type': 'int'},
        ],
    }
    parsed_schema = parse_schema(schema)    

    with open('Hiredemployee.avro', 'wb') as out:
        writer(out, parsed_schema, hir_rows)






    return Response("Backup realizado", status=status.HTTP_201_CREATED)




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



        
        







