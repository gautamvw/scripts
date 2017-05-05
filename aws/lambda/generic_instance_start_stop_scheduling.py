import boto3, re
from datetime import date
from time import gmtime, strftime

def lambda_handler(event, context):
  sts_client = boto3.client('sts')
  RoleArnSub=''.join(['arn:aws:iam::','%s',':role/Cross-Account-DevOps-Test'])%event['account_ID']
  print RoleArnSub
  assumedRoleObject = sts_client.assume_role(
      RoleArn=RoleArnSub,
      RoleSessionName="AssumeRoleSession1"
  )
    
  credentials = assumedRoleObject['Credentials']
  ec2 = boto3.resource('ec2', 'us-east-1',aws_access_key_id = credentials['AccessKeyId'],aws_secret_access_key = credentials['SecretAccessKey'],aws_session_token = credentials['SessionToken'])
  Schedule_Format = re.compile('Uptime-.{7}-\d{4}-\d{4}')
  start_array = []
  stop_array = []
  instances = ec2.instances.filter(Filters=[])

  for instance in instances:
    if not instance.tags:
      print "No tags found for the instance id %s, exiting ..."%instance.id
      break
    else:
      for i in range(len(instance.tags)):
        if instance.tags[i]['Key']=='Automation_Schedule_Opt_Out':
          Automation_Schedule_Opt_Out=instance.tags[i]['Value']
        elif instance.tags[i]['Key']=='Automation_Schedule':
          Automation_Schedule=instance.tags[i]['Value']
      if not Automation_Schedule_Opt_Out or not Automation_Schedule:
        print "Either Tags %s and %s not found for instance %s"%(Automation_Schedule_Opt_Out,Automation_Schedule,instance.id)
      else:
        print instance.id, instance.instance_type, instance.state
        if Automation_Schedule_Opt_Out=='Yes':
          print "Opting out of Automation Schedule"
          break
        else:
          #find current state
          current_state=instance.state['Name']
          if Automation_Schedule=='Uptime-AlwaysOn' and current_state=='stopped':
            print "Automation_Schedule is %s and current_state is %s, starting the instance"%(Automation_Schedule,current_state)
            start_array.append(instance.id)
          elif Automation_Schedule=='Uptime-AlwaysOn' and current_state=='running':
            print "Automation_Schedule is %s and current_state is %s, nothing to be done"%(Automation_Schedule,current_state)
            break
          elif Automation_Schedule=='Uptime-AlwaysOff' and current_state=='stopped':
            print "Automation_Schedule is %s and current_state is %s, nothing to be done"%(Automation_Schedule,current_state)
            break
          elif Automation_Schedule=='Uptime-AlwaysOff' and current_state=='running':
            print "Automation_Schedule is %s and current_state is %s, stopping the instance"%(Automation_Schedule,current_state)
            stop_array.append(instance.id)
          #tag in Uptime-MTWRFXX-0700-1745 format
          elif Schedule_Format.match(Automation_Schedule) is not None:
            Schedule_Split=Automation_Schedule.split("-")
            today = date.today()
            weekday_num = today.weekday()
            days_array=Schedule_Split[1]
            start_time=Schedule_Split[2]
            end_time=Schedule_Split[3]
            current_time=strftime("%H%M", gmtime())
            if days_array[weekday_num].upper=='X':
              print "nothing to do on %s, exiting ..."%weekday_num
            else:
              if current_state=='running' and current_time > end_time:
                print "Automation_Schedule is %s, current_state is %s, current time is %s, stopping the instance"%(Automation_Schedule,current_state,current_time)
                stop_array.append(instance.id)
              elif current_state=='running' and end_time > current_time:
                print "Automation_Schedule is %s, current_state is %s, current time is %s, nothing to do"%(Automation_Schedule,current_state,current_time)
              elif current_state=='stopped' and ((current_time > start_time) and (current_time < end_time)):
                print "Automation_Schedule is %s, current_state is %s, current time is %s, starting the instance"%(Automation_Schedule,current_state,current_time)
                start_array.append(instance.id)
              elif current_state=='stopped' and start_time > current_time:
                print "Automation_Schedule is %s, current_state is %s, current time is %s, nothing to do"%(Automation_Schedule,current_state,current_time)
          else:
            print "Automation_Schedule is %s which is not in correct format\n     \
            Correct Format should be like Uptime-MTWTFXX-0700-1900 or Uptime-AlwaysOn/Uptime-AlwaysOff"%Automation_Schedule
  if len(start_array) > 0:
    print "start_array is %s"%start_array
    starting = ec2.instances.filter(InstanceIds=start_array).start()
    print starting
  else:
    print "no instances found to be started"
  if len(stop_array) > 0:
    print "stop_array is %s"%stop_array
    stopping = ec2.instances.filter(InstanceIds=stop_array).stop()
    print stopping
  else:
    print "no instances found to be stopped"

# #Uptime-MTWTFXX-0700-1900