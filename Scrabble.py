"""
CSE 231 Project 8
In this project, we will be creating a scrabble word generator. The goal of this generator
is to give all possible words that are able to be created by the letters in the player's rack,
and by the letters already on the board. The generator will take the input from the user if
they want to enter an example case. The code will then take the user input for the file that
we will be generating the words from (most common 3000 scrabble words). After the user enters
the file, the code will then prompt for the letters in the rack then the letters on the board.
The code will return, in descending order, the set of words by points, and the set of words by
length. The code will then prompt the user if they want another example case, in which if yes
they will be reprompted for the same, and if no, we print the goodbye message and end the code.
"""
BANNER="Scrabble Tool"
SCORE={'a':1, 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1,'s':1,'t':1, 'u':1, 'v':4, 'w':4, 'x':8, 'y':4, 'z':10}
import itertools
from operator import itemgetter
#These are our global variables used in the functions and used to iterate/sort
def open_file():
    """
    The purpose of this function is to open a file that the user inputs. We prompt the user to
    input a filename, and the code looks for the file in the computer. If the file is found, the
    file is opened and read, and if it is not, we print the file not found message and reprompt
    the user to enter a valid file. Open file functions are the first necessary step to many
    of our problems.
    """

    filefound=False
    filename = input("Input word file: ")
    #Prompt for user input
    while (filefound==False):      
        try:
            fp = open(filename)
            return fp
        except FileNotFoundError:
            #Try and except most useful for open file functions
            print("File not found. Try again.")
            filename = input("Input word file: ")
            #Reprompt the user for a valid file


def read_file(fp):
    """
    The read file function will pass in a file pointer returned by the open file function
    and read the data. In this case, the function will create an empty dictionary and
    take each line and strip it and make it lowercase for simplicity. We then need to
    make sure that it is not taking words less then length 3 and not taking words with
    apostrophes or dashes. We then add the words to the dictionary and return the dictionary
    """
    scrabble_word_dict={}
    #Creating empty dictionary
    for line in fp:
        #Going through each line in file
        word=line.strip().lower()
        if len(word)>=3 and '-' not in word and "'" not in word: 
            #Setting our requirements to be added to the dictionary
            scrabble_word_dict[word]=1
    return scrabble_word_dict
#We return the newly created dictionary for each input case
            

def calculate_score(rack,word):
    """
    This function will be used to calculate the score from the user inputted rack and
    words already on the board. We do this by using our global variable SCORE dictionary
    that has a key for each letter with its corresponding point value. We run through this
    dictionary and create the new score by adding the score of the corresponding letter
    from the given rack. We then set the requirements that if the length of the rack
    is 0 meaning all letters were used, the bonus of 50 points is applied. For each letter
    in the word, we want to use the replace method to see if all tiles in the rack are
    used. The function will return the newly added score for the rack and words.
    """
    len_rack=len(rack)
    score=0
    #Need local variables to build off of
    for ch in word:
        score_letter=SCORE[ch]
        #Corresponding score in the global dictionary used for each letter
        score=score+score_letter
        #Gives us the score of the letters added

    for ch in word:
        rack=rack.replace(ch,'',1)
        #The replace method mentioned
        
    if len(rack)==0 and len_rack==7:
        #If all tiles used, they get a bonus of 50
        score=score+50
    return score
    

def generate_combinations(rack,placed_tile):
    """
    This function finds all combinations of a string (combined rack and placed_tile) with
    length of at least 3, with longest being 9. We collect combinations in a set, but 
    do not include combinations that do not have the placed_tile.
    """
    pos_tiles = rack + placed_tile
    combos = set()
    #Creating the empty set to return
    for i in range(3,len(pos_tiles)+1):
        #Our length of at least 3, and max length of however long possible
        
        for x in itertools.combinations(pos_tiles, i):
            #We use the itertools to generate combos of words from the file, iterate using a for loop
            if placed_tile in x or placed_tile == "":
                combos.add(x)
    return combos

def generate_words(combo,scrabble_words_dict):    
    """
    This function takes a list of characters from the input combo and finds all permutations
    of the characters.  However, only those permutations that are valid English words are added
    to an empty set we create. The dictionary we created by reading the file is the second parameter,
    scrabble_words_dict. This is the dictionary of the 3000 words. We then use the permutation function
    given by Python to find these words and add them to the set, then return the set.
    """
    set_words=set()
    #Need empty set
    for value in combo:
        for w in itertools.permutations(value):
            #Use the given Python function to take the input and permutate it
            word=''.join(w)
            #Must create the word using this, join the permutated string to an empty string
            if word in scrabble_words_dict:
                #If this word we generated is in the 3000 word dictionary, we add it to the set
                set_words.add(word)
    return set_words
#We return this new set of added, valid words

