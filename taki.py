from random import shuffle
#Consts
REGULAR_DIRECTION = 1
OPPOSITE_DIRECTION = -1
RED = 0
BLUE = 1
GREEN = 2
YELLOW = 3
R_B_G_Y = 4
REGULAR = 0
TAKI = 10
SUPERTAKI = 11
CHANGECOLOR = 12
CHANGEDIR = 13
STOP = 14
PLUS2 = 15
NUMOFCARDS = 8
GAMEOVER = 1
NOTOVER = 0

class Game(object):
	def __init__(game, num_of_players):
		game.count_p2 = 1
		game.dir = REGULAR_DIRECTION
		game.deck = game.get_full_deck()
		shuffle(game.deck) #ToDo give cards to players 
		game.visible_card = game.get_single_card() #TODO make sure a valid starting card
		game.players = game.create_players(num_of_players)
		game.curr_player = game.players[0] #TODO add interactive number of the current player

	def get_full_deck(game):
		#craete card list
		#2 of each number and color
		#Add special cards:
			#2 taki for each color
			#2 CHANGEDIR for each color
			#2 change color
			#2 SUPERTAKI
			#PLUS2 for each color
		deck = []
		for color in xrange(4):
			for num in xrange(1,10):
				deck.append(Card(color,num))
				deck.append(Card(color,num))
		#Add all special
			deck.append(Card(color,STOP))
			deck.append(Card(color,STOP))
			deck.append(Card(color,CHANGEDIR))
			deck.append(Card(color,CHANGEDIR))
			deck.append(Card(color,TAKI))
			deck.append(Card(color,TAKI))
			deck.append(Card(color,PLUS2))
			deck.append(Card(color,PLUS2))
		deck.append(Card(R_B_G_Y,SUPERTAKI))
		deck.append(Card(R_B_G_Y,SUPERTAKI))
		deck.append(Card(R_B_G_Y,CHANGECOLOR))
		deck.append(Card(R_B_G_Y,CHANGECOLOR))
		return deck
	
	def get_single_card(game):
		card = game.deck.pop()
		return card

	def create_players(game, num_of_players):
		#craete deck of num of cards cards
		#create player and give him the deck
		#repeat num of players time
		players_list=[]
		for player_num in xrange(num_of_players):
			player_deck=[]
			for card in xrange(NUMOFCARDS):
				player_deck.append(game.get_single_card())
			name = raw_input("please type player name\n")
			players_list.append(Player(name,player_deck))
		return players_list

	def play_game(game):
		#play turn
		answer=""
		while 'n' != answer and 'y' != answer:
			while not game.play_turn():
				print "next turn"
			print "game over! would you like to play again?"
			#TODO if so, start a new game
			while answer not in ['n','y']:
				answer = raw_input("please note 'y' or 'n' ---> 'y' = YES, 'n' = No\n")
		if 'y' == answer:
			main()
		else:
			print "Thank you, Good bye!"
		
	def play_turn(game):
		#print turn details : who's turn, player deck,visible card
		print "It's {0} turn.".format(game.curr_player.name)
		valid=False #checks that players chosen card is valid
		while not valid:
			print "Current card playing is {0}.".format(game.visible_card)
			print "Your deck is:"
			for card_num in xrange(len(game.curr_player.players_deck)):
				print "[{0}]: {1}".format(card_num,game.curr_player.players_deck[card_num])
			#choose action 
			#check validity
			#play action
			answer = raw_input("press card number to play // 'd' to draw a card // 'q' to Quit the game\n")
			#Take care of wrong inputs

			if "q" == answer:
				return GAMEOVER
			if "d" == answer: 
				valid=True
				#Deal with drawing from the deck + taking care of the plus2 card
				while game.count_p2>0:
					game.curr_player.players_deck.append(game.get_single_card())
					game.count_p2-=1
				game.count_p2=1
				print "{0} decided to draw a card from the deck!".format(game.curr_player.name)
			else:
				try:
					answer=int(answer)
				except:
					print "If you enter charecters to draw or quit, it is 'd' or 'q'"
					continue
				if answer >= len(game.curr_player.players_deck):
					print "Chose a numbet that fits to your deck!"
					continue
				chosen_card=game.curr_player.players_deck[int(answer)]
				if game.valid_card_check(chosen_card):
					valid=True
					print "chosen card was {0} ".format(chosen_card)
					if chosen_card.value >=10: #the card is a special card
						print "Special card was played!"
						if STOP==chosen_card.value:
							game.stop_card(chosen_card,answer)
							break
						if CHANGEDIR==chosen_card.value:
							game.change_dir_card()
						if CHANGECOLOR==chosen_card.value:
							chosen_card.color=game.change_color_card(chosen_card)
						if TAKI==chosen_card.value:
							game.taki_card(chosen_card,answer)
							break
						if SUPERTAKI==chosen_card.value:
							game.supertaki_card(chosen_card,answer)
							break
						if PLUS2==chosen_card.value:
							game.plus2_card()
							
					game.visible_card = chosen_card
					game.curr_player.players_deck.pop(int(answer))
				else:
					print "Your choice isn't by the game format"
				
		#check game over : if so print the winner
		if not len(game.curr_player.players_deck):
			print "The WINNER is player {0}".format(game.curr_player.name)
			return GAMEOVER
		#if answer != 'd' and STOP==chosen_card.value:
		#	game.curr_player = game.whos_next()		#skip a turn
		game.curr_player = game.whos_next()
		return NOTOVER
	
	def stop_card(game,chosen_card,answer):
		print "{0} turn was skipped by {1} stop card!".format(game.whos_next().name, game.curr_player.name)
		game.visible_card = chosen_card
		game.curr_player.players_deck.pop(int(answer))
		game.curr_player = game.whos_next()		#skip a turn
	
	def change_dir_card(game):
		game.dir*=-1
		print "Game Direction was changed!"
	
	def change_color_card(game,chosen_card):
		new_color=raw_input("Choose a color: 'r'=RED, 'b'=BLUE, 'g'=GREEN, 'y'=YELLOW\n")
		good_color_list=['r','b','g','y']
		while new_color not in good_color_list:
			print "Invalid choise!:"
			new_color=raw_input("Please choose: 'r' / 'b' / 'g' / 'y'\n")
		return good_color_list.index(new_color)
		
	def taki_card(game,chosen_card,answer):
		game.visible_card = chosen_card
		game.curr_player.players_deck.pop(int(answer))
		new_card=0
		while 'c'!= new_card:
			print "Current card playing is {0}.".format(game.visible_card)
			print "Chose another card that fits your TAKI! Your deck is:"
			for card_num in xrange(len(game.curr_player.players_deck)):
				print "[{0}]: {1}".format(card_num,game.curr_player.players_deck[card_num])
			new_card=raw_input("press card number to play, or 'c' to close the Taki\n")
			if new_card=="c":
				break
			chosen_card=game.curr_player.players_deck[int(new_card)]																
			if chosen_card.value==game.visible_card.value and chosen_card.color != game.visible_card.color \
				and chosen_card.value != TAKI:
				#game format - same value, different color colses the taki
				game.visible_card = chosen_card
				game.curr_player.players_deck.pop(int(new_card))
				break
			if game.valid_card_check(chosen_card):
				game.visible_card = chosen_card
				game.curr_player.players_deck.pop(int(new_card))
				#game format - stop/change direction/change color card (must be valid card) closes the taki
				if STOP==chosen_card.value:
					game.stop_card(chosen_card,new_card)
					break
				if CHANGEDIR==chosen_card.value:
					game.change_dir_card()
					break
				if CHANGECOLOR==chosen_card.value:
					chosen_card.color=game.change_color_card(chosen_card)
					break
				if PLUS2==chosen_card.value:
					game.plus2_card()
					break
			else:
				print "Invalid card!"
		print "TAKI is closed"

	def supertaki_card(game,chosen_card,answer):
		print "SUPER TAKI!"
		chosen_card.color=game.change_color_card(chosen_card)
		game.taki_card(chosen_card,answer)
		return
	def plus2_card(game):
		if 1 == game.count_p2:
			game.count_p2+=1
		else:
			game.count_p2+=2
		print "Total card to draw: {0} cards!".format(game.count_p2)


	def valid_card_check(game, chosen_card):
		#TODO implement
		#If the card is special
		if PLUS2 == game.visible_card.value and 1!=game.count_p2:
			if PLUS2 == chosen_card.value:
				return True
			else:
				return False	
		if chosen_card.value==CHANGECOLOR or chosen_card.value==SUPERTAKI:
			return True
		#If card is the same number or the same color
		if chosen_card.color == game.visible_card.color or chosen_card.value == game.visible_card.value:
			return True	
		return False
		

	def whos_next(game):
		curr_player_index=game.players.index(game.curr_player)
		if REGULAR_DIRECTION == game.dir:
			return game.players[(curr_player_index+1)%len(game.players)]
		else:
			return game.players[(curr_player_index-1)%len(game.players)]

