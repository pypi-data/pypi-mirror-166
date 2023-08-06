import re
import nltk
import unicodedata
nltk.download('stopwords')


def find_hashtags(text):
    '''extract a list of hashtags, and remove punctuations'''
    punctuation_ls = "!\"$%&'()*+,-/.:;<=>?[\]^`{|}~"
    hashtags_list = []
    temp_list = []
    counter = 0
    split_text = re.findall(r"\w+|#\w+|@\w+|[!\"$%&'()*+,-/.:;<=>?[\]^`{|}~]", text) # split based on punctuation and whitespace 
    clean_split_text = [elem for elem in split_text if elem not in punctuation_ls]
     
    for index,part in enumerate(clean_split_text):  
        if part.startswith('#'):   # hashtag is found  
            temp_list.append(part[1:])
            counter += 1
            # check if the word is the last word in the text
            if index == len(clean_split_text)-1:
                if counter>=3:
                    hashtags_list.extend(temp_list)
                    del clean_split_text[index-counter+1:index+1] 
                else:
                    break
            continue
            
        else:  # encounter a non-hashtag
            if counter >= 3:  # add hashtags from temp to hashtags_list  
                hashtags_list.extend(temp_list)
                del clean_split_text[index-counter+1:index+1]
                temp_list = []
                counter = 0
                continue
            else: # delete the hashtags from temp_list
                temp_list = []
                counter = 0
                continue
    return hashtags_list," ".join(clean_split_text)


def hashtags(text):
    hashtagslist,_ = find_hashtags(text)
    return {"hashtags":hashtagslist}

# ----------------------------------------------------

def replace_hashtags(text):
    '''remove the hashtags'#' within the main caption''' 
    text = text.replace("#","")
    return text


def replace_usernames(text):
    '''define a function to detect mentions and replace it with <username>'''
    cleanedText = re.sub(r'(?<![@\w])@(\w{1,30})',"<username>",text)
    return cleanedText

    
def remove_stopwords(text, language, warning=True):
    try:
        stopwords_set = set(nltk.corpus.stopwords.words(language))
        filtered_words = [word.lower() for word in text.split() if word.lower() not in stopwords_set]
        text = " ".join(filtered_words)
        return text
    
    except OSError:
        if warning:
            print("Language stopwords database not found! Stopwords not removed.")
        return spacing_fix(text)

    
def spacing_fix(text):
    text = " ".join(text.split())
    return text


def fix_fonts(text):
    text = unicodedata.normalize('NFKC', text)
    return text


def clean_text(text, language):
    
    # Remove irrelevant components of text
    _,text = find_hashtags(text)
    text = replace_hashtags(text)
    text = replace_usernames(text)
    text = remove_stopwords(text,language)
    text = fix_fonts(text)
    
    # Filter text that are too short
    if len(text)<=2 or text==None:
        text = ''
        return {"clean_text":text}
    else:
        return {"clean_text":text}


def text_length(text,language):
    textobj = clean_text(text,language)
    return {"text_length":len(textobj["clean_text"])}


def clean_data(text,language):
    res1 = hashtags(text)
    res2 = clean_text(text,language)
    res3 = {"text_length": len(res2["clean_text"])}
    res = {}
    res.update(res1)
    res.update(res2)
    res.update(res3)
    return res 