"""
Image classifier for furniture
"""
import os
from pathlib import Path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from furnituresorter.utils import get_files, image_extensions, create_folders
from furnituresorter.classifier import classify


class FurnitureSorter(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        input_box = toga.Box(style=Pack(direction=ROW))
        input_folder = toga.TextInput(readonly=True)
        input_folder.style.update(flex=1)

        output_box = toga.Box(style=Pack(direction=ROW))
        output_folder = toga.TextInput(readonly=True)
        output_folder.style.update(flex=1)

        console_box = toga.Box(style=Pack(direction=ROW))
        direc = str(os.getcwd())
        console = toga.MultilineTextInput(readonly=True, initial=f"Now in {direc}")
        console.style.update(flex=1)

        def update_console(text):
            console.value += "\n" + text

        self.main_window = toga.MainWindow(title=self.formal_name, size=(300, 300))

        def get_input_folder(widget):
            self.in_folder = self.main_window.select_folder_dialog('select folder to sort', initial_directory=os.getcwd())
            self.in_folder = Path(self.in_folder[0])
            input_folder.value = self.in_folder
            update_console(f"Input folder set to {self.in_folder}")

        def get_output_folder(widget):
            self.out_folder = self.main_window.select_folder_dialog('select output location', initial_directory=os.getcwd())
            self.out_folder = Path(self.out_folder[0])
            output_folder.value = self.out_folder
            update_console(f"Output folder set to {self.out_folder}")

        def classify_and_move(widget):            
            try:
                create_folders(self.out_folder)
            except:
                update_console("Problem creating the output location -- did you pick a destination folder?")
                return
            
            try:
                pictures = get_files(self.in_folder, extensions=image_extensions, recurse=True)
            except Exception as e:
                update_console(f"{e}")
                return
            
            try:
                classify(pictures, self.out_folder)
                update_console("Done!")
            except Exception as e:
                update_console("There was a problem :(")
                update_console(f"{e}")
            
            


        select_input_folder_button = toga.Button(
            'Select folder to sort',
            on_press=get_input_folder,
            style=Pack(padding=(0, 10))
        )

        select_output_folder_button = toga.Button(
            'Select destination folder',
            on_press=get_output_folder,
            style=Pack(padding=(0, 10))
        )
       
        classify_button = toga.Button(
            'Classify',
            on_press=classify_and_move,
            style=Pack(padding=(10, 200))
        )
        
        input_box.add(select_input_folder_button)
        input_box.add(input_folder)
        input_box.style.update(padding=(10, 20))

        output_box.add(select_output_folder_button)
        output_box.add(output_folder)
        output_box.style.update(padding=(10, 20))

        console_box.add(console)
        console_box.style.update(padding=(10, 20))
        
        main_box.add(input_box)
        main_box.add(output_box)
        main_box.add(classify_button)
        main_box.add(console_box)


        self.main_window.content = main_box
        self.main_window.show()



def main():
    return FurnitureSorter()
