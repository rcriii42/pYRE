import pygame, os
from pygame.locals import Rect
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from GraphicUtils import tile_texture
import clickndrag
import clickndrag.gui

char_width = 10

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
teal = (0, 128, 128)
yellow = (255, 255, 0)
white = (255, 255, 255)
buff = (240, 220, 130)
black = (0, 0, 0, 255)

bubble_nos = set(range(1000)) #serial nos for bubbles, hope we never have more than 1000
class MessageBubble(clickndrag.gui.OutlinedText):
    """
    MessageBubble - A label that self-destructs after a short period of time
    """
    def __init__(self, item, text, text_color=yellow, res_time=2, float=0):
        """Initialise the MessageBubble.
            item is the item to put the bubble next to (expected to have name & rect parameter)
           text is the text to be written on the Label. If text is None, it is
           replaced by an empty string.
           res_time is the time to stay active in seconds.
           If float positive, the bubble moves up and to the right that many pixels per update
        """
        self.num = bubble_nos.pop()
        name = "%s_%d"%(item.name, self.num)
        clickndrag.gui.OutlinedText.__init__(self, name, text, text_color)
        self.clock = pygame.time.Clock()
        self.life = res_time*1000.
        self.float = (float, float*-1)
        
    def update(self):
        """Call the base class update, then check for end-of-life.
        """
        self.rect.move_ip(self.float)
        clickndrag.gui.Label.update(self)
        self.life -= self.clock.tick()
        if self.life <= 0:
            bubble_nos.add(self.num)
            self.destroy()
        return

# class CityStatus(clickndrag.gui.Container):
#     """
#     CityStatus - Class to wrap a status window for a city that updates each turn
#     """
#     def __init__(self, name, city, padding = 0, background_color = None):
#         """
#         initialize.  Initialized with a name, destroy button in upper right, and
#         four lines per project in the city.
#         """
#         clickndrag.gui.Container.__init__(self, name, padding, background_color)
#         self.city = city
#         self.project_status = {}    #a dict of lists of labels for each project
#
#         city_data_strs = {'city_name':city.name}
#         city_data_strnames=[]
#         self.num_proj=-1
#         for p in city.projects:
#             self.num_proj += 1
#             city_data_strnames.extend(['name_%d'%self.num_proj,
#                                        'size_%d'%self.num_proj,
#                                        'value_%d'%self.num_proj,
#                                        'dredges_%d'%self.num_proj])
#             city_data_strs['name_%d'%self.num_proj]="%s"%p.name
#             city_data_strs['size_%d'%self.num_proj]="  Size: %0.0f"%p.quantity
#             city_data_strs['value_%d'%self.num_proj]="  Value: $%0.0f"%p.total_value
#             city_data_strs['dredges_%d'%self.num_proj]="  Dredges: %i %% Done: %.1f"%(len(p.dredges),p.progress()*100)
#         name_length = max([len(city_data_strs[s]) for s in city_data_strs])*char_width+char_width
#         name_label=clickndrag.gui.Label('city_name',
#                                         city.name,
#                                         Rect(0, 0, name_length, 15),
#                                         background_color=teal)
#         self.sub(name_label)
#         destroy_button = clickndrag.gui.Button('X',
#                                                Rect(name_label.rect.width-char_width, 0, char_width, 15),
#                                                lambda x: x.parent.parent.destroy(),
#                                                background_color=teal)
#         name_label.sub(destroy_button)
#         n=-1
#         for p in city.projects:
#             n += 1
#             self.add_project_display(p, n)
#
#     def add_project_display(self, p, pID):
#         """Add a new project"""
#         city_data_strnames = ['name_%d'%pID,'size_%d'%pID,'value_%d'%pID,'dredges_%d'%pID]
#         city_data_strs = {}
#         city_data_strs['name_%d'%pID]="%s"%p.name
#         city_data_strs['size_%d'%pID]="  Size: %0.0f"%p.quantity
#         city_data_strs['value_%d'%pID]="  Value: $%0.0f"%p.total_value
#         city_data_strs['dredges_%d'%pID]="  Dredges: %i %% Done: %.1f"%(len(p.dredges),p.progress()*100)
#         self.project_status[p] = []
#         str_len = max([len(city_data_strs[s]) for s in city_data_strs])*char_width
#         for s in city_data_strnames:
#             if 'name' in s:
#                 color = buff
#             else:
#                 color = None
#             L = clickndrag.gui.Label(s,
#                                      city_data_strs[s],
#                                      Rect(0, 0, str_len, 15),
#                                      background_color = color)
#             self.sub(L)
#             self.project_status[p].append(L)
#
#     def update(self):
#         """
#         Update the labels for each project, then call base class update.
#         """
#         for p in self.project_status:
#             if p not in self.city.projects:
#                 #this project has disappeared, remove and destroy the labels
#                 for x in self.project_status[p]:
#                     self.project_status[p].remove(x)
#                     x.destroy()
#         for p in self.city.projects:
#             if p not in self.project_status:
#                 #this is a new project, add it
#                 self.num_proj += 1
#                 self.add_project_display(p, self.num_proj)
#             self.project_status[p][0].text = "%s"%p.name
#             self.project_status[p][1].text = "  Size: %0.0f"%p.quantity
#             self.project_status[p][2].text = "  Value: $%0.0f"%p.total_value
#             self.project_status[p][3].text = "  Dredges: %i %% Done: %.1f"%(len(p.dredges),p.progress()*100)
#
#         clickndrag.gui.Container.update(self)

