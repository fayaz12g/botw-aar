import os
import sys
import customtkinter
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory
from customtkinter import *
from threading import Thread
import shutil
from download import *
from patch import *
import getpass
from script import patch_blarc
from PIL import Image
import webbrowser
from tkinter import *
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory
import customtkinter
from customtkinter import *
from PIL import Image, ImageTk
import os
from threading import Thread
import getpass
from pathlib import Path
import sys
import shutil
import psutil
from visuals import create_visuals
from compress import *
from extract import extract_blarc
from functions import *
import pyautogui



#######################
#### Create Window ####
#######################

tool_version = "2.0.0"

root = customtkinter.CTk()
root.title(f"Fayaz's Settings {tool_version} for The Legend of Zelda: Breath of the Wild")
root.geometry("520x760")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")  
windowtitle = customtkinter.CTkLabel(master=root, font=(CTkFont, 20), text="Fayaz's BOTW Utility {tool_version}")

###############################################
###########    GLOBAL SETTINGS      ###########
###############################################

# Visuals
screen_width, screen_height = pyautogui.size()
ar_numerator = StringVar(value=f"{screen_width}")
ar_denominator = StringVar(value=f"{screen_height}")

do_60fps = BooleanVar(value=True)
do_dynamic = BooleanVar(value=True)

# # Controller
# controller_types = ["Switch", "Xbox", "Playstation"]

# full_button_layouts = ["Normal"]
# deck_button_layouts = ["Normal"]

# dualsense_colors = ["Red", "White", "Blue", "Pink", "Purple", "Black"]

# colored_button_colors = ["White"]

# controller_type = StringVar(value="Switch")
# button_color = StringVar()
# controller_color = StringVar()
# button_layout = StringVar()

# HUD
centered_HUD = BooleanVar()
corner_HUD = BooleanVar(value=True)

# Generation
output_yuzu = BooleanVar()
output_sudachi = BooleanVar()
output_ryujinx = BooleanVar()
open_when_done = BooleanVar()
mod_name_var = StringVar(value="Fayaz's Settings")

input_folder = None

zs_file_path = None

# image_name = "switch_normal.jpeg"
# controller_layout_label = ""
# normal__xbox_layout = "Normal Layout:  A > B, B > A , X > Y, Y > X"
# PE__xbox_layout = "PE Layout: A > A, B > B, X > X, Y > Y"
# western_xbox_layout = "Western Layout: B > A,  A > B, X > X, Y > Y"
# elden_xbox_layout = "Elden Ring Layout: A > Y, B > B, Y > A,  X > X"
# normal__dual_layout = "Normal Layout:  A > Circle, B > Cross, X > Triangle, Y > Square"
# PE__dual_layout = "PE Layout: B > Circle, A > Cross, Y > Triangle, X > Square"
# western_dual_layout = "Western Layout: B  > Circle,  A > Cross, X > Triangle, Y > Square"
# elden_dual_layout = "Elden Ring Layout: A > Triangle,  B > Square, X > Circle, Y > Cross"

patch_folder = None
blyt_folder = None

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
icon_path = os.path.join(script_directory, 'icon.ico')
# dfps_folder = os.path.join(script_directory, "dFPS")
# dfps_ini_folder = os.path.join(script_directory, "customini", "dfps")

root.iconbitmap(icon_path)

################################################
###########    HELPER FUNCTIONS      ###########
################################################

class ClickableLabel(customtkinter.CTkLabel):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, cursor="hand2", **kwargs)
        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        text = self.cget("text")
        lines = text.split("\n")
        for line in lines:
            if line.startswith("http"):
                webbrowser.open_new(line)

class PrintRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""
        self.text_widget.configure(state='disabled')  # Disable user input
        # self.text_widget.configure("custom_tag", background='lightgray', foreground='black')

    def write(self, text):
        self.buffer += text
        self.text_widget.configure(state='normal')  # Enable writing
        self.text_widget.insert("end", text, "custom_tag")  # Apply custom_tag to the inserted text
        self.text_widget.see("end")
        self.text_widget.configure(state='disabled')  # Disable user input again

    def flush(self):
        self.text_widget.configure(state='normal')  # Enable writing
        try:
            self.text_widget.insert("end", self.buffer, "custom_tag")  # Apply custom_tag to the buffered text
        except Exception as e:
            self.text_widget.insert("end", f"Error: {e}\n", "custom_tag")  # Display the exception message with custom_tag
        finally:
            self.text_widget.see("end")
            self.text_widget.configure(state='disabled')  # Disable user input again
            self.buffer = ""

