# Fichier: classes/windowsChat/ChatBox.py

import pygame
import pygame_gui

from datetime import datetime

from classes.utilitaires.utilitaires_02_reseau import Utilitaires02Reseau


class ChatBox:
    def __init__(self, manager, canvas_position):

        #
        self.canvas_position = canvas_position

        #
        self.text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                (self.canvas_position[0], self.canvas_position[1]), (400, 250)),
            html_text='',
            manager=manager
        )

        #
        self.text_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.canvas_position[0], self.canvas_position[1] + 260), (400, 30)),
            manager=manager
        )

        # Liste qui stocke les messages d'utilisateur.
        self.received_messages = []

    # [REPERE 1 - 2]
    # MAJ avec les messages reçus depuis le serveur.
    # MAJ de la ChatBox.
    # MAJ le widget: self.text_box de la classe
    # ChatBox (fichier: classes/windowsChat/ChatBox.py).
    # [REPERE 1 - 1] dans la methode update() du fichier
    # screen06_game.py.
    # [REPERE 1 - 3] dans le fichier client.py.
    def update_messages(self, new_message):

        #
        self.received_messages.insert(0, new_message)

        #
        messages_str = '\n'.join(self.received_messages)

        #
        self.text_box.html_text = f"\n{messages_str}"

        #
        self.text_box.rebuild()

    def process_events(self, event, manager, websocket_client=None):

        if event.type == pygame.MOUSEBUTTONDOWN:

            #
            x, y = event.pos

            #
            adjusted_x, adjusted_y = x - \
                self.canvas_position[0], y - self.canvas_position[1]

            #
            if self.text_entry.rect.collidepoint(adjusted_x, adjusted_y):
                adjusted_event = pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN,
                    {'pos': (adjusted_x, adjusted_y), 'button': 1}
                )

                #
                manager.process_events(adjusted_event)

                #
                return True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                #
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                #
                text_to_send = self.text_entry.get_text()

                print(current_time)

                # Concaténer current_time et text_to_send avec un
                # retour à la ligne.
                formatted_text_to_send = f">>> {text_to_send}"

                print(f'Msg client à envoyer: {formatted_text_to_send}')

                # Envoyer le message au serveur
                if websocket_client:
                    Utilitaires02Reseau.send_message(
                        websocket_client, formatted_text_to_send)

                self.received_messages.insert(0, formatted_text_to_send)

                messages_str = '\n'.join(self.received_messages)

                self.text_box.html_text = f"\n{messages_str}"

                self.text_box.rebuild()

                self.text_entry.set_text('')

                return True

        return False

    def draw(self, screen):
        # Dessinez les éléments personnalisés sur le Surface de Pygame ici.
        # Par exemple, si vous voulez dessiner un rectangle autour de la chat box:
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.canvas_position[0], self.canvas_position[1], 400, 300), 2)
