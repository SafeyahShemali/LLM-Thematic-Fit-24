import data
from models import Model
import fit_scoring
import prompt_bank
import json
import datetime

'''Experiment 1'''
def exp_simple_lemma_tuple_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
     '''Setting Preparation'''
    exp_name = 'lemma_tuple'

    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(100)       

    # Get the data
    dataset = data.read_data(filename)
    
    # Create files for the results if not exits 
    fields = ['predicate', 'argument', 'actual_fit', 'exp_fit']
    
    #get the dataset name
    dataset_name = filename.split('.csv')[0]
    
    #get the model name 
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1] 
    
    # Prepare files for the output 
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
        
    for i in range(len(dataset)):

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()
        
        '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')
            
        #in case we rerun the code, we no need to redo the already finished records
        if IsExist1 and IsExist2:
                continue

        '''Result Preparation'''  
        result1 = [predicate, argument, actual_fit]
        result2 = [predicate, argument, actual_fit]

        '''Prompting For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'categorical')

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
         '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

# The difference than the previous one:
# - no need to specify the roletype as it is included in the dataset (ARG0, ARG1, ARG2)
# - reading the data is diffrernt due to the dataset formating 
# - result fields are different
def exp_simple_lemma_tuple_other(filename: str, model: Model, model_name: str):
    
    '''Setting Preparation'''
    exp_name = 'lemma_tuple'

    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(100)       

    # Get the dataset 
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument', 'role_type' , 'actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1]   
        
    # Prepare files for the output 
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'    

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
        
    for i in range(1): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()

        '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument, roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument, roleType)

        if IsExist1 and IsExist2:
            continue   

        '''Result Preparation'''  
        result1 = [predicate, argument, roleType, actual_fit]
        result2 = [predicate, argument, roleType, actual_fit]

        '''Prompting For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'categorical')

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')
        
'''Experiment 3'''
def exp_reasoning_lemma_tuple_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
    '''Setting Preparation'''
    exp_name = 'lemma_tuple'
    date = datetime.datetime.now()

    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(600)       

    # Get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1] 
    
    # Prepare files for the output 
    result_filename1 = f'Result/{exp_name}_reasoning_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_reasoning_categorical_{dataset_name}_{model_name_only}.csv'
    reason_filename = f'Result/reasons_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(reason_filename):
        data.open_result_file(filename= reason_filename, fields= ['predicate', 'argument', 'role_type', 'reasons 1', 'reasons 2','reasons 3'])
   
    for i in range(len(dataset)): 

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2: # to execlude duplicate
            continue
            
        '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)
        
        '''Result Preparation'''  
        result1 = [predicate, argument, actual_fit]
        result2 = [predicate, argument, actual_fit]

        '''Step-by-Step Reasoning'''
        fit_scoring.reasoning('',model,model_name_only, predicate, argument, roleType, reason_filename, '')
        
        '''Prompting For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'categorical')
        
        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

# The difference than the previous one:
# - no need to specify the roletype as it is included in the dataset (ARG0, ARG1, ARG2)
# - reading the data is diffrernt due to the dataset formating 
# - result fields are different
def exp_reasoning_lemma_tuple_other(filename: str, model: Model, model_name: str):
    
    '''Setting Preparation'''
    exp_name = 'lemma_tuple'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(600)       

    # Get the data
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','role_type','actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1]    
        
    # Prepare files for the output 
    result_filename1 = f'Result/{exp_name}_reasoning_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_reasoning_categorical_{dataset_name}_{model_name_only}.csv'
    reason_filename = f'Result/reasons_{dataset_name}_{model_name_only}.csv'
    
    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(reason_filename):
        data.open_result_file(filename= reason_filename, fields= ['predicate', 'argument', 'role_type', 'reasons 1', 'reasons 2','reasons 3'])   
   
    for i in range(len(dataset)): 

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument , roleType)

        if IsExist1 and IsExist2:
                continue
        
         '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)
        
        '''Result Preparation'''  
        result1 = [predicate, argument, roleType, actual_fit]
        result2 = [predicate, argument, roleType, actual_fit]
        
        '''Step-by-Step Reasoning'''
        fit_scoring.reasoning('',model,model_name_only,predicate, argument, roleType, reason_filename, '')
        
        '''Prompting For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'categorical')

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, model_name_only, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)
        
        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

