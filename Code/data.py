import os
import json
import csv
import pandas as pd
import prompt_bank
import datetime

def read_data(filename: str):
    data = []
    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            data.append(lines)
    return data

def read_data_pado(filename: str):
    data = []
    with open(filename, mode ='r')as file:
        txtFile = file.readlines()
        txtFile = remove_items(txtFile,'\t\n')
        for i in txtFile:
            line = i.split("\t")
            data.append(line)
        return data

def read_data_mcrae(filename: str):
    data = []
    with open(filename, mode ='r')as file:
        txtFile = file.readlines()
        txtFile = remove_items(txtFile, '\n')
        for i in txtFile:
            line = i.split(" ")
            data.append(line)
        return data

def remove_items(test_list, item):
    # remove the item for all its occurrences
    c = test_list.count(item)
    for i in range(c):
        test_list.remove(item)
    return test_list

def is_file_exits(filename: str):
    return os.path.exists(filename)

def open_result_file(filename: str, fields: []):
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

def record_exist(result_file_name: str, predicate: str, argument: str, roleType: str):

    # for ferretti Instrument and Location
    if 'ferretti' in result_file_name:
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1]:
                        return True
        return False
    
    else:
        # for Pado and Mcrae 
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1] and roleType == line[2]:
                    return True
        return False

def record_exist_other(result_file_name: str, predicate: str, argument: str, roleType: str):
    # Get the Result
    result = read_data(result_file_name)
    # Get red of the header 
    result.pop(0)

    for i in range(len(result)):
        p = result[i][0]
        a = result[i][1]
        t = result[i][2]         

        if p == predicate and a == argument and t == roleType:
            return True
    return False

def save_result(filename: str, result: []):
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the data rows
        csvwriter.writerow(result)

# processing the responses form both models is not the same, 
# for Codellama the responses was generated in  multiple form that leads us to processit in a semi-manual way.
def processing_json(model_name:str, responce: str, json_key: str ,filename_error: str, predicate: str, argument: str, roleType: str):
         ####
        if model_name == "codellama":
            try:
                print('responce: ',responce)
                data = json.loads(responce, strict=False)
                return data[json_key]

            except json.JSONDecodeError as e:
        
                print("Invalid JSON syntax:", e.msg, e)
                save_result(filename_error, [datetime.datetime.now(),predicate,argument,responce])

                if '{"Response": "Yes"}' in responce:
                    fixed = responce.split('{"Response": "Yes"}')[0]
                    responce = '{"' + json_key + '":" ' + fixed + ' "}'

                if '*' in responce:
                        responce= responce.replace('*', '')

                if  ('{"' not in responce) and ('"}' not in responce):
                    responce = '{"' + json_key + '":" ' + responce + ' "}'
                    if responce.count('"') > 4 or ('*' in responce):
                        fixed = responce.split('{\"Response\":\"  ')[1]
                        fixed = fixed.replace('"', "'")
                        fixed = fixed.split('\'}')[0]
                        fixed = '{\n\"Response\":\"' + fixed
                        fixed = fixed + '\"}'
                        responce= fixed.replace('\n', '')

                if not ('"}' in responce ):
                    responce = responce + '"}'
                    '   {"Response": "'
                    fixed = responce.split('{\"Response\": \"')[1]
                    fixed = fixed.replace('"', "'")
                    fixed = fixed.split('\'}')[0]
                    fixed = '{\n\"Response\":\"' + fixed
                    fixed = fixed + '\"}'
                    fixed= fixed.replace('*', '-')
                    responce= fixed.replace('\n', '')

                    if ('*' in responce):
                        responce = responce.replace('*', '')
                        responce = responce.replace('\n', '')
                        responce = responce.replace('\n\n', '')

                    print(responce)
                if '{\"Response": \"' in responce:
                    fixed = responce.split('{\"Response": \"')[1]
                    fixed = fixed.replace('"', "'")
                    fixed = fixed.split('\'}')[0]
                    fixed = '{\n\"Response\":\"' + fixed
                    fixed = fixed + '\"}'
                    fixed= fixed.replace('*', '-')
                    responce= fixed.replace('\n', '')

                if '{\"Response\":\"   ' in responce :
                    fixed = responce.split('{\"Response\":\"   ')[1]
                    fixed = fixed.replace('"', "'")
                    fixed = fixed.split('\'}')[0]
                    fixed = '{\n\"Response\":\"' + fixed
                    fixed = fixed + '\"}'
                    fixed= fixed.replace('*', '-')
                    responce= fixed.replace('\n', '')

                if responce.count('"') > 4 or ('*' in responce):
                    fixed = responce.split('{\"Response\": \"')[1]
                    fixed = fixed.replace('"', "'")
                    fixed = fixed.split('\'}')[0]
                    fixed = '{\n\"Response\":\"' + fixed
                    fixed = fixed + '\"}'
                    if '*' in responce:
                        fixed= fixed.replace('*', '-')
                    responce= fixed.replace('\n', '')

                if  ('{"' not in responce) and ('"}' not in responce):
                    responce = '{"' + json_key + '":" ' + responce + ' "}'
                    if responce.count('"') > 4 or ('*' in responce):
                        fixed = responce.split('{\"Response\":\"   ')[1]
                        fixed = fixed.replace('"', "'")
                        fixed = fixed.split('\'}')[0]
                        fixed = '{\n\"Response\":\"' + fixed
                        fixed = fixed + '\"}'
                        if '*' in responce:
                            fixed= fixed.replace('*', '-')
                        responce= fixed.replace('\n', '')

                if 'Expecting property name enclosed in double quotes' in e.msg:
                    dic = eval(responce)
                    dic_value = dic[json_key]
                    return dic_value

                if 'Expecting value' in e.msg:
                    fixed = responce.split(',\n]\n}')[0]
                    fixed = fixed.replace('"', "'")

                    fixed = '{\n\"Response\":\"' + fixed
                    fixed = fixed + '\"\n}'

                    try :     
                        data = json.loads(fixed)
                        return data[json_key]
                    except json.JSONDecodeError as e:
                            return   
        else:
            if not ('{' in responce ) and not ('}' in responce ):
                print(responce)
                responce = '{"' + json_key + '":"' + responce + ' "}'
                print(responce)

            if not ('"}' in responce ):
                print('yes2')
                responce = responce + '}'
                print(responce)
                
            try:
                print('responce: ',responce)
                data = json.loads(responce, strict=False)
                return data[json_key]

            except json.JSONDecodeError as e:

                if 'Expecting property name enclosed in double quotes' in e.msg:
                    dic = eval(responce)
                    dic_value = dic[json_key]
                    return dic_value

                if '```json' in responce:
                    sentences = responce.split('```json')[1]
                    sentences = sentences.split('```')[0]
                    return json.loads(sentences)[json_key]

                if 'Expecting value' in e.msg:
                    fixed = responce.split(',\n]\n}')[0]
                    fixed = fixed + '\n]\n}'
                    try:
                        data = json.loads(fixed)
                        return data[json_key]
                    except json.JSONDecodeError as e:
                        return

                if not ('{' in responce ) and not ('}' in responce ):
                    responce = '{"' + json_key + '":"' + responce + ' "}'

                if not ('"}' in responce ):
                    responce = responce + '}'
            
