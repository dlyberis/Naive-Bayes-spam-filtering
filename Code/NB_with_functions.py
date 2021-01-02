import os
from math import log
from numpy import finfo

def update_vocabulary(file_path, vocabulary):
    '''
    open a file and checks every word of a document that is digit and
    put it in a dictionary as a key, if it is not already in there in dictionary.
    Also counts the appearence frequency of each word and store it as value of the specific key
    Parameters
    ----------
    doc_path (string)
        Path of the given file 
    vocabulary (dictionary)
        The list which contains the words and their appearence frequency.
    ----------
    Return
    ----------
    vocalulary (dictionary)
        The initial dictionary after update
    '''
    # open file
    with open(file_path,'r') as doc:
        # for each line of the document
        for line in doc:
            # create a list with the words of each line
            line_words_lists = line.strip('\n\t').split(" ")
            # put the words in vocabulary (dictionary)
            for word in line_words_lists:
                if word.isdigit():
                    if word in vocabulary:
                        vocabulary[word] += 1
                    else:
                        vocabulary[word] = 1
    return vocabulary

def calc_posterior_pos(vocabulary,spam_vocabulary,legit_vocabulary,posterior_pos_spam,posterior_pos_legit):
    '''
    Calculate posterior possibilities of words in spam and legit docs
    with smoothing to prevent dividing by zero.
    ----------
    vocabulary (dictionary)
        A dictionary which contains all of the words of all training documents.
        Each word is stored as a key and its Frequency of occurrence in all
        training documents as a value.
    spam_vocabulary (dictionary)
        A dictionary which contains all of the words of all spam documents in training set.
        Each word is stored as a key and its Frequency of occurrence in all spam documents
        as a value.
    legit_vocabulary (dictionary)
        A dictionary which contains all of the words of all legit documents in training set.
        Each word is stored as a key and its Frequency of occurrence in all spam documents
        as a value.
    ----------
    Return
    ----------
    posterior_lists (list)
        A list which contains the lists of posterior possibilities of spam and legit words
    '''
    for key in vocabulary:
        if key in spam_vocabulary:
            posterior_pos_spam[key]=(spam_vocabulary.get(key)+1)/(sum(spam_vocabulary.values())+len(vocabulary))
        else:
            posterior_pos_spam[key]=(0+1)/(sum(spam_vocabulary.values())+len(vocabulary))
        if key in legit_vocabulary:
            posterior_pos_legit[key]=(legit_vocabulary.get(key)+1)/(sum(legit_vocabulary.values())+len(vocabulary))
        else:
            posterior_pos_legit[key]=(0+1)/(sum(legit_vocabulary.values())+len(vocabulary))
    posterior_lists=[posterior_pos_spam,posterior_pos_legit]
    return posterior_lists


def naive_bayes(test_file_path,vocabulary,posterior_pos_spam,posterior_pos_legit,prior_pos):
    '''
    This Function uses naive bayes method to predict the target class of a new email file.
    ----------
    test_file_path (str)
        The path of the file that is going to be tested.
    ----------
    Return
    ----------
    predict_file (str)
        The target class that naive bayes classifies the file, "spam" or "legit.
    '''
    Vnb_spam=0
    Vnb_legit=0
    temp_spam=0
    temp_legit=0
    predict_file=""
    # open file
    with open(test_file_path,'r') as test_doc:
        # for each line of the document
        for line in test_doc:
            # create a list with the words of each line
            line_words_lists = line.strip('\n\t').split(" ")
            # put the words in vocabulary (dictionary)
            for word in line_words_lists:
                if word.isdigit() and (word in vocabulary):                             
                    temp_spam += log(posterior_pos_spam.get(word))
                    temp_legit += log(posterior_pos_legit.get(word))
    Vnb_spam=log(prior_pos.get('prior_spam'))+temp_spam
    Vnb_legit=log(prior_pos.get('prior_legit'))+temp_legit
    if (Vnb_spam>Vnb_legit):
        predict_file="spam"
    elif (Vnb_spam<Vnb_legit):
        predict_file="legit"
    return predict_file

def update_prediction_counters(predict_status,ident_spam,ident_legit,test_email,total_spam,cor_ident_spam,total_legit,cor_ident_legit):
    # update counters
    if(predict_status=="spam"):
        ident_spam +=1
    elif(predict_status=="legit"):
        ident_legit +=1
    if "spmsg" in test_email:
        total_spam += 1
        if predict_status=="spam":
            cor_ident_spam +=1
    elif "legit" in test_email:
        total_legit += 1
        if predict_status=="legit":
            cor_ident_legit +=1
    return [ident_spam,ident_legit,total_spam,cor_ident_spam,total_legit,cor_ident_legit]

