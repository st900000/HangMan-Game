import sys

from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from animal_dictionary import get_animals, animals
import random
import time
import pygame

class Hangman(QWidget):
    choice = random.choice(get_animals())
    dash = [" _ "] * len(choice)

    correct = "sound_files/correct_answer.mp3"
    wrong = "sound_files/wrong_answer.mp3"
    win = "sound_files/win_game.mp3"
    lose = "sound_files/lose_game.mp3"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("HangMan")
        self.wrong_guesses = 0
        self.guess = QLabel(f"Guesses: {self.wrong_guesses}", self)
        self.picture = QLabel(self)
        self.man1 = QPixmap("hgArt/Hang Man Art 2.png")
        self.man2 = QPixmap("hgArt/Hang Man Art.png")
        self.man3 = QPixmap("hgArt/3.png")
        self.man4 = QPixmap("hgArt/4.png")
        self.man5 = QPixmap("hgArt/5.png")
        self.man6 = QPixmap("hgArt/6.png")
        self.man7 = QPixmap("hgArt/7.png")

        self.picture.setPixmap(self.man1)
        self.picture.setScaledContents(True)

        self.emoji = QLabel(self)
        self.word = QLabel("".join(self.dash), self)
        self.line_edit = QLineEdit(self)
        self.message = QLabel("",self)

        pygame.mixer.init()

        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()
        vbox.addWidget(self.guess)
        vbox.addWidget(self.picture)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.word)
        vbox.addWidget(self.line_edit)
        vbox.addWidget(self.message)

        self.guess.setAlignment(Qt.AlignRight)
        self.picture.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.word.setAlignment(Qt.AlignCenter)
        self.message.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)

        self.guess.setObjectName("guess")
        self.emoji.setObjectName("emoji")
        self.word.setObjectName("word")
        self.message.setObjectName("message")

        self.line_edit.setPlaceholderText("Guess the letter")

        self.setStyleSheet("""
        QWidget{
            background-color: white;
        }
        QLineEdit{
            font-size: 30px;
            padding: 10px;
            border: 4px solid;
            border-radius: 30px;
        }
        QLabel#word{
            font-size: 30px;
            font-weight: bold;
            font-style: italic;
            margin: 25px;
        }
        QLabel#guess{
            color: red;
            font-size: 30px;
            font-family: Arial;
            font-weight: bold;
        }
        QLabel#emoji{
            font-size: 80px;
        }
        QLabel#message{
            font-size: 30px;
            font-family: calibri;
            font-weight: bold;
            font-style: italic;
        }    
        """)

        self.line_edit.returnPressed.connect(self.check_letter)
        self.line_edit.returnPressed.connect(self.check_result)
        time.sleep(0.5)
        self.line_edit.returnPressed.connect(self.clear_text)

    @staticmethod
    def play_sound(sound_file):

        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def check_letter(self):
        if len(self.line_edit.text()) != 1:
            self.message.setText("Your choice must contain atleast ONE letter")
            time.sleep(4)
            self.message.clear()
            self.line_edit.clear()

        else:
            self.play_sound(self.correct)
            for i in range(len(self.choice)):
                 if self.choice[i] == self.line_edit.text().upper():
                    self.dash[i] = self.line_edit.text().upper()
                    self.word.setText("".join(self.dash))


    def check_result(self):
        if not self.line_edit.text().upper() in self.choice:
            self.play_sound(self.wrong)
            self.line_edit.clear()
            self.wrong_guesses += 1
            self.guess.setText(f"Guesses: {str(self.wrong_guesses)}")
            match self.wrong_guesses:
                case 1:
                    self.picture.setPixmap(self.man2)
                    self.picture.setScaledContents(True)
                case 2:
                    self.picture.setPixmap(self.man3)
                    self.picture.setScaledContents(True)
                case 3:
                    self.picture.setPixmap(self.man4)
                    self.picture.setScaledContents(True)
                case 4:
                    self.picture.setPixmap(self.man5)
                    self.picture.setScaledContents(True)
                case 5:
                    self.picture.setPixmap(self.man6)
                    self.picture.setScaledContents(True)
                case 6:
                    self.picture.setPixmap(self.man7)
                    self.picture.setScaledContents(True)

        if self.wrong_guesses == 6:
            self.play_sound(self.lose)

            while pygame.mixer.music.get_busy():
                time.sleep(1)

            self.emoji.setText(animals.get(self.choice))
            self.line_edit.setDisabled(True)
            self.message.setText(f"GAME OVER!!\nThe Animal was a {self.choice}")

        if self.word.text() == self.choice:
             self.play_sound(self.win)

             while pygame.mixer.music.get_busy():
                 time.sleep(1)

             self.emoji.setText(animals.get(self.choice))
             self.line_edit.setDisabled(True)
             self.message.setText("YOU WIN!!")

    def clear_text(self):
        self.line_edit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hangman = Hangman()
    hangman.show()
    sys.exit(app.exec_())