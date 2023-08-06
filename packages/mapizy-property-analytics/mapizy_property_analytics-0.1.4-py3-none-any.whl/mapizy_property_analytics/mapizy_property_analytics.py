import json, requests, time
from datetime import datetime
def development_API(API_url,API_key,Address = '5 Pele Ave Salisbury East Salisbury SA 5109',\
                              First_date= '2018-01-01',Last_date = '2020-01-01',Frequency = 'half-yearly',Analyse_type = 'change'):
  '''
    Takes the following parameters and returns the backend respond.
    Parameters: 
    
      API_url, API_key: You should get them after logining in mapizy-studio.com
      Address : Is the postal address of the requiring property.
      First_date : The first date and must be in format of YYYY-MM-DD
      Last_date : The last date and must be in format of YYYY-MM-DD
      Frequency: The frequency of imagery retriving. It can be {2-yearly,yearly,half-yearly,quarterly}
      Analyse_type : It can be {change,latest}

  '''
  
  # Check the input 
  format = "%Y-%m-%d"
  try:
    a = datetime.strptime(First_date, format)
  except:
    return {'STATUS' : 'Error_3','MESSAGE' : 'First date should be YYYY-MM-DD'}  
  try:
    a = datetime.strptime(Last_date, format)
  except:
    return {'STATUS' : 'Error_4','MESSAGE' : 'Last date should be YYYY-MM-DD'} 
  if not Frequency in ['2-yearly','yearly','half-yearly','quarterly']:
    return {'STATUS' : 'Error_5','MESSAGE' : 'Frequency can be one of {2-yearly,yearly,half-yearly,quarterly}'}
  if not Analyse_type in ['change','latest']:
    return {'STATUS' : 'Error_6','MESSAGE' : 'Analyse_type can be one of {change,latest}'}
  
  data = {"API_KEY":API_key,
        "MODE" : "PERFORM",
        "ADDRESS" : Address,
        "FIRST_DATE" : First_date, "LAST_DATE" : Last_date,
        "FREQUENCY" : Frequency, "ANALYSE_TYPE" : Analyse_type}
  headers = {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
  response = requests.post(API_url, data=json.dumps(data), headers=headers)
  response_perform_json = json.loads(response.content)
  if not 'ESTIMATED_TIME' in response_perform_json:
    return response_perform_json
  estimated_perform_time = float(response_perform_json['ESTIMATED_TIME'])
  data = {"API_KEY":API_key,
        "MODE" : "GET_STATUS",
        "TIME_CREATED" : response_perform_json['TIME_CREATED']}
  time_sleep_list = [estimated_perform_time*0.2 ,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2\
                     ,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2\
                     ,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2\
                     ,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2,estimated_perform_time*0.2]
  time_difference = 0
  for time_sleep in time_sleep_list:
    if time_sleep - time_difference>0:
      time.sleep(time_sleep - time_difference)
    st_time = time.time()
    response = requests.post(API_url, data=json.dumps(data), headers=headers)
    response_get_state_json = json.loads(response.content)
    if response_get_state_json['STATUS'] == 'FINISHED':
      return response_get_state_json
    time_difference = time.time() - st_time
  return {'STATUS' : 'Error_7','MESSAGE' : 'Server couldnt perform the request! Please retry.'}