def generate_words_with_scores(rack,placed_tiles,scrabble_words_dict):
    """
    This function will take a string provided by the user, the placed tile, and thevscrabble
    words dictionary returned by read file. We generate combos, make sure they're valide and
    add them to the set, then pass the set through this function to create a new dictionary of
    each valid word with its score. We find this score by using the calculate score function
    in thos function, which is a common thing to do with these problems. 
    """
    scores={}
    #Create empty dictionary
    if (len(placed_tiles)!=0):
        #If the placed tiles exist
        for placed_tile in placed_tiles:

            combos=generate_combinations(rack,placed_tile)
            #Create the combos of all words
            set_words=generate_words(combos,scrabble_words_dict)
            #Make sure the words are valid for our inputs
    
            for word in set_words:
                score=calculate_score(rack,word)
                #Add the word to our dictionary
                #Calculate the score of these valid words using our calculate score fucntion
                scores[word]=score

    else:
        
        combos=generate_combinations(rack,placed_tiles)
        set_words=generate_words(combos,scrabble_words_dict)
        #For tiles not placed
       
        for word in set_words:
                score=calculate_score(rack,word)
                scores[word]=score
                #Add the word to our dictionary
                #Calculate the score of these valid words using our calculate score fucntion

    return scores
#We return the dictionary of valid words with their key of calculated scores

def sort_words(word_dic):
    """
    This function will take the new dictionary created by our former function and return two lists.
    These lists will be lists of tuples. Our lists will differ in the sense that one must display 
    the score of the word if played, and the other will display the length of the word if played.
    These lists basically show potential results from two different standpoints. We will sort the first
    and second tuples using the itemgetter method as we usually do in these problems. We will return
    2 lists sorted by score and length
    """
    sorted_score_list=[]
    sorted_wordlength_list=[]
    #Creating the 2 new lists
    
    for word in word_dic:
        score=word_dic.get(word)
        len_word=len(word)
        scrabble_tuple=()
        #Creating our tuple for the data
        scrabble_tuple=(word,score,len_word)
        sorted_score_list.append(scrabble_tuple)
        #We append this tuple to the list for score
        sorted_wordlength_list.append(scrabble_tuple)
        #We append this tuple to the list for length

    sorted_score_list.sort(key=itemgetter(0))
    #We must do a primary sort first
    sorted_score_list.sort(key=itemgetter(1,2),reverse=True)
    #We then sort the list by score and length using the indexes 1 and 2 for the tuples, in descending order

    sorted_wordlength_list.sort(key=itemgetter(0))  
    #We do the same thing for the length list as the score list.
    sorted_wordlength_list.sort(key=itemgetter(2,1),reverse=True)
  
    return sorted_score_list,sorted_wordlength_list
#We return the two very similar lists for the user

def display_words(word_list,specifier):
    """
    The purpose of this function is to display the words from the lst we just created in 
    the former function. We want to display each word in a specific format for the user,
    and we only want to display the top 5 options from the list. If the generated list
    is less than 5 options, we display all the options. We then use given format strings to
    display this data.
    """
    print("Word choices sorted by "+specifier)
    print("{:>6s}  -  {:s}".format(specifier,'Word'))
    #Formatting our display

    for word in word_list[:5]:
        #Top 5 options from the list
        element1=''
        element2=word[0]

        if specifier=='Score':
            #Data for score not length
           element1=word[1]
           #If it equals score it goes in the first index to display score on left or length on left
        else:
           element1=word[2]
           #If it equals word it goes in the second index
             
        print("{:>6d}  -  {:s}".format(element1,element2)) 

def main():
       
    """
    This function is what makes the code work. We first print our banner, then ask the user
    if they want an example. If so, we prompt for a file, which they will input until correct.
    Then, we will prompt them for the rack, then prompt them for any tiles already on the board.
    The main then calls on our functions to create the words, sort them, add them to the set,
    add scores to them, create lists from these, and then displaying the list in our proper
    formatting. We then ask if the user wants another exampke done, and if the answer is yes, we reloop.
    If the answer is no, we print our goodbye message and end the code.
    """
    continue_game=False
    print(BANNER)
    #We print our banner
    choice=input("Would you like to enter an example (y/n): ").lower()
    #Prompt for input, make it lowercase for simplicity
    if choice=='y':
        continue_game=True
 
    while continue_game==True:
       all_scrabble_word_dict_scores={}
       fp=open_file()
       scrabble_dict=read_file(fp)
       #Create the dictionary needed from read file and the file pointer

       valid_rack_input=False
       while (valid_rack_input==False):
              rack=input("Input the rack (2-7chars): ")
              #Prompt for rack
              if rack.isalpha():
                  #If the rack exists and isn't a number, continue
                 if len(rack)>=2 and len(rack)<=7:
                     #If the rack is the proper length for our example
                    valid_rack_input=True
                 else: 
                    print("Error: only characters and 2-7 of them. Try again.")
              else:
                 print("Error: only characters and 2-7 of them. Try again.")
  
       placed_tiles=input("Input tiles on board (enter for none): ")
       #Prompt for tiles already on board, or take enter as none

       all_scrabble_word_dict_scores=generate_words_with_scores(rack,placed_tiles,scrabble_dict)
       #We generate the words with scores using these inputs

       word_scores,word_lengths=sort_words(all_scrabble_word_dict_scores)
       #We use sort words function to create the lists we want to return with the newly calculated scores
  
       display_words(word_scores,'Score')
       #We display the words for score
       print()
       display_words(word_lengths,'Length')
       #We display the words for length
       choice=input("Do you want to enter another example (y/n): ").lower()
       if choice=='n':
          continue_game=False
    print("Thank you for playing the game")

if __name__ == "__main__":
    main()
