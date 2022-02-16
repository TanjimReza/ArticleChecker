import re
from pprint import pprint
from config import *
print(f"<--{'---x---'*10}-->")
print(f"\n<----{'-x-'*8} Article Checker {'-x-'*8}---->\n")
print(f"<--{'---x---'*10}-->\n\n")
word_error = {}
para_error = {}
answer_error = {}
FAQ_LINE = int(0)
# print(f"\n<---{'-x-'*20}--->")
with open('word.txt','r') as inputFile: 
    #!------------------- WORD -------------------!#
    print(f"\n::::::: Word Count Result :::::::\n")    
    text = inputFile.read().splitlines()
    for para in text: 
        line = re.split("[?!.:]",para)
        # print(line)
        for words in line: 
            countWords = len(words.split())
            # countWords = len(re.findall(r'\w+',words))
            if countWords > WORD_LIMIT: 
                word_error[countWords] = words
    if len(word_error) > 0: 
        print(f"Total {len(word_error)} Errors Found!\n\n")
        for word,desc in word_error.items():
            print(f"{word} : {desc}\n")
    else:
        print("-> No Word Errors Found!")
    #!--------------------------------------------!#
    print("\n")
# print(f"\n:::: Paragraph Character Result :::\n")    
with open('word.txt', 'r') as file:
    text = file.read().split("\n")
    
    #!------------------- META -------------------!#
    print(f"\n::::::: META Result :::::::\n")
    META_TEXT = text[0].lower()
    if META_TEXT == META_CHECK:
        print(f"-> Meta:",text[1],end="\n") #* The Line After META is META Para
        print("-> Meta Characters:",len(text[1]),end="\n")
        meta_char_count = len(text[1])
        if meta_char_count in META_LIMIT:
            print("-> No issues in META!")
        elif meta_char_count < min(META_LIMIT):
            print("-> META is TOO SHORT!")
        elif meta_char_count > max(META_LIMIT):
            print("-> META is TOO LONG!")
        else: 
            print("-> No issues in META!")
    else:
        print("-> No meta found! Skipping.")
    print("\n")
    #!--------------------------------------------!#
    #!------------------- FAQ -------------------!#
    print(f"::::::: FAQs Result :::::::\n")
    for count,paragraphs in enumerate(text,start=0): 
        if paragraphs == FAQ:
            FAQ_LINE = count
            break
    # print(text[FAQ_LINE]) #* The Line After FAQ is FAQ Para
    TEXT_AFTER_FAQ = text[FAQ_LINE+1:]
    # print(TEXT_AFTER_FAQ)
    for i in TEXT_AFTER_FAQ:
        if len(i) <= 0:
            TEXT_AFTER_FAQ.remove(i) 
    QUESTIONS = TEXT_AFTER_FAQ[::2]
    ANSWERS = TEXT_AFTER_FAQ[1::2]
    QUESTIONS = [QUESTIONS[i].replace("Question: ","").strip() for i in range(0,FAQ_COUNT)]
    ANSWERS = [ANSWERS[i].replace("Answer:","").strip() for i in range(0,FAQ_COUNT)]
    
    for answer in ANSWERS:
        count = len(answer)
        if count in FAQ_ANSWER_LIMIT_NO_ISSUE:
            continue
        else:
            if count < min(FAQ_ANSWER_LIMIT_ISSUE):
                answer_error[answer] = count
            elif count > max(FAQ_ANSWER_LIMIT_ISSUE):
                answer_error[answer] = count
    if len(answer_error) > 0:
        print(f"Total {len(answer_error)} Errors Found!\n")
        for answer,count in answer_error.items():
            print(f"{answer} : {count}\n")
    else: 
        print(f"No issues in FAQs!\n")
    print("\n")
    #!--------------------------------------------!#
print(f"<--{'---x---'*10}-->")
print(f"\n<----{'-x-'*10} END {'-x-'*10}---->\n")
print(f"<--{'---x---'*10}-->\n\n")