def handle_focus_in(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.configure(text_color=("#000000", "#FFFFFF"))

def handle_focus_out(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.configure(text_color='gray')

def update_values(*args):
    global do_custom_ini
    do_custom_ini = True

def select_output_folder():
    global input_folder
    global patch_folder
    input_folder = askdirectory()
    if input_folder:
        try:
            os.makedirs(input_folder, exist_ok=True)
            Path(input_folder).mkdir(parents=True, exist_ok=True) 
        except Exception as e:
            return
    else:
        return

def create_ratio():
    numerator = ar_numerator.get()
    denominator = ar_denominator.get()

    if numerator and denominator:
        numerator = float(numerator)
        denominator = float(denominator)
        ratio = numerator / denominator
    else:
        ratio = 16/9

    return str(ratio)

def calculate_ratio():
    numerator_entry_value = ar_numerator.get()
    if not numerator_entry_value:
        print("Numerator value is empty. Please provide a valid number.")
        return

    try:
        numerator = float(numerator_entry_value)
    except ValueError:
        print("Invalid numerator value. Please provide a valid number.")
        return

    if ar_denominator.get() == '':
        denominator = 9
    else:
        denominator = float(ar_denominator.get())

    if denominator == 0:
        print("Denominator value cannot be zero.")
        return

    scaling_component = numerator / denominator
    if scaling_component < 16 / 9:
        scaling_factor = scaling_component / (16 / 9)
    else:
        scaling_factor = (16 / 9) / scaling_component
    return scaling_factor

def check_process_running(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False

scaling_factor = 0.762
HUD_pos = "corner"

def handle_focus_in(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.configure(text_color=("#000000", "#FFFFFF"))

def handle_focus_out(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.configure(text_color='gray')

def create_mod():
    global scaling_factor
    global input_folder
    mod_name = str(mod_name_var.get())
    ratio_value = (int(numerator_entry.get()) / int(denominator_entry.get()))
    scaling_factor = (16/9) / (int(numerator_entry.get()) / int(denominator_entry.get()))
    username = getpass.getuser()
    gameid = "01007EF00011E000"
    if output_yuzu.get() is True:
        input_folder = f"C:/Users/{username}/AppData/Roaming/yuzu/load/{gameid}"
        process_name = "yuzu.exe"
    if output_ryujinx.get() is True:
        input_folder = f"C:/Users/{username}/AppData/Roaming/Ryujinx/mods/contents/{gameid}"
        process_name = "ryujinx.exe"
    if output_sudachi.get() is True:
        input_folder = f"C:/Users/{username}/AppData/Roaming/sudachi/load/{gameid}"
        process_name = "sudachi.exe"
    else:
        process_name = "yuzu.exe"
    if input_folder:
        patch_folder = os.path.join(input_folder, mod_name, "exefs")
        try:
            os.makedirs(input_folder, exist_ok=True)
            Path(patch_folder).mkdir(parents=True, exist_ok=True) 
        except Exception as e:
            print(f"Error: {e}")
            return
    else:
        print("Select an emulator or output folder.")
        return
    text_folder = os.path.join(input_folder, mod_name)
    patch_folder = os.path.join(input_folder, mod_name, "exefs")
    if corner_HUD.get() == True:
        print("Corner HUD")
        HUD_pos = "corner"
    if centered_HUD.get() == True:
        print("Center HUD")
        HUD_pos = "center"
    # Clean up the working directory
    if os.path.exists(text_folder):
        shutil.rmtree(text_folder)

    # Download the BOTW Layout Files
    BOTW_download(input_folder, mod_name)

    # Create the PCHTXT Files
    visual_fixes = create_visuals(do_60fps.get(), do_dynamic.get())
    BOTW_patch(patch_folder, str(ratio_value), str(scaling_factor), visual_fixes)
    romfs_folder = os.path.join(input_folder, mod_name, "romfs")
    pack_folder = os.path.join(input_folder, mod_name, "romfs", "Pack")

    # Download and put Controlelr Files in Place
    # controller_files(controller_type.get(), theromfs_folder)

    ####################
    # PACK Extraction #
    ####################

    for root, _, files in os.walk(romfs_folder):
        for file in files:
            if file.lower().endswith(".pack"):
                file_path = os.path.join(root, file)
                print(f"Extracting {file}.")
                extract_blarc(file_path)
                os.remove(file_path)
                    
    ####################
    # SBLARC Extraction #
    ####################

    for root, _, files in os.walk(romfs_folder):
        for file in files:
            if file.lower().endswith(".sblarc"):
                file_path = os.path.join(root, file)
                print(f"Extracting {file}.")
                extract_blarc(file_path)
                os.remove(file_path)

    # Perform Pane Strecthing
    patch_blarc(str(ratio_value), HUD_pos, romfs_folder)

    ##########################
    # Cleaning and Repacking #
    ##########################
    
    
    x = 1
    sub = 1

    print("Repacking new sblarc files. This step may take a while")
    for root, dirs, _ in os.walk(romfs_folder):
        if "blyt" in dirs:
            parent_folder = os.path.dirname(root)
            new_blarc_file = os.path.join(parent_folder, os.path.basename(root) + ".sblarc")
            pack(root, ">", 1, new_blarc_file, sub)
            sub = sub + 1
            shutil.rmtree(root) 
    
    print("Repacking new pack files. This step may take a while")
    for root, dirs, _ in os.walk(pack_folder):
        if "Layout" in dirs:
            parent_folder = os.path.dirname(root)
            new_blarc_file = os.path.join(parent_folder, os.path.basename(root) + ".pack")
            pack(root, ">", -1, new_blarc_file, x)
            x = x + 1
            shutil.rmtree(root) 


    if open_when_done.get() == True:
        print ("Complete! Opening output folder.")
        os.startfile(text_folder)
    else:
        print("Finished! You can now launch your emulator and enjoy.")

def create_patch():
    sys.stdout = PrintRedirector(scrolled_text)
    t = Thread(target=create_mod)
    t.start() 

################################
####### Layout Mangement #######
################################

def pack_widgets():
    notebook.pack(padx=10, pady=10)

    console_label3.pack(padx=10, pady=10)

    frame.pack()

    numerator_entry.pack(side="left")
    aspect_ratio_divider.pack(side="left")
    denominator_entry.pack(side="left")
    
    fps60_checkbox.pack(padx=5, pady=5)
    dynamic_checkbox.pack(padx=10, pady=10)
    
    # image_label.pack()

    # image_layout_label.pack(padx=5, pady=5)
    
    # controller_type_label.pack()
    # controller_type_dropdown.pack()

    # if controller_type.get() == "Colored Dualsense":
    #     controller_color_label.pack()
    #     controller_color_dropdown.pack()
    
    # if controller_type.get() == "Xbox" or controller_type.get() == "Playstation":
    #     button_color_label.pack()
    #     button_color_dropdown.pack()

    # if controller_type.get() == "Xbox" or controller_type.get() == "Playstation" or controller_type.get() == "Steam Deck":
    #     button_layout_label.pack()
    #     button_layout_dropdown.pack()

    content_frame.pack(padx=10, pady=10)

    hud_label.pack()
    center_checkbox.pack()
    corner_checkbox.pack(padx=10, pady=10) 

    emulator_label.pack(pady=10)
    yuzu_checkbox.pack(side="top")
    ryujinx_checkbox.pack(side="top", pady=5)
    sudachi_checkbox.pack(side="top")

    output_folder_button.pack()
    output_folder_button.pack(pady=10)

    open_checkbox.pack(pady=10, side="top")

    mod_name_label.pack()
    mod_name_entry.pack()

    create_patch_button.pack(pady=15)

    console_label.pack(padx=10, pady=5)
    scrolled_text.pack()

    progressbar.pack(pady=5)

    credits_label.pack(padx=20, pady=30)


def forget_packing():
    notebook.pack_forget()

    console_label3.pack_forget()

    frame.pack_forget()

    numerator_entry.pack_forget()
    aspect_ratio_divider.pack_forget()
    denominator_entry.pack_forget()
    
    fps60_checkbox.pack_forget()
    dynamic_checkbox.pack_forget()

    # image_label.pack_forget()
    # image_layout_label.pack_forget()
    
    # controller_type_label.pack_forget()
    # controller_type_dropdown.pack_forget()
    
    # controller_color_label.pack_forget()
    # controller_color_dropdown.pack_forget()
    
    # button_color_label.pack_forget()
    # button_color_dropdown.pack_forget()

    # button_layout_label.pack_forget()
    # button_layout_dropdown.pack_forget()

    content_frame.pack_forget()

    hud_label.pack_forget()
    center_checkbox.pack_forget()
    corner_checkbox.pack_forget()

    emulator_label.pack_forget()
    yuzu_checkbox.pack_forget()
    sudachi_checkbox.pack_forget()
    ryujinx_checkbox.pack_forget()

    output_folder_button.pack_forget()
    output_folder_button.pack_forget()

    mod_name_label.pack_forget()
    mod_name_entry.pack_forget()

    open_checkbox.pack_forget()

    create_patch_button.pack_forget()
    create_patch_button.pack_forget()

    console_label.pack_forget()
    scrolled_text.pack_forget()

    progressbar.pack_forget()

    credits_label.pack_forget()

def repack_widgets(*args):
    forget_packing()
    pack_widgets()

#######################
######## Tabs #########
#######################

notebook = customtkinter.CTkTabview(root, width=10, height=10)

#######################
####### Visuals #######
#######################

notebook.add("Visuals")

console_label3= customtkinter.CTkLabel(master=notebook.tab("Visuals"), text=f'Aspect Ratio: (Auto-Deteced as {screen_width} x {screen_height}):')

frame = customtkinter.CTkFrame(master=notebook.tab("Visuals"))

numerator_entry = customtkinter.CTkEntry(frame, textvariable=ar_numerator)
numerator_entry.configure(text_color='gray')
numerator_entry.bind("<FocusIn>", lambda event: handle_focus_in(numerator_entry, f"{screen_width}"))
numerator_entry.bind("<FocusOut>", lambda event: handle_focus_out(numerator_entry, f"{screen_width}"))
aspect_ratio_divider= customtkinter.CTkLabel(frame, text=":")
denominator_entry = customtkinter.CTkEntry(frame, textvariable=ar_denominator)
denominator_entry.configure(text_color='gray')
denominator_entry.bind("<FocusIn>", lambda event: handle_focus_in(denominator_entry, f"{screen_height}"))
denominator_entry.bind("<FocusOut>", lambda event: handle_focus_out(denominator_entry, f"{screen_height}"))

fps60_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="60 FPS", variable=do_60fps)
dynamic_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Visuals"), text="Disabled Dynamic Resolution", variable=do_dynamic)

# ##########################
# ####### Controller #######
# ##########################

# notebook.add("Controller")

# def update_image(*args):
#     selected_controller_type = controller_type.get().lower()
#     selected_controller_color = controller_color.get().lower()
#     selected_button_layout = button_layout.get().lower()

#     global image_name
#     if selected_controller_type == "colored dualsense":
#         if selected_controller_color:
#             image_name = f"dual_{selected_controller_color}.jpeg"
#         else:
#             image_name = f"dual_black.jpeg"
#     elif selected_controller_type == "xbox":
#         if selected_button_layout:
#             image_name = f"xbox_{selected_button_layout}.jpeg"
#         else:
#             image_name = f"xbox_normal.jpeg"
#     elif selected_controller_type == "playstation":
#         if selected_button_layout:
#             image_name = f"dual_{selected_button_layout}.jpeg"
#         else:
#             image_name = f"dual_normal.jpeg"
#     elif selected_controller_type == "switch":
#         image_name = "switch_normal.jpeg"
#     elif selected_controller_type == "steam deck":
#         if selected_button_layout == "normal":
#             image_name = "deck_normal.jpeg"
#         else:
#             image_name = "deck_western.jpeg"
#     elif selected_controller_type == "steam":
#         image_name = "steam_pe.jpeg"
#     else:
#         image_name = "switch_normal.jpeg"

#     global controller_layout_label

#     if selected_button_layout == "elden ring":
#         image_name = image_name.replace("elden ring", "elden")
#         if selected_controller_type == "playstation":
#             controller_layout_label = elden_dual_layout
#         else:
#             controller_layout_label = elden_xbox_layout
#     elif selected_button_layout == "western":
#         if selected_controller_type == "playstation":
#             controller_layout_label = western_dual_layout
#         else:
#             controller_layout_label = western_xbox_layout
#     elif selected_button_layout == "PE":
#         if selected_controller_type == "playstation":
#             controller_layout_label = PE__dual_layout
#         else:
#             controller_layout_label = PE__xbox_layout
#     elif selected_button_layout == "normal":
#         if selected_controller_type == "playstation":
#             controller_layout_label = normal__dual_layout
#         else:
#             controller_layout_label = normal__xbox_layout

#     if selected_controller_type != "playstation" and selected_controller_type != "xbox":
#         controller_layout_label = ""

#     image_layout_label.configure(text=controller_layout_label)
#     image_layout_label.update()

#     image_path = os.path.join(script_directory, "images", image_name)
    
#     # Load and display the image
#     image = Image.open(image_path)
#     photo = customtkinter.CTkImage(image, size=(500,300))
#     image_label.configure(image=photo)
#     image_label.image = photo  # Keep a reference to the photo to prevent garbage collection
#     image_label.update()

# def select_controller(*args):
#     def change_menu(list, option_menu, option_var):
#         option_menu.configure(values=list)
#         option_var.set(list[0])
    
#     controller = controller_type.get()

#     if controller == "Xbox" or controller == "Playstation":
#         change_menu(full_button_layouts, button_layout_dropdown, button_layout)
#     elif controller == "Steam Deck":
#         change_menu(deck_button_layouts, button_layout_dropdown, button_layout) 

#     if controller == "Colored Dualsense":
#         change_menu(dualsense_colors, controller_color_dropdown, controller_color)

#     if controller == "Xbox" or controller == "Playstation":
#         change_menu(colored_button_colors, button_color_dropdown, button_color)

#     update_image()
#     repack_widgets()

# image_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="")

# image_layout_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text=f"{controller_layout_label}", font=("Roboto", 11, "bold"))

# controller_type_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Controller Type:")
# controller_type_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=controller_type, values=controller_types, command=select_controller)

# controller_color_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Controller Color:")
# controller_color_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=controller_color, values=dualsense_colors, command=update_image)

# button_color_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Button Color:")
# button_color_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=button_color, values=colored_button_colors, command=update_image)

# button_layout_label= customtkinter.CTkLabel(master=notebook.tab("Controller"), text="Button Layout:")
# button_layout_dropdown = customtkinter.CTkOptionMenu(master=notebook.tab("Controller"), variable=button_layout, values=full_button_layouts, command=update_image)

# notebook.delete("Controller") # delete this line to readd controller options

###################
####### HUD #######
###################

notebook.add("HUD")

content_frame = customtkinter.CTkFrame(master=notebook.tab("HUD"))

hud_label= customtkinter.CTkLabel(content_frame, text='Hud Location:')
center_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("HUD"), text="Center", variable=centered_HUD, value=1, command=lambda: [corner_HUD.set(False), repack_widgets])
corner_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("HUD"), text="Corner", variable=corner_HUD, value=2, command=lambda: [centered_HUD.set(False), repack_widgets])
corner_checkbox.select()

########################
####### GENERATE #######
########################

notebook.add("Generate")

emulator_label= customtkinter.CTkLabel(master=notebook.tab("Generate"), text="Select your Emulator OR choose a custom output folder, then click Generate.")
yuzu_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("Generate"), text="Yuzu/Torzu", value=1, variable=output_yuzu, command=lambda: [output_sudachi.set(False), output_ryujinx.set(False), repack_widgets()])  
ryujinx_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("Generate"), text="Ryujinx", value=2, variable=output_ryujinx, command=lambda: [output_yuzu.set(False), output_sudachi.set(False), repack_widgets()])  
sudachi_checkbox = customtkinter.CTkRadioButton(master=notebook.tab("Generate"), text="Sudachi", value=2, variable=output_sudachi, command=lambda: [output_yuzu.set(False), output_ryujinx.set(False), repack_widgets()])  