class GameWindow(object):
    """
    GameWindow - Class to wrap the graphical display for the game.
    """
    def __init__(self, width=700, height=800, timeScale=1):
        
        self.max_frame_rate = 10    #max frame rate in frames-per-second
        # self.clock = pygame.time.Clock()
        
        pygame.init()
        self.screenSize = width, height
        self.w32windowClass = "pygame"  #The win32 window class for this object
        self.screen = clickndrag.Display(self.screenSize) #pygame.display.set_mode(self.screenSize)
        self.windowCaption = "Pyre"
        pygame.display.set_caption(self.windowCaption)        
        self.white = pygame.Color("white")
        self.screen.image.fill(self.white)
        pygame.display.flip()
        
        # #The game screen
        # sea_tile = pygame.image.load(os.path.join('graphics', 'sea_tile_32x32.png')).convert()
        # self.sea_tiles = [sea_tile]*250
        # self.sea_tiles.append(pygame.image.load(os.path.join('graphics', 'whale_tile_32x32.png')).convert())
        # self.sea_tiles.append(pygame.image.load(os.path.join('graphics', 'tugboat_tile_32x32.png')).convert())
        # self.sea_tiles.append(pygame.image.load(os.path.join('graphics', 'turtle_tile_32x32.png')).convert())
        # self.sea_tiles.append(pygame.image.load(os.path.join('graphics', 'swordfish_tile_32x32.png')).convert())
        # menu_margin = width#*.75
        # self.game_plane = clickndrag.Plane("game screen", Rect(0, 0, menu_margin, height))
        # self.game_background = tile_texture(self.game_plane.image, self.sea_tiles)
        # self.game_plane.image.blit(self.game_background, (0,0))
        # self.screen.sub(self.game_plane)
        
        #The main status display - Date and player $$
        self.turn_status = clickndrag.gui.Button("Turn: 1",
                                                Rect(0, 0, 150, 15),
                                                None) #callback placeholder
        self.screen.sub(self.turn_status)
        self.player_status = clickndrag.gui.Button("Player: player_1",
                                                   Rect(150, 0, 125, 15),
                                                   None) #callback placeholder
        self.screen.sub(self.player_status)
        self.status_windows = {}
        
        self.city_bubble = None

        pygame.display.flip()

    def update(self, game):
        """update - update the game window"""
        #self.game_plane.image.blit(self.game_background, (0,0)) #reset background drawing
        # for c in game.cities:
        #     if not c.plane:
        #         c.plane = clickndrag.Plane("city of %s"%c.name, Rect(c.location,c.image_size))
        #         c.plane.image.blit(c.image, (0,0))
        #         self.game_plane.sub(c.plane)
        #
        # for d in game.dredges:
        #     if not d.plane:
        #         image_size = 50,50
        #         d.plane = clickndrag.Plane(d.name, Rect(d.location,image_size))
        #         d.plane.image.set_colorkey(white)
        #         d.plane.image.fill(white)
        #         draw_dredge(d.plane.image, d.dimensions, image_size[0])
        #         #d.plane.image.blit(d.image, (0,0))
        #         d.plane.draggable=True
        #         self.game_plane.sub(d.plane)
                
        self.turn_status.text = "Turn: {0:,}".format(int(game.turn))
        self.player_status.text = "Value: {}".format(game.current_player.name)
        self.screen.update()
        self.screen.render()
        
        pygame.display.flip()
        return True
    
    # def build_city_status(self, bubble):
    #     c=bubble.city
    #     if c in self.status_windows:
    #         self.status_windows[c].destroy()
    #     city_status = CityStatus(c.name, c)
    #
    #     #place city status where it will not lap off the edge of the screen, starting in top left
    #     if c.plane.rect.left-city_status.rect.width>self.game_plane.rect.left and c.plane.rect.top-city_status.rect.height>self.game_plane.rect.top:
    #         city_status.rect.bottomright = c.plane.rect.topleft
    #     elif c.plane.rect.right+city_status.rect.width<self.game_plane.rect.right and c.plane.rect.top-city_status.rect.height>self.game_plane.rect.top:
    #         city_status.rect.bottomleft = c.plane.rect.topright
    #     elif c.plane.rect.right+city_status.rect.width>self.game_plane.rect.right and c.plane.rect.bottom+city_status.rect.height<self.game_plane.rect.bottom:
    #         city_status.rect.topleft = c.plane.rect.bottomright
    #     else:
    #         city_status.rect.topright = c.plane.rect.bottomleft
    #     self.game_plane.sub(city_status)
    #     self.status_windows[c] = city_status
        
    def post_quit(self):
        q = pygame.event.Event(pygame.QUIT)
        pygame.event.post(q)

    def quit(self):
        pygame.quit()
    
    def mainloop(self, controller):
        """The mainloop for the game, expects a controller to manage the game objects"""
        elapsed=1
        drag_dredge = False
        while controller.end != True:
            #Update the time
            messages = controller.step(elapsed)
            self.update(controller.G)
            # for m in messages:
            #     if m[1]:
            #         mb = MessageBubble(m[0].plane, m[1], float=2)
            #         mb.rect.bottomleft = m[0].plane.rect.topright
            #         self.game_plane.sub(mb)
            #Check events
            event_list = pygame.event.get()
            self.screen.process(event_list) #Let clickndrag go first
            self.next_message=None
            last_mouse_move = None
            last_mouse_down = None
            last_mouse_up = None
            for e in event_list:
                if e.type == QUIT:
                    controller.quit()
                elif e.type == MOUSEMOTION:
                    last_mouse_move = e
                elif e.type == MOUSEBUTTONDOWN:
                    last_mouse_down = e
                elif e.type == MOUSEBUTTONUP:# and drag_dredge:
                    last_mouse_up = e
            if last_mouse_move:
                #self.next_message = "Moved to: %s"%`last_mouse_move.pos`
                pass
            # if last_mouse_down:
            #     if self.city_bubble:
            #         self.city_bubble.destroy()
            #         self.city_bubble = None
            #     #self.next_message = "Mouse click: %s %s"%(`last_mouse_down.pos`, `last_mouse_down.button`)
            #     for c in controller.G.cities:
            #         #did we click on a city?
            #         if c.plane.rect.collidepoint(last_mouse_down.pos):
            #             self.next_message =  "clicked on city of %s"%c.name
            #             bubble_loc = Rect((c.location[0]+c.image_size[0],
            #                               c.location[1]-15),
            #                               (len(c.name)*8, 15))
            #             self.city_bubble = clickndrag.gui.Button(c.name,
            #                                                      bubble_loc,
            #                                                      self.build_city_status)
            #             self.city_bubble.city = c
            #             self.game_plane.sub(self.city_bubble)
            #     for d in controller.G.dredges:
            #         #How about a dredge?
            #         if d.plane.rect.collidepoint(last_mouse_down.pos):
            #             self.next_message = "clicked on dredge %s"%d.name
            #             if last_mouse_down.button == 1:
            #                 drag_dredge = d
            #                 self.next_message = "dragging dredge %s"%d.name
            # if drag_dredge:
            #     if last_mouse_up:
            #         drag_dredge.destination = last_mouse_up.pos
            #         self.next_message = "Dredge %s moved to: %s"%(drag_dredge.name, drag_dredge.destination)
            #         drag_dredge = None
            #     else:
            #         pass
            #         #self.next_message = "dragging dredge %s to %s"%(d.name, `dredge_drag_to`)
            
            #move on with our lives
            pygame.event.clear()
            if self.next_message: print(self.next_message)
            elapsed = self.clock.tick(self.max_frame_rate)