class Card:
	def __init__(card, color,value=None):
		card.color=color
		card.value=value

	def __str__(card):
		colors=["RED","BLUE","GREEN","YELLOW","R/B/G/Y"]
		values=["0","1","2","3","4","5","6","7","8","9","TAKI","SUPERTAKI",\
		"CHANGECOLOR","CHANGEDIR","STOP","PLUS2"]
		return "{0} {1}".format(values[card.value],colors[card.color])

class Player:
	def __init__(player,name="diffultname", players_deck=[]):
		player.name=name
		player.players_deck=players_deck
	
	def __str__(player):
		s = "{0}\n".format(player.name)
		for card in player.players_deck:
			s += str(card)
			s += "\n"
		return s


def start_game(game):	
	#get number of players
	num_of_players = int(raw_input("Welcome to our awesome Taki game, How many players are you playing?"))
	#create game
	game = Game(num_of_players)
	#start playing
	game.play_game()


def main():
	num_of_players=raw_input("How much people wants to play? optional 2 to 6 players\n")
	start_game=True
	while start_game:
		if len(num_of_players)>1:
			num_of_players=raw_input("Enter only 1 character answer (2,3,4,5 or 6)\n")
		elif ord(num_of_players)<=49 or ord(num_of_players)>=55:
			num_of_players=raw_input("please enter right number of players (2,3,4,5 or 6)\n")
		else:
			start_game = False
	g = Game(int(num_of_players))
	g.play_game()


if __name__ == "__main__":	
	main()
