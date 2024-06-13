import math
import pandas as pd

#Scan the list of completed matches, count the wins and losses of each competitor. In case of a tie, break it with the head-to-head match. Print order list and save.
def results(CL,dft):
    #dict --> {contestant:[wins,losses]}
    records_dict = {}
    for contestant in dft:
        print(contestant)
        records_dict[str(contestant)] = [0,0]

    print(records_dict)


    for match in CL:
        #If the first contestant won
        c1 = match[0]
        c2 = match[1]
        winner = match [2]

        w_c1 = w_c2 = l_c1 = l_c2 = 0
        # find current wins and losses of c1
        w_c1 = records_dict[str(c1)][0]
        l_c1 = records_dict[str(c1)][1]
        # find current wins and losses of c2
        w_c2 = records_dict[str(c2)][0]
        l_c2 = records_dict[str(c2)][1]
        #increment wins and losses as appropriate
        if winner == 1:
            w_c1 += 1
            l_c2 += 1
        else:
            l_c1 += 1
            w_c2 += 1

        records_dict[str(c1)] = [w_c1,l_c1]
        records_dict[str(c2)] = [w_c2,l_c2]

    print(records_dict)



# Run the contest
# Loop over the list of uncontested lists, asking user for the winner, store the result. Remove a contested match from the uncontested list and move to the completed list. If the user selects 'q' at any time, save the two lists for future use.
def contest(UL,dft):
    CL = [] #contested list
    remaining = UL.copy()
    print(UL)

    for match in UL:
        print(f"Current Match: {match}")


        c1 = match[0]
        c2 = match[1]
        print("\n --------- 1.", c1, "vs. 2.", c2)
        print("Enter the number of the winner")
        winner = -1
        while winner != 1 and winner !=2:
            winner = int(input())
            if(winner != 1 and winner !=2): print('invalid input. Try again.')

        CL.append([c1,c2,winner])
        print(remaining.pop(0))

    print(CL)
    results(CL,dft)


    
# As a check, if the list is of length n, the number of matches should be (n*(n-1))/2
# Store each matchup as a list with three elements: [C1, C2, Status]. This creates the list of uncontested lists.
# Status: 0 = Match not contested
#         1 = C1 wins
#         2 = C2 wins

def rr(cfile = 'TrekMovies.txt'):
    # Import the list of competitors and place in an numbered dict 
    df = pd.read_csv(cfile,header=None)
    print(df.columns)
    dft = df[0].tolist()
    n = len(dft)
    print(f'We have {n} competitors')
    uncontested_list = []
    
    #create_matches(dft)
    # Loop over the list, creating all possible matchups, being sure not to double count.
    # loop over the list
    list_position = 0
    for outer in dft:
        # for each item in the list, loop over the other items to create matches
        # Then, pop this item off the list
        if len(dft) > 1:
            list_position += 1
            dft_tmp = dft[list_position:]
            print(f'Length of dft is {len(dft)}')
            #print(dft)
            print(f'Length of dft_temp is {len(dft_tmp)}')
            #print(dft_tmp)
            for inner in dft_tmp:
                print(outer, ", ", inner)
                uncontested_list.append([outer,inner,0])

    check_sum = (n*(n-1))/2
    lul = len(uncontested_list)
    print(f'Length of UL should be {check_sum}. Lenth is: {lul}')
    print(uncontested_list)
    contest(uncontested_list,dft)

if __name__ == '__main__':
    rr('Flavors.txt')