def create_vocabulary(train_set,root,root_folder,vocabulary,spam_vocabulary,legit_vocabulary,total_docs,spam_docs,legit_docs):
    for sub_folder in train_set:
        # get a list with emails of the current sub_folder
        folder_files = os.listdir(r"{}".format(os.path.join(os.path.join(root, root_folder), sub_folder)))
        # update total files counter
        total_docs += len(folder_files)
        for email in folder_files:
            file_path = r"{}".format(os.path.join(os.path.join(os.path.join(root,root_folder),sub_folder),email))
            # update spam and legit email counters
            if "spmsg" in email:
                spam_docs += 1
                update_vocabulary(file_path,spam_vocabulary)
            elif "legit" in email:
                legit_docs += 1
                update_vocabulary(file_path,legit_vocabulary)     
            # update vocabulary
            update_vocabulary(file_path,vocabulary)
    return [vocabulary,spam_vocabulary,legit_vocabulary,total_docs,spam_docs,legit_docs]

# The directory which contains the datasets
root = r'C:\Users\Dimitris\Documents\Master\Machine Learning\ML_Project_03\pu_corpora_public'

def main(root):
    # Create a list with the subdirectories of the main_dir
    entries = os.listdir(root)

    # Keep only the folders in the list
    for direc in entries:
        if os.path.isfile(os.path.join(root,direc)):
            entries.remove(direc)

    # K- fold for all main folders 'pu1', 'pu2', 'pu3', 'pua'     
    for root_folder in entries:
        print('Φάκελος προς έλεγχο: {}\n'.format(root_folder))
        fold_spam_recall=[]
        fold_spam_precesion=[]
        total_spam_recall=0
        total_spam_precision=0
        # list which contains only the subfolders part1-part10
        email_folders = [x for x in os.listdir(os.path.join(root,root_folder)) if os.path.isdir(os.path.join(os.path.join(root,root_folder),x))]
        # remove unused folder from the list
        email_folders.remove('unused')
        # 10-fold validation
        for k in range(10):
            # split folders for training and testing in each fold.
            # for e,f in enumerate (email_folders):
            test_set = email_folders[k]
            train_set = [x for x in (email_folders) if x!=test_set]
            print('Training Set: {}\nTest Set: {}'.format(train_set,test_set))
            # initialize counters and dictionatries for the current training set
            vocabulary={}
            spam_vocabulary={}
            legit_vocabulary={}
            prior_pos={}
            posterior_pos_spam={}
            posterior_pos_legit={}
            total_docs = 0
            spam_docs = 0
            legit_docs = 0
            # For each folder of the training set read all of the emails
            # and create a vocabulary with the words contained in emails.
            [vocabulary,spam_vocabulary,legit_vocabulary,total_docs,spam_docs,legit_docs] = \
            create_vocabulary(train_set,root,root_folder,vocabulary,spam_vocabulary,legit_vocabulary,total_docs,spam_docs,legit_docs)
            #Calculate prior possibilities
            prior_pos["prior_spam"]=spam_docs/total_docs
            prior_pos["prior_legit"]=legit_docs/total_docs
            #Calculate posterior possibilities of spam and legit with smoothing
            [posterior_pos_spam,posterior_pos_legit]=calc_posterior_pos(vocabulary,spam_vocabulary,legit_vocabulary,posterior_pos_spam,posterior_pos_legit)

            # testing process
            test_folder_files = os.listdir(r"{}".format(os.path.join(os.path.join(root, root_folder), test_set)))
            total_spam = 0
            total_legit = 0
            ident_spam = 0
            ident_legit = 0
            cor_ident_spam=0
            cor_ident_legit=0
            for test_email in test_folder_files:
                predicted_status=""
                # test file path
                test_file_path = r"{}".format(os.path.join(os.path.join(os.path.join(root, root_folder), test_set),test_email))
                # predict test file 
                predicted_status=naive_bayes(test_file_path,vocabulary,posterior_pos_spam,posterior_pos_legit,prior_pos)
                # update counters
                [ident_spam,ident_legit,total_spam,cor_ident_spam,total_legit,cor_ident_legit] = \
                update_prediction_counters(predicted_status,ident_spam,ident_legit,test_email,total_spam,cor_ident_spam,total_legit,cor_ident_legit)
            # Calculate spam recall and spam precesion for each fold and store the in a list
            #print('cor_ident_spam:{} total_spam:{}\n'.format(cor_ident_spam,total_spam))
            fold_spam_recall.append(cor_ident_spam/(total_spam+finfo(float).eps))
            fold_spam_precesion.append(cor_ident_spam/(ident_spam+finfo(float).eps))
            print('Testing στον Φάκελο: {},\ntotal_test_spam_doc: {}, ident_spam: {}, cor_ident_spam: {}\n'.format(test_set,total_spam,ident_spam,cor_ident_spam))
        total_spam_recall = sum(fold_spam_recall)/len(fold_spam_recall)
        total_spam_precision = sum(fold_spam_precesion)/len(fold_spam_precesion)
        print('----------------------------------------------')
        print ('Για τον Φάκελο: {}\nSpam_recall: {:.02f}\nSpam_precision: {:.02f}\n'.format(root_folder,total_spam_recall*100,total_spam_precision*100))
        print('----------------------------------------------')         

if __name__ =="__main__":
    main(root)