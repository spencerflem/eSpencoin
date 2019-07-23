import textPlayer as tp
t = tp.TextPlayer('games/zork1.z5')
start_info = t.run()
command_output = t.execute_command('go north')
print(command_output)
if t.get_score() != None:
    score, possible_score = t.get_score()
t.quit()