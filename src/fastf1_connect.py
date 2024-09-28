import fastf1
import asyncio

def main(info):
    session = fastf1.get_session(info['year'], info['race_indx'], info['session'])
    session.load(telemetry=False, weather=False)
    return session

def ordered_names(session_results):
    ordered_result = session_results.results.to_dict()['BroadcastName']
    ordered_names = []
    for key in list(ordered_result.keys()):
        print(key,ordered_result[key])
        if ordered_result[key] == 'nan':
            continue
        else:
            name = ordered_result[key].split(' ')[1]
            ordered_names.append(name[0]+name[1:].lower())
    return ordered_names
    
async def call_from_dp_ops(year,race_indx,session,names=True):
    session_info = fastf1.get_session(year, race_indx, session)
    session_info.load(telemetry=False, weather=False)
    await asyncio.sleep(1)
    if names:
        session_results = ordered_names(session_info)
    else:
        session_results = session_info.drivers
    return session_results 
    