
def get_attributes(file_path):

    attribute = []
    prev_pos = 0
    define_line = ""

    with open(file_path,'r+') as file:
        for line in file:
            if (line[0]=="A"):
                define_line = ""
                extracted_words = line.split()
                pos = int(extracted_words[0][-1])
                if (prev_pos != pos):
                    tmp = []
                    prev_pos = pos
                    attribute.append(tmp)
                    
                extracted_words.insert(0,"#define")
                extracted_words.insert(2,"Cyber")
                extracted_words.insert(4,"=")
                for x in extracted_words:
                    define_line += x + " "
                tmp.append(define_line)
    
    file.close()
    return attribute

def attribute_combination(attributes):

    combinations = 1

    for i in range(len(attributes)):
        combinations *= len(attributes[i])

    rows, cols = len(attributes), combinations

    combination_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    count = 0
    
    for i in range(len(attributes)):
        count = 0
        if (i == 0):
                iterations = 1
        else:
            iterations *= len(attributes[len(attributes)-i])
            #print(iterations)
        for j in range(0, combinations, iterations):

            for k in range(iterations):
                #print(len(attributes)-i-1," ", j+k, " ", len(attributes)-i-1, " ", count )
                combination_matrix[len(attributes)-i-1] [j+k] = attributes [len(attributes)-i-1] [count]
                
            
            if (count < len(attributes[len(attributes)-i-1])-1):
                count = count + 1
            else:
                count = 0              

    return combination_matrix, combinations