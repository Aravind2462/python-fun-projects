#displaying the board
def display_board(board):
    print(f'           {board[7]} | {board[8]} | {board[9]} ')
    print('          ---+---+---')
    print(f'           {board[4]} | {board[5]} | {board[6]} ')
    print('          ---+---+---')
    print(f'           {board[1]} | {board[2]} | {board[3]} ')
    print("\n")

    
#selecting player input
def player_input():
    player_in = 'error'
    while player_in != 'x' and player_in != 'o':
        player_in = input("Player-1 select the 'X' or 'O' : ")
        if player_in != 'x' and player_in != 'o':
            print("please enter the correct value ") 
    player1 = player_in.upper()
    if player1 == 'X':
        player2 = 'O'
    else:
        player2 = 'X'
    return (player1,player2)
    

#place the input at the position
def place_marker(board, marker, position):  
    
    board[position] = marker


#check is this win or not
def win_check(board, mark): 
    if board[1] == mark and board[2] == mark and board[3] == mark: #chick horizontal 1 
        return True
    elif board[4] == mark and board[5] == mark and board[6] == mark: #chick horizontal 2 
        return True
    elif board[7] == mark and board[8] == mark and board[9] == mark: #chick horizontal 3 
        return True
    elif board[1] == mark and board[4] == mark and board[7] == mark: #chick vertical 1 
        return True
    elif board[2] == mark and board[5] == mark and board[8] == mark: #chick vertical 2
        return True
    elif board[3] == mark and board[6] == mark and board[9] == mark: #chick vertical 3
        return True
    elif board[1] == mark and board[5] == mark and board[9] == mark: #chick vertical 2
        return True
    elif board[3] == mark and board[5] == mark and board[7] == mark: #chick vertical 3
        return True
    


#checking the posision is free
def space_check(board, position): 
    
    return board[position] == ' '

#checking the board is full
def full_board_check(board): 
    for i in board:
        if i == ' ':
            return False
    return True

#getting next position from player
def player_choice(board,player): 
    check = ('1','2','3','4','5','6','7','8','9')
    a = 0
    while True:
        a = 0
        while a not in check:
        
            a = input(f'player-{player} select your position 1 to 9: ')
            if a in check:
                a = int(a)
                if space_check(board, a):
                    return a
                else:
                    print('opps its already selected please select remaining numbers')
            else:
                print(f'player-{player} please select the number 1 to 9')

#asking for replay              
def replay(): 
    check = 'check'
    while check != 'y' and check != 'n':
        check = input("Do you want to replay enter 'y' or 'n' :")
        check = check.lower()
        if check != 'y' and check != 'n':
            print('please enter the correct value')
    if check == 'y':
        clear_output()
        print("\n\n")
        return True
    else:
        return False


#game flow
import os
clear_output = lambda: os.system("cls")
clear_output()
print("\n\nWELCOME TO 'TIC TOC TOE' GAME")

while True:
    av_nums = {1,2,3,4,5,6,7,8,9}
    board = ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    print("\n")
    display_board(board)
    player1,player2 = player_input()
    while not full_board_check(board):
        clear_output()
        #player 1 process
        print("\n")
        print("\n")
        print('     player 1 its your turn')
        print("\n")
        display_board(board)
        p1 = player_choice(board, 1)
        place_marker(board, player1, p1)
        if win_check(board, player1):
            clear_output()
            print("\n")
            print("\n")
            print('     player1 is the winner!')
            print("\n")
            display_board(board)
            break
        display_board(board)
        if full_board_check(board):
            clear_output()
            print("\n")
            print("\n")
            print("          Match draw")
            print("\n")
            display_board(board)
            break
            
        #player 2 process
        clear_output()
        print("\n")
        print("\n")
        print('     player 2 its your turn')
        print("\n")
        display_board(board)
        p2 = player_choice(board, 2)
        place_marker(board, player2, p2)
        if win_check(board, player2):
            clear_output()
            print("\n")
            print("\n")
            print('     player 2 is the winner!')
            print("\n")
            display_board(board)
            break
        display_board(board)
        if full_board_check(board):
            clear_output()
            print("\n")
            print("\n")
            print("          Match draw")
            print("\n")
            display_board(board)
            break
        
 
    if not replay():
        clear_output()
        print("\n")
        print("\n")
        print('     Thanks for playing')
        print("\n")
        print("\n")
        break