'''Experiment 2'''
def exp_simple_gen_sentences_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
    '''Setting Preparation'''
    exp_name = 'gen_sentences'

    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1]    
        
    # Prepare files for the output 
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(sentence_filename):
        data.open_result_file(filename= sentence_filename, fields= ['predicate','argument','sentence 1','sentence 2','sentence 3','sentence 4','sentence 5'])  
    
    for i in range(1): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
            
        '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)
        
        '''Result Preparation'''  
        result1 = [predicate, argument]
        result2 = [predicate, argument]
        result3 = [predicate, argument]
        
        '''Generating Sentences Part'''
        sentences = fit_scoring.generate_sentence(model, model_name_only, predicate, argument, roleType)

        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:
            
            '''Storing Sentences'''
            result3.append(sentence)
            
            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, model_name_only, predicate, argument, roleType, sentence) 

            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'categorical', sentence)
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'numerical', sentence)

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            else:
                '''Back off'''
                result1.append('')
                result2.append('')
                
                '''Retrieve the data from previous exp'''
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, '')
                
                fit_score_categorical = float(fit_score_categorical[-1])
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, '')
                fit_score_numerical = float(fit_score_numerical[-1])
                
                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            # Pop out the assistance prompt of sematic fit 
            model.conversation.pop()

             # Pop out the user prompt of sematic fit
            model.conversation.pop()

        '''Add the results'''
        result2.append(actual_fit)
        result2.append(round(avg2/sentence_no,2))

        result1.append(actual_fit)
        result1.append(round(avg1/sentence_no,2))

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        # Save the sentences
        data.save_result(sentence_filename, result3)
        
        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

def exp_simple_gen_sentences_other(filename: str, model: Model, model_name: str):
    
    '''Setting Preparation'''
    exp_name = 'gen_sentences'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','role_type','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1]  
        
    # Prepare files for the output 
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'
    
    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(sentence_filename):
        data.open_result_file(filename= sentence_filename, fields= ['predicate','argument','role_type','sentence 1','sentence 2','sentence 3','sentence 4','sentence 5'])
    
    for i in range(len(dataset)):

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()

        '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument , roleType)

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument, roleType]
        result2 = [predicate, argument, roleType]
        result3 = [predicate, argument, roleType]

        '''Generating Sentences Part'''
        sentences = fit_scoring.generate_sentence(model, model_name_only, predicate, argument, roleType)

        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:
            
            '''Storing Sentences'''
            result3.append(sentence)

            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, model_name_only, predicate, argument, roleType, sentence) 

            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'categorical', sentence)

                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'numerical', sentence)

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            else:
                '''Back off'''
                result1.append('')
                result2.append('')

                '''Retrieve the data from previous exp'''
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, roleType)

                fit_score_categorical = float(fit_score_categorical[-1])
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical
                
                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, roleType)
                
                fit_score_numerical = float(fit_score_numerical[-1])

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            # Pop out the assistance prompt of sematic fit 
            model.conversation.pop()

             # Pop out the user prompt of sematic fit
            model.conversation.pop()

        '''Add the results'''
        result2.append(actual_fit)
        result2.append(round(avg2/sentence_no,2))

        result1.append(actual_fit)
        result1.append(round(avg1/sentence_no,2))

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        # Save the sentences
        data.save_result(sentence_filename, result3)
        
        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')


'''Experiment 4'''
def exp_reasoning_gen_sentences_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
    '''Setting Preparation'''
    exp_name = 'gen_sentences'

    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    
    dataset_name = filename.split('.csv')[0]
    
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1]    
    
    # prepare files for output
    result_filename1 = f'Result/{exp_name}_reasoning_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_reasoning_categorical_{dataset_name}_{model_name_only}.csv'
    reason_filename = f'Result/reasons_with)_sentences_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    
    for i in range(1): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()

         '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument]
        result2 = [predicate, argument]
    
        '''Generating Sentences Part'''
        sentences = data.get_back_exp_result(sentence_filename, predicate, argument, '')
        sentences.pop(0)
        sentences.pop(0)

        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:

            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, model_name_only, predicate, argument, roleType, sentence) 

            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)
                
                '''Step-by-Step Reasoning'''
                fit_scoring.reasoning('reasons_for_ferretti_with_sentences',model,model_name_only,predicate, argument, roleType, reason_filename, sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'categorical', sentence)
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'numerical', sentence)


                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            else:
                '''Back off'''
                result1.append('')
                result2.append('')
                
                '''Retrieve the data from previous exp'''
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_reasoning_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, '')
                
                
                fit_score_categorical = float(fit_score_categorical[-1])

                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical
                
                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_reasoning_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, '')
                
                fit_score_numerical = float(fit_score_numerical[-1])

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            # Pop out the assistance prompt of sematic fit 
            model.conversation.pop()

             # Pop out the user prompt of sematic fit
            model.conversation.pop()
        
        '''Add the results'''
        result2.append(actual_fit)
        result2.append(round(avg2/sentence_no,2))

        result1.append(actual_fit)
        result1.append(round(avg1/sentence_no,2))

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
         '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

def exp_reasoning_gen_sentences_other(filename: str, model: Model, model_name: str):
    
    '''Setting Preparation'''
    exp_name = 'gen_sentences'

    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','role_type','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    
    if "gpt" in model_name:
        model_name_only = model_name.split('-')[0]
    else:
        model_name_only = model_name.split('/')[1]    
    
    # Prepare files for the output
    result_filename1 = f'Result/{exp_name}_reasoning_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_reasoning_categorical_{dataset_name}_{model_name_only}.csv'
    reason_filename = f'Result/reasons_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'
    
    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)

   
    for i in range(len(dataset)): 

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()
        
         '''TRACING'''
        print('predicate: ', predicate, 'argument: ', argument, 'roleType: ', roleType)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument , roleType)

        if IsExist1 and IsExist2:
            continue
            
        '''Result Preparation'''  
        result1 = [predicate, argument,roleType]
        result2 = [predicate, argument,roleType]

        '''Generating Sentences Part'''
        sentences = data.get_back_exp_result(sentence_filename, predicate, argument, roleType)
        sentences.pop(0)
        sentences.pop(0)
        sentences.pop(0)

        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:

            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, model_name_only, predicate, argument, roleType, sentence) 

            '''Sematically Fit Sentence'''
            if is_semantic:  
                
                '''Reasoning'''
                fit_scoring.reasoning('with_sentence',model,model_name_only,predicate, argument, roleType, reason_filename, sentence)
        
                result1.append(sentence)
                result2.append(sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'categorical', sentence)
                
                result2.append(fit_score_categorical)
                if fit_score_categorical != None:
                    avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, model_name_only, predicate, argument, roleType, 'numerical', sentence)

                result1.append(fit_score_numerical)
                if fit_score_numerical != None:
                    avg1 += fit_score_numerical
                    
                # Pop out the assistance prompt of sematic fit 
                model.conversation.pop()

                 # Pop out the user prompt of sematic fit
                model.conversation.pop()
                
                 # Pop out the reasoning 
                model.conversation.pop()
                model.conversation.pop()
                model.conversation.pop()
                model.conversation.pop()
                model.conversation.pop()
                model.conversation.pop()
                    
            else:
                '''Back off'''
                result1.append('')
                result2.append('')
                
                '''Retrieve the data from previous exp'''
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_reasoning_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, roleType, occurance_execute, occurance_teach)
                
                if fit_score_categorical[-1] != '':
                    fit_score_categorical = float(fit_score_categorical[-1])
                    avg2 += fit_score_categorical
                else:
                    fit_score_categorical = ''
                
                result2.append(fit_score_categorical)
                
                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_reasoning_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, roleType, occurance_execute, occurance_teach)
                
                if fit_score_numerical[-1] != '':
                    fit_score_numerical = float(fit_score_numerical[-1])
                    avg1 += fit_score_numerical
                else:
                    fit_score_numerical = ''
                    
                result1.append(fit_score_numerical)
                
                # Pop out the assistance prompt of sematic fit 
                model.conversation.pop()

                 # Pop out the user prompt of sematic fit
                model.conversation.pop()

        '''Add the results'''
        result2.append(actual_fit)
        result2.append(round(avg2/sentence_no,2))

        result1.append(actual_fit)
        result1.append(round(avg1/sentence_no,2))

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

