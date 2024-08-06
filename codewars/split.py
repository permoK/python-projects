def points(games):
    x_scores = []
    y_scores = []
    for i in games:
        game = i.split(":")
        # print(game)

        win = 3
        loose = 0
        draw = 1


        x_games = int(game[0])
        y_games = int(game[1])
    
        # print(x_games)
        # print(y_games)

        if x_games > y_games:
            x_scores.append(win)
        elif x_games < y_games:
            y_scores.append(win)
        else:
            y_games.append(draw)
            x_games.append(draw)
    # print(x_scores)
    # print(y_scores)

    return sum(x_scores)

games = ['1:0','2:0','3:0','4:0','2:1','3:1','4:1','3:2','4:2','4:3']

print(points(games))