def get_back_exp_result(result_file_name: str, predicate: str, argument: str, roleType: str):

    if not is_file_exits(result_file_name):
        print('The file ', result_file_name, "is not exist")
        return
    
    # for ferretti Instrument and Location
    if 'ferretti' in result_file_name:
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1]:
                    return line
        return None

    else:
        # for Pado and Mrecrae
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1] and roleType == line[2]:
                    if (predicate == 'teach' and argument == 'instructor') or  predicate == 'execute' and argument == 'martyr':
                        continue # to consider both repition in the dataset.
                    return line
        return None

def retrive_reasons(result_file_name: str, dataset_name: str, model_name_only: str, predicate: str, argument: str, roleType: str):
    
    # checking the reasons retiving for exp3.2.1 and eexp3.2.2:
    retrieved_reason_filename = f'Result/retrieved_reasons_{dataset_name}_{model_name_only}.csv'
    retrieved_reasons_result = [predicate, argument, roleType]
    reasons_conversation = []
    json_key = 'Response'
    
    reasons_prompts = prompt_bank.get_prompt(
        'reasoning_lemma_tuple', predicate, argument, roleType, json_key)
    
    if not is_file_exits(result_file_name):
        print('not exist file')
        return None

    # for ferretti Instrument and Location
    if 'ferretti' in result_file_name:
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1]:
                    for i in range(3):
                        reasons_conversation.append(
                            {"role": "user", "content": f"{reasons_prompts[i]}"})
                        reasons_conversation.append(
                            {"role": "assistant", "content": f"{line[3+i]}"})

            return reasons_conversation
        return None

    else:
        # for Pado and Mrecrae
        with open(result_file_name, mode='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1] and roleType == line[2]:
                    for i in range(3):
                        reasons_conversation.append(
                            {"role": "user", "content": f"{reasons_prompts[i]}"})
                        reasons_conversation.append(
                            {"role": "assistant", "content": f"{line[3+i]}"})
                        retrieved_reasons_result.append(f"{line[3+i]}")
                        
            # Store the result record in the result file
            save_result(retrieved_reason_filename, retrieved_reasons_result)
            return reasons_conversation

        return None
