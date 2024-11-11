import fastf1
import asyncio

def main(year,race_indx,session):
    session = fastf1.get_session(year,race_indx,session)
    get_info = session.load(telemetry=False, weather=False)
    return get_info

def ordered_names(session_results):
    ordered_result = session_results.results.to_dict()['BroadcastName']
    ordered_names = []
    for key in list(ordered_result.keys()):
        # print((len(ordered_result[key])))
        if ordered_result[key] == 'nan':
            continue
        else:
            name = ordered_result[key].split(' ')[1] 
            # sometimes this results an empty string so need to fix that
            ordered_names.append(name[0]+name[1:].lower())
    return ordered_names
    
def call_from_dp_ops(year,race_indx,session,names=True):
    session_info = fastf1.get_session(year, race_indx, session)
    session_info.load(telemetry=False, weather=False)
    # await asyncio.sleep(1)
    if names:
        # print("Here",session_info.results.to_dict()['BroadcastName'])
        # input()
        session_results = ordered_names(session_info)
    else:
        session_results = session_info.car_data
    return session_results 
    
if __name__ == "__main__":
    results = call_from_dp_ops(2024,21,'R',names=False)
    print(results)
    # print(results)