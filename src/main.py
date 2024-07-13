import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move

"""
Main Class: creates the screen and starts the game
            loops through events/moves and updates screen as game continues
"""
class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creates screen
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.popup_active= False
        self.restart_button=None
        self.cancel_button=None


    def mainloop(self):
        game = self.game
        board = self.game.board
        screen = self.screen
        dragger = self.game.dragger
        
        while True:
            game.show_bg(screen)  #this loop will keep running and continually update the screen
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen) #show pieces
            game.show_hover(screen)
            
            #extra update blit if a piece is being dragged to render it faster/smoother
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get(): #looks through all possible game events (user actions)
                 #if event is a quit by the user, end game
                if event.type ==pygame.QUIT: 
                    pygame.quit()
                    sys.exit()

                elif self.popup_active:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if self.restart_button.collidepoint((mouse_x, mouse_y)):
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            self.popup_active = False
                        elif self.cancel_button.collidepoint((mouse_x, mouse_y)):
                            self.popup_active = False

                #if the user clicks
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    dragger.update_mouse(event.pos) #updates pos with position of the event click

                    clicked_row = dragger.mouseY // SQSIZE #moving along y axis affects what row you are on
                    clicked_col = dragger.mouseX // SQSIZE #moving along x axis affects what column you are on
                    
                    

                    #if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece #saving ref to piece
                        # check if clicked piece is a valid color, as in it is the color of the next turn to move
                        if piece.color == game.next_player:
                            piece.clear_moves()
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos) #save initial position of piece
                            dragger.drag_piece(piece)

                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                    

                #if user moves mouse
                elif event.type == pygame.MOUSEMOTION: 
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    if Square.in_range(motion_col, motion_row):
                        game.set_hover(motion_row, motion_col)
                    
    
                    if dragger.dragging: #if the user has a piece currently clicked
                        dragger.update_mouse(event.pos)

                        #adding extra blit for background and pieces to create smoother animation when dragging
                        #show methods
                        game.show_bg(screen) 
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen) #blit depends on mouse position, so updated mouse first


                #if user unclicks mouse
                elif event.type == pygame.MOUSEBUTTONUP: 
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        

                        #create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)

                        new_move = Move(initial,final)

                        if board.valid_move(dragger.piece, new_move):
                            captured=board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, new_move)
                            board.set_true_en_passant(dragger.piece)

                            #sounds
                            game.play_sound(captured)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            game.next_turn()
                    dragger.undrag_piece(piece)

                #key press
                elif event.type == pygame.KEYDOWN:
                    #changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()
                    
                    if event.key == pygame.K_r and not self.popup_active:
                        self.popup_active = True

            

               


            if self.popup_active:
                self.draw_reset_popup()

            pygame.display.update() #updates screen
        
    

    def draw_reset_popup(self):
        popup_width = 400
        popup_height = 200
        popup_x = (WIDTH - popup_width) // 2
        popup_y = (HEIGHT - popup_height) // 2

        white = (255, 255, 255)
        black = (0, 0, 0)
        gray = (169, 169, 169)

        pygame.draw.rect(self.screen, gray, (popup_x, popup_y, popup_width, popup_height))

        font = pygame.font.Font(None, 36)
        self.draw_text("Are you sure you want to restart?", font, black, self.screen, popup_x + 10, popup_y + 20)

        
        self.restart_button = pygame.Rect(popup_x + 50, popup_y + 100, 100, 50)
        self.cancel_button = pygame.Rect(popup_x + 250, popup_y + 100, 100, 50)

        pygame.draw.rect(self.screen, black, self.restart_button)
        pygame.draw.rect(self.screen, black, self.cancel_button)

        self.draw_text("Restart", font, white, self.screen, popup_x + 60, popup_y + 115)
        self.draw_text("Cancel", font, white, self.screen, popup_x + 260, popup_y + 115)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


main = Main()

main.mainloop()