output_folder_button = customtkinter.CTkButton(master=notebook.tab("Generate"), text="Custom Output Folder", fg_color="gray", hover_color="black", command=select_output_folder)

mod_name_label = customtkinter.CTkLabel(master=notebook.tab("Generate"), text="Enter a name for the generated mod:")
mod_name_entry = customtkinter.CTkEntry(master=notebook.tab("Generate"), textvariable=mod_name_var)

open_checkbox = customtkinter.CTkCheckBox(master=notebook.tab("Generate"), text="Open Output Folder When Done", variable=open_when_done)

create_patch_button = customtkinter.CTkButton(master=notebook.tab("Generate"), text="Generate", command=create_patch)

console_label= customtkinter.CTkLabel(master=notebook.tab("Generate"), text='Console:')
scrolled_text = customtkinter.CTkTextbox(master=notebook.tab("Generate"), width=400, height=300, font=("Futura", 15))

progressbar = customtkinter.CTkProgressBar(master=notebook.tab("Generate"), orientation="horizontal")
progressbar.configure(mode="determinate", determinate_speed=.01, progress_color="green", fg_color="lightgreen", height=6, width=400)
progressbar.set(0)

#######################
####### CREDITS #######
#######################

notebook.add("Credits")

credits_label = ClickableLabel(master=notebook.tab("Credits"), text=
                    ('Utility created by fayaz\n'
                     'https://github.com/fayaz12g/BOTW-aar\n'
                     'ko-fi.com/fayaz12\n'
                     '\n\nWith special help from\n'
                     'Christopher Fields (cfields7)\n'
                     'for code beautification and being a great best friend :)'))

pack_widgets()

# select_controller()
# update_image()

root.mainloop()