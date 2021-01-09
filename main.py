import pyglet
import os
import random

class BlackJack(pyglet.window.Window):
    def __init__(self, xs, ys):
        super().__init__(width = xs, height = ys)


        # Score Locations;
        #  self.hit_btn_sprite.x + self.hit_btn_sprite.width

        self.bg = pyglet.resource.image('bg.png')
        self.hit_btn_img = pyglet.resource.image('hit.png')
        self.hit_btn_sprite = pyglet.sprite.Sprite(self.hit_btn_img, self.width / 2 - 100, 50)
        self.stay_btn_img = pyglet.resource.image('stay.png')
        self.stay_btn_sprite = pyglet.sprite.Sprite(self.stay_btn_img, self.hit_btn_sprite.x + self.hit_btn_sprite.width + 10, 50)
        self.ace_one_img = pyglet.resource.image('1.png')
        self.ace_one_sprite = pyglet.sprite.Sprite(self.ace_one_img, self.width / 2 - 200, self.height / 2 + 20)
        self.ace_eleven_img = pyglet.resource.image('11.png')
        self.ace_eleven_sprite = pyglet.sprite.Sprite(self.ace_eleven_img, self.width / 2 - 200, self.height / 2 - 50)
        self.player_score_box_img = pyglet.resource.image('score_box.png')
        self.player_score_box_sprite = pyglet.sprite.Sprite(self.player_score_box_img, self.width / 2 - 32, self.height / 2 - 50 )
        self.dealer_score_box_img = pyglet.resource.image('score_box.png')
        self.dealer_score_box_sprite = pyglet.sprite.Sprite(self.dealer_score_box_img, self.width / 2 - 32, self.height / 2 + self.player_score_box_sprite.height - 45)
        
        self.game_over_msg = pyglet.text.Label('Game Over! The winner is: ', 'Times New Roman', 18, x=self.width / 2 - 300, y=self.height / 2)
        self.player_score_label = pyglet.text.Label('', 'Times New Roman', 18, x=self.player_score_box_sprite.x + self.player_score_box_sprite.width / 2 - 10,
            y=self.player_score_box_sprite.y + self.player_score_box_sprite.height / 2 - 5)

        self.dealer_score_label = pyglet.text.Label('', 'Times New Roman', 18, x=self.dealer_score_box_sprite.x + self.dealer_score_box_sprite.width / 2 - 10,
            y=self.dealer_score_box_sprite.y + self.dealer_score_box_sprite.height / 2 - 5)
        self.deck_of_cards = list()
        self.player_cards = list()
        self.dealer_cards = list()

        self.dealer_turn = True
        self.game_over = False
        self.ace_flag = False
        self.ace_one = False
        self.ace_eleven = False

        self.player_score = 0
        self.dealer_score = 0
        self.dealer_x = 0
        self.player_x = 0
        self.round = 0

    def calc_score(self, s, v):

        if v[0] == 'K' or v[0] == 'J' or v[0] == 'Q' or v[0] == '1':
            s = 10
        elif v[0] == "A":
            if self.round == 0:
                if self.dealer_score + 11 > 21:
                    s = 1
                    print(f'----the ace number for the delaer is: {s}----')
                else:
                    s = 11
                    print(f'----the ace number for the delaer is: {s}----')
                    
            elif self.round == 1:
                self.ace_flag = True
                s = 0
                print(f'----The ace flag value is: {self.ace_flag}----')
            
        else:
            s = int(v[0])

        return s

    def get_deck(self):
        self.cards = os.listdir('PNG')
        for card in self.cards:
            if "back" not in card:
                self.deck_of_cards.append(card)

    def get_card(self, num=0):
        self.r = random.randint(0, len(self.deck_of_cards) - 1)
        self.r = self.deck_of_cards[self.r]
        self.card_image = pyglet.resource.image(f'PNG/{self.r}')

        if num == 0:
            if self.dealer_score <= 17:

                self.card_sprite = pyglet.sprite.Sprite(self.card_image, self.width / 2 + self.dealer_x, self.height - 200)
                self.card_sprite.update(None, None, None, 0.1, None, None)
                self.dealer_x += 30
                self.dealer_cards.append(self.card_sprite)
                self.dealer_score += self.calc_score(self.dealer_score, self.r)
                print(f'The dealer score: {self.dealer_score} | The card the dealer drew: {self.r}')
        elif num == 1:
            if self.player_score <= 21:    
                self.card_sprite = pyglet.sprite.Sprite(self.card_image, self.width / 2 + self.player_x, self.height / 2 - 175)
                self.card_sprite.update(None, None, None, 0.1, None, None)
                self.player_x += 30
                self.player_cards.append(self.card_sprite)
                self.player_score += self.calc_score(self.player_score, self.r)
                print(f'The player score: {self.player_score} | The card the player drew: {self.r}')

    def game_loop(self):

        if self.ace_flag == False:
            if self.round == 0:
                self.get_card(0)
                self.round = 1
            elif self.round == 1:
                self.get_card(1)
                self.round = 2
            elif self.round == 3:
                self.get_card(0)
  
    def on_mouse_press(self, x, y, button, modifier):

        if self.ace_flag == False:
            if x > self.hit_btn_sprite.x and x < (self.hit_btn_sprite.x + self.hit_btn_sprite.width):
                if y > self.hit_btn_sprite.y and y < (self.hit_btn_sprite.y + self.hit_btn_sprite.height):
                    print('Hit Button Clicked')
                    self.round = 1
                    # self.get_card(1)

            if x > self.stay_btn_sprite.x and x < (self.stay_btn_sprite.x + self.stay_btn_sprite.width):
                if y > self.stay_btn_sprite.y and y < (self.stay_btn_sprite.y + self.stay_btn_sprite.height):
                    print('Stay Button Clicked')
                    self.round = 3

        elif self.ace_flag == True:
            if x > self.ace_one_sprite.x and x < (self.ace_one_sprite.x + self.ace_one_sprite.width):
                if y > self.ace_one_sprite.y and y < (self.ace_one_sprite.y + self.ace_one_sprite.height):
                    print('Ace One Clicked')
                    self.player_score += 1
                    self.ace_flag = False
                    self.round = 1

            if x > self.ace_eleven_sprite.x and x < (self.ace_eleven_sprite.x + self.ace_eleven_sprite.width):
                if y > self.ace_eleven_sprite.y and y < (self.ace_eleven_sprite.y + self.ace_eleven_sprite.height):
                    print('Ace Eleven Clicked')
                    self.player_score += 11
                    self.ace_flag = False

    def update(self,t):
        self.clear() 

        self.bg.blit(0,0)


        if self.player_score >= 21:
            self.game_over = True
        
        if self.dealer_score >= 17:
            self.game_over = True

        if self.game_over == False:
        
            self.player_score_label.text = str(self.player_score)
            self.dealer_score_label.text = str(self.dealer_score)
        
        
            self.game_loop()

            self.player_score_box_sprite.draw()
            self.dealer_score_box_sprite.draw()
            self.player_score_label.draw()
            self.dealer_score_label.draw()

            for self.card in self.dealer_cards:
                self.card.draw()

            for self.card in self.player_cards:
                self.card.draw()


            if self.ace_flag == True:
                self.ace_one_sprite.draw()
                self.ace_eleven_sprite.draw()

            self.hit_btn_sprite.draw()
            self.stay_btn_sprite.draw()
        else:
            if self.player_score > self.dealer_score and self.player_score <= 21 or self.player_score == 21:
                self.game_over_msg.text = "Game Over! The player won! Congragulations"
            elif self.player_score < self.dealer_score and self.dealer_score <= 21 or self.player_score > 21:
                self.game_over_msg.text = "Game Over! Your score was: {0}. The dealer won! Try better next time".format(self.player_score)
            else:
                self.game_over_msg.text = "Game Over! It's a tie"

            self.game_over_msg.draw()

if __name__=='__main__':
    game = BlackJack(800, 600)
    game.get_deck()
    pyglet.clock.schedule_interval(game.update, 1/30)
    pyglet.app.run()