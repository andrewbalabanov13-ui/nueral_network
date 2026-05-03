import random



def move_player_or_enemy(player_row,player_col,enemy_row,enemy_col,type,world,move_dir):
    max_row = len(world)
    max_col = len(world[0])
    if type == "p":
        row_x = player_row
        col_y = player_col
    elif type == "e":
        row_x = enemy_row
        col_y = enemy_col
    #0 = right
    #1 = left
    #2 = up
    #3 = down
    if move_dir == 0 and row_x != max_row - 1:
        row_x += 1
    elif move_dir == 1 and row_x != 0:
        row_x -= 1
    elif move_dir == 2 and col_y != 0:
        col_y -= 1
    elif move_dir == 3 and col_y != max_col - 1:
        col_y += 1
    
    if type == "p":
        player_row = row_x
        player_col = col_y
        if world[player_row][player_col] == "c":
            return (player_row,player_col,enemy_row,enemy_col,2)
    if type == "e":
        enemy_row = row_x
        enemy_col = col_y
    


    if player_row == enemy_row and player_col == enemy_col:
        return (player_row,player_col,enemy_row,enemy_col,1)
    return (player_row,player_col,enemy_row,enemy_col,0)

    
    
def run():
    player_row,player_col,enemy_row,enemy_col,world = setup()
    should_stop = 0
    move_dir = 0
    while should_stop == 0:
        #move player
        move_dir = random.randint(0,3)
        player_row,player_col,enemy_row,enemy_col,should_stop = move_player_or_enemy(player_row,player_col,enemy_row,enemy_col,"p",world,move_dir)
        if should_stop != 0:
            break
        #move enemy
        move_dir = random.randint(0,3)
        player_row,player_col,enemy_row,enemy_col,should_stop = move_player_or_enemy(player_row,player_col,enemy_row,enemy_col,"e",world,move_dir)

        # print("p " +  str(player_row),str(player_col))
        # print(enemy_row,enemy_col)
    
    if should_stop == 1:
        print("you lose")
    elif should_stop == 2:
        print("you win ")
        
    





def setup():
    world =[["a","a","a","a","a","a"],
            ["a","a","a","a","a","a"],
            ["a","a","a","a","a","a"],
            ["a","a","a","a","a","a"],
            ["a","a","a","a","a","a"],
            ["a","a","a","a","a","a"]]
    randRow,randCol = get_random_row_and_col(world)
    world[randRow][randCol] = "c"

    while world[randRow][randCol] == "c":
        randRow,randCol = get_random_row_and_col(world)

    player_row = randRow
    player_col = randCol
    for x in range(len(world)):
        print(world[x])

    while True:
        randRow,randCol = get_random_row_and_col(world)
        if not(player_row - 1 > randRow and player_row + 1 < randRow and player_col - 1 > randCol and player_col + 1 < randCol):
            enemy_row = randRow
            enemy_col = randCol

            break
        
        # if player_row - 1 > randRow and player_row + 1 < randRow        :
        #     if player_col - 1 > randCol and player_col + 1 < randCol:
        #         pass
        #     else:
                
        #         enemy_row = randRow
        #         enemy_col = randCol
        #         break
        # else:
        #     enemy_row = randRow
        #     enemy_col = randCol
        #     break

    return (player_row,player_col,enemy_row,enemy_col,world)

def get_random_row_and_col(world):
    return random.randint(0,len(world) - 1),   random.randint(0,len(world[0]) - 1)



run()