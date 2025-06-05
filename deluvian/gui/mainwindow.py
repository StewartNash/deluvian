from tkinter import *
from tkinter import ttk

from deluvian.core.droplet import Droplet
from deluvian.utils.directories import search_directory_extension, search_directory
from deluvian.utils.utilities import bdecode, pretty_print_torrent, print_tuple_list

import os

TORRENT_EXTENSION = ".torrent"
MP4_EXTENSION = ".mp4"
APPLICATION_NAME = "Deluvian"
#TORRENT_DIRECTORY = "F:\\Videos\\Torrent"
#FILE_DIRECTORY = "F:\\Videos\\Movies"
TORRENT_DIRECTORY = "/media/accessory/Extreme SSD/Torrents"
FILE_DIRECTORY = "/media/accessory/Extreme SSD/Videos"

MAXIMUM_TORRENTS = 25
MAXIMUM_FILES = 25

class ApplicationWindow:
    def __init__(self):

        # torrent_directory = StringVar(value=torrent_directory_name)
        # file_directory = StringVar(value=file_directory_name)

        self.torrent_directory_name = TORRENT_DIRECTORY
        self.file_directory_name = FILE_DIRECTORY

        self.droplet_list = []
        self.torrent_files = None
        self.torrent_files_concatenated = None
        self.torrent_list = None
        self.file_list = None
        self.filename_list = None
        self.associated_files = {}

        self.highlighted_torrents = []
        self.highlighted_files = []

        root = Tk()
        root.title(APPLICATION_NAME)
        main_window = ttk.Frame(root, padding=(3, 3, 12, 12))
        main_window.grid(column=0, row=0, sticky=(N, E, S, W))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Configure menu
        root.option_add('*tearOff', FALSE)
        root_window = Toplevel(root)
        menubar = Menu(root_window)
        root_window['menu'] = menubar
        menu_manage = Menu(menubar)
        menubar.add_cascade(menu=menu_manage, label='Manage')
        menu_manage.add_command(label='Load Association', command=self.load_association)
        menu_manage.add_command(label='Save Association', command=self.save_association)
        menu_manage.add_command(label='Load Torrents', command=self.load_torrents)
        menu_manage.add_command(label='Associate Torrents', command=self.associate_torrents)

        left_panel = ttk.Frame(main_window)
        # middle_panel = ttk.Frame(main_window, width=360)
        middle_panel = ttk.Frame(main_window)
        right_panel = ttk.Frame(main_window)
        left_panel.grid(column=0, row=0, rowspan=2, sticky=(N, E, S, W))
        middle_panel.grid(column=1, row=0, sticky=(N, S))
        # middle_panel.grid_propagate(False)
        right_panel.grid(column=2, row=0, sticky=(N, E, S, W))

        # right_upper_panel = ttk.Frame(middle_panel)
        # right_lower_panel = ttk.Frame(middle_panel)
        # right_upper_panel.grid(column=0, row=0, sticky=(N, E, W))
        # right_lower_panel.grid(column=0, row=1, sticky=(E, W, S))

        # torrent_directory_entry = ttk.Entry(right_upper_panel)
        # file_directory_entry = ttk.Entry(right_upper_panel)

        self.torrent_directory = StringVar()
        self.file_directory = StringVar()
        self.torrent_directory.set(self.torrent_directory_name)
        self.file_directory.set(self.file_directory_name)

        torrent_directory_entry = ttk.Entry(middle_panel, textvariable=self.torrent_directory)
        file_directory_entry = ttk.Entry(middle_panel, textvariable=self.file_directory)
        torrent_directory_entry.grid(column=0, row=0)
        file_directory_entry.grid(column=0, row=1)

        self.populate_torrents()
        self.update_files()
        self.correlate_files()

        self.torrent_listbox = Listbox(left_panel, listvariable=self.torrent_list)
        self.torrent_listbox.bind("<<ListboxSelect>>", lambda e: self.torrent_listbox_changed(self.torrent_listbox.curselection()))
        self.torrent_listbox.grid(column=0, row=0, sticky=(N, E, S, W))

        self.file_listbox = Listbox(right_panel, listvariable=self.filename_list)
        self.file_listbox.bind("<<ListboxSelect>>", lambda e: self.file_listbox_changed(self.file_listbox.curselection()))
        self.file_listbox.grid(column=0, row=0, sticky=(N, E, S, W))

        main_window.columnconfigure(0, weight=2)
        main_window.columnconfigure(1, weight=1)
        main_window.columnconfigure(2, weight=2)
        main_window.rowconfigure(0, weight=1)

        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)

        # file_text = Text(right_lower_panel)
        self.file_text = Text(middle_panel, wrap="none")
        # file_text.grid(column=0, row=0, sticky=(N, E, S, W))
        info_scrollbar_vertical = Scrollbar(middle_panel, orient=VERTICAL)
        info_scrollbar_horizontal = Scrollbar(middle_panel, orient=HORIZONTAL)
        self.file_text['xscrollcommand'] = info_scrollbar_horizontal.set
        self.file_text['yscrollcommand'] = info_scrollbar_vertical.set
        info_scrollbar_vertical.config(command=self.file_text.yview)
        info_scrollbar_horizontal.config(command=self.file_text.xview)
        self.file_text.grid(column=0, row=2, sticky=(N, E))
        info_scrollbar_vertical.grid(column=1, row=2, sticky=(N, S, W))
        info_scrollbar_horizontal.grid(column=0, row=3, stick=(S, E, W))

        file_scrollbar_vertical = Scrollbar(right_panel, orient=VERTICAL)
        self.file_listbox.config(yscrollcommand=file_scrollbar_vertical.set)
        file_scrollbar_vertical.config(command=self.file_listbox.yview)
        file_scrollbar_vertical.grid(column=1, row=0, sticky=(N, S, W))

        # self.file_text.insert('1.0', 'Lorem ipsum dolor sit amet')

        self.correlate_files()

        root.mainloop()

    def torrent_listbox_changed(self, selection):
        self.torrent_listbox.configure(background="white")
        self.file_listbox.configure(background="white")
        if selection:
            self.update_torrent_info(selection)
            self.highlight_selected_items(selection[0])

    def file_listbox_changed(self, selection):
        self.torrent_listbox.configure(background="white")
        self.file_listbox.configure(background="white")
        if selection:
            self.highlight_selected_items(selection[0], is_torrent=False)

    def update_torrent_info(self, selection):
        self.clear_file_info()
        # print(self.torrent_files_concatenated)
        filename = self.torrent_files_concatenated[selection[0]]
        file_output = bdecode(filename)
        file_info = pretty_print_torrent(file_output)
        self.file_text.insert(END, file_info)
        temporary = ""
        for x in self.droplet_list[selection[0]].get_associated_file():
            temporary = temporary + "\n" + os.path.join(x[ROOT_INDEX], x[FILENAME_INDEX])
        self.file_text.insert(END, temporary)
        # self.file_text.insert(END, print_tuple_list())

    def update_torrent_list(self):
        self.torrent_files, self.torrent_files_concatenated = search_directory_extension(self.torrent_directory_name, TORRENT_EXTENSION, maximum_files = MAXIMUM_TORRENTS)
        self.torrent_list = StringVar(value=self.torrent_files_concatenated)

    def populate_torrents(self):
        self.torrent_files, self.torrent_files_concatenated = search_directory_extension(self.torrent_directory_name, TORRENT_EXTENSION, maximum_files = MAXIMUM_TORRENTS)
        self.torrent_list = StringVar(value=self.torrent_files_concatenated)
        self.droplet_list.clear()
        for torrent_file in self.torrent_files_concatenated:
            self.droplet_list.append(Droplet(torrent_file, bdecode(torrent_file)))

    def update_files(self):
        input_1, input_2 = search_directory(self.file_directory_name, maximum_files = MAXIMUM_FILES)
        self.file_list = input_1
        self.filename_list = StringVar(value=input_2)

    def correlate_files(self):
        index = 0
        for x in self.droplet_list:
            x.clear_associated_file()
            indices = add_similar_files(x, self.file_list)
            if indices:
                self.associated_files[index] = indices
            index = index + 1

    def clear_file_info(self):
        self.file_text.delete(1.0, END)

    def highlight_selected_items(self, selected_item, is_torrent=True):
        self.clear_highlighted_items()
        if is_torrent:
            if selected_item in self.associated_files:
                for x in self.associated_files[selected_item]:
                    self.set_highlighted_items(x, is_torrent=False)
        else:  # It is a file
            for key in self.associated_files.keys():
                value = self.associated_files[key]
                if selected_item in value:
                    self.set_highlighted_items(key)

    def set_highlighted_items(self, number, is_torrent=True):
        if is_torrent:
            self.torrent_listbox.itemconfig(number, {'bg': 'green'})
            self.highlighted_torrents.append(number)
        else:
            self.file_listbox.itemconfig(number, {'bg': 'green'})
            self.highlighted_files.append(number)

    def clear_highlighted_items(self):
        for key in self.highlighted_torrents:
            self.torrent_listbox.itemconfig(key, {'bg': 'white'})
        for key in self.highlighted_files:
            self.file_listbox.itemconfig(key, {'bg': 'white'})
        self.highlighted_torrents.clear()
        self.highlighted_files.clear()

    def load_association(self):
        None

    def save_association(self):
        None

    def load_torrents(self):
        None

    def load_files(self):
        None

    def associate_torrents(self):
        None



    # def torrent_files_concatenated(self):
    #     torrent_files, torrent_files_concatenated = search_directory_extension(self.torrent_directory_name, TORRENT_EXTENSION)
    #     return torrent_files_concatenated


ROOT_INDEX = 0
FILENAME_INDEX = 1

FILEPATH_INDEX = 0
LENGTH_INDEX = 1


def add_similar_files(droplet, file_list):
    associated_file_indices = []
    index = 0
    for x in file_list:
        root = x[ROOT_INDEX]
        filename = x[FILENAME_INDEX]
        # print(filename)
        if droplet.files is not None:
            for y in droplet.files:
                if filename == y[FILEPATH_INDEX]:
                    # print(filename)
                    droplet.add_associated_file((root, filename))
                    associated_file_indices.append(index)
        else:
            if filename == droplet.name:
                # print(filename)
                droplet.add_associated_file((root, filename))
                associated_file_indices.append(index)
        index = index + 1
    return associated_file_indices

