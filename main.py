import json
from collections import defaultdict
from datetime import datetime, timedelta

# Utils
def json_save(data, filename):    
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"{filename} saved successfully")

def convert_str_to_time(timevalue):
    return datetime.strptime(timevalue, "%m/%d/%Y")

def preprocess_data(data):
    for person in data:
        for completion in person['completions']:

            completion['timestamp'] = convert_str_to_time(completion['timestamp'])
                       
            if completion['expires']:
                completion['expires'] = convert_str_to_time(completion['expires'])
            else:
                completion['expires'] = None

    return data
# ----------

def Task1(data):
    training_counts = defaultdict(int)

    for person in data:
        training_dict = {}
             
        for training in person['completions']:
            training_name = training['name']
            training_timestamp = training['timestamp']
                     
            if training_name not in training_dict:
                training_dict[training_name] = training_timestamp
            else:                
                existing_date = training_dict[training_name]
                new_date = training_timestamp
                if new_date > existing_date:
                    training_dict[training_name] = training_timestamp                   
               
        for training_name in training_dict.keys():
            training_counts[training_name] += 1
    
    return training_counts



def Task2(data, target_trainings, fiscal_year):
    start_fiscal_year = datetime(fiscal_year - 1, 7, 1)
    end_fiscal_year = datetime(fiscal_year, 6, 30)

    training_results = {training: [] for training in target_trainings}
    
    for person in data:
        training_dict = {}
               
        for training in person['completions']:
            training_name = training['name']
            training_timestamp = training['timestamp']
                        
            if training_name in target_trainings:
              
                if start_fiscal_year <= training_timestamp <= end_fiscal_year:
                 
                    if training_name not in training_dict:
                        training_dict[training_name] = training_timestamp
                    else:
                      
                        if training_timestamp > training_dict[training_name]:
                            training_dict[training_name] = training_timestamp
                
        for training_name, _ in training_dict.items():
            training_results[training_name].append(person['name'])
    
    return training_results


def Task3(data, specified_date):
    expiration_check_date = specified_date
    expires_soon_check_date = specified_date + timedelta(days=31)

    results = []
    
    for person in data:
        person_result = {"name": person["name"], "completions": []}
        training_dict = {}
    
        for training in person["completions"]:
            training_name = training["name"]
            training_timestamp = training["timestamp"]
            expires_on_date = training["expires"]
                        
            if not expires_on_date:
                continue
                      
            if training_name not in training_dict:
                training_dict[training_name] = {"timestamp": training_timestamp, "expires": expires_on_date}
            else:
                if training_timestamp > training_dict[training_name]["timestamp"]:
                    training_dict[training_name] = {"timestamp": training_timestamp, "expires": expires_on_date}
       
        for training_name, details in training_dict.items():
            expires_on_date = details["expires"]

            if expires_on_date < expiration_check_date:                
                person_result["completions"].append({
                    "training_name": training_name,
                    "status": "expired"                    
                })
            elif expiration_check_date <= expires_on_date < expires_soon_check_date:               
                person_result["completions"].append({
                    "training_name": training_name,
                    "status": "expires soon"                    
                })
        
        if person_result["completions"]:
            results.append(person_result)
    
    return results



if __name__ == "__main__":
    with open('trainings.json') as file:
        training_data_raw = json.load(file)

    training_data = preprocess_data(training_data_raw)   # Converts values of timestamp and expires, from string to datetime objects
    
    json_save(Task1(training_data), "Task1_result.json")
   
    target_trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    fiscal_year = 2024

    json_save(Task2(training_data, target_trainings, fiscal_year), "Task2_result.json")

    specified_date = datetime(2023, 10, 1)

    json_save(Task3(training_data, specified_date), "Task3_result.json")