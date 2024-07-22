import ttkbootstrap as ttk
from tkinter import font


class App:
    """
	simple tkinter app used to preview all the fonts on your system
	"""

    def __init__(self) -> None:

        self.__main_window = ttk.Window()
        self.__main_window.geometry("850x600")
        self.__main_window.title("Font Preview")
        self.__main_window.maxsize(950, 620)
        self.__main_window.minsize(750, 550)
        self.__main_window.iconbitmap("assets/icon.ico")

        self.__style = ttk.Style()
        self.__theme_names = self.__style.theme_names()

        # top frame
        self.__top_frame = ttk.Frame(self.__main_window, padding=(10, 10, 10, 0))
        self.__top_frame.pack(fill="x")

        self.__ft_lbl = ttk.Label(master=self.__top_frame, text="Fonts Preview", font="-size 16")
        self.__ft_lbl.pack(side="left")

        self.__theme_cbo = ttk.Combobox(master=self.__top_frame, values=self.__theme_names)
        self.__theme_cbo.pack(padx=10, side="right")
        self.__theme_cbo.current(self.__theme_names.index(self.__style.theme.name))
        self.__theme_cbo.bind("<<ComboboxSelected>>", self.change_theme)

        self.__theme_lbl = ttk.Label(master=self.__top_frame, text="Change theme:")
        self.__theme_lbl.pack(side="right")

        ttk.Separator(self.__main_window).pack(fill="x", pady=10, padx=10)

        # left frame
        self.__left_frame = ttk.Frame(master=self.__main_window)
        self.__left_frame.pack(fill="y", pady=10, padx=10, side="left")

        self.__ft_treeview = ttk.Treeview(master=self.__left_frame, columns=(1), height=10, bootstyle="success",
                                          show="headings")
        self.__ft_treeview.heading(1, text="Fonts")
        self.__ft_treeview.column(1, minwidth=15, anchor="center", stretch=ttk.YES)
        self.__ft_treeview.bind("<ButtonRelease-1>", self.load_font)
        self.__ft_treeview.pack(fill="both", expand="yes")

        self.__query_var = ttk.StringVar()
        self.__query_var.trace("w", self.search_treeview)
        self.__search_entry = ttk.Entry(self.__left_frame, bootstyle="success", textvariable=self.__query_var)
        self.__search_entry.pack(fill="x", pady=10)

        self.fill_treeview_with_ft()
        ttk.Separator(self.__main_window, orient="vertical").pack(fill="y", pady=(10, 15), side="left")

        # rigth frame
        self.__right_frame = ttk.Frame(master=self.__main_window)
        self.__right_frame.pack(fill="both", padx=10, pady=10, side="left", expand=True)

        self.__selected_ft_name = ttk.StringVar()
        self.__ft_name = ttk.Label(master=self.__right_frame, text="Font Name:", font="-size 14")
        self.__ft_name.pack(fill="x", pady=(0, 6))
        self.__ft_name_lbl = ttk.Label(master=self.__right_frame, font="-size 16", textvariable=self.__selected_ft_name)
        self.__ft_name_lbl.pack(fill="x", pady=(0, 20))

        self.__sample_text = ttk.StringVar()
        self.__temp = None
        self.__sample_text.set("This is a sample text")
        self.__sample_text_lbl = ttk.Label(master=self.__right_frame, text="Sample Text:", font=("normal", 14))
        self.__sample_text_lbl.pack(fill="x", pady=(0, 6))
        self.__sample_text_entry = ttk.Entry(master=self.__right_frame, textvariable=self.__sample_text,
                                             font="-size 12", bootstyle="success")
        self.__sample_text_entry.pack(fill="x", pady=(0, 20))

        self.__ft_size_lbl = ttk.Label(master=self.__right_frame, text="Font Size:", font="-size 14")
        self.__ft_size_lbl.pack(fill="x", pady=(0, 6))
        self.__ft_size_slider = ttk.Scale(master=self.__right_frame, orient="horizontal", from_=1, to=36, value=12,
                                          bootstyle="success")
        self.__ft_size_slider.configure(command=self.change_size)
        self.__ft_size_slider.pack(fill="x", pady=(0, 20))

        self.__bold_text = ttk.Label(self.__right_frame, textvariable=self.__sample_text,
                                     font=(self.__selected_ft_name.get(), int(self.__ft_size_slider.get()), "bold"))
        self.__bold_text.pack(fill="x")

        self.__italic_text = ttk.Label(master=self.__right_frame, textvariable=self.__sample_text,
                                       font=(self.__selected_ft_name.get(), int(self.__ft_size_slider.get()), "italic"))
        self.__italic_text.pack(fill="x")

        # main_ window loop
        self.__main_window.mainloop()

    def change_theme(self, event: object) -> None:
        # change the window theme

        t = self.__theme_cbo.get()
        self.__style.theme_use(t)
        self.__theme_cbo.selection_clear()

    def fill_treeview_with_ft(self) -> None:
        # fill the tree-view with fonts on the system

        fonts = font.families(root=self.__main_window)

        counter = 0
        self.__ft_treeview.delete(*self.__ft_treeview.get_children())
        for font_ in fonts:
            self.__ft_treeview.insert(parent="", index=ttk.END, iid=counter, values=font_)
            counter += 1

    def search_treeview(self, *args) -> None:
        # searching the tree view for font matching text in __search_entry

        if self.__query_var.get() == "":
            self.fill_treeview_with_ft()
        else:
            query_string = self.__query_var.get()
            if query_string == "":
                return None

            matching_fonts = []
            for child_element in self.__ft_treeview.get_children():
                temp_var = str(self.__ft_treeview.item(child_element)["values"][0].lower())
                if query_string in temp_var:
                    matching_fonts.append(temp_var)

            self.__ft_treeview.delete(*self.__ft_treeview.get_children())
            counter = 0
            for font_ in matching_fonts:
                self.__ft_treeview.insert(parent="", index=ttk.END, iid=counter, values=font_)
                counter += 1

    def load_font(self, event) -> None:
        # load font onto the right frame

        if (font_row := self.__ft_treeview.focus()) == "":
            return

        focused_font = self.__ft_treeview.get_children()[int(font_row)]
        font_records = self.__ft_treeview.item(focused_font)

        self.__selected_ft_name.set(font_records["values"])
        self.__temp = font_records["values"]
        self.__bold_text.configure(font=(font_records["values"], int(self.__ft_size_slider.get()), "bold"))
        self.__italic_text.configure(font=(font_records["values"], int(self.__ft_size_slider.get()), "italic"))

    def change_size(self, *args) -> None:
        # changing the size of the sample text labels

        self.__bold_text.configure(font=(self.__temp, int(self.__ft_size_slider.get()), "bold"))
        self.__italic_text.configure(font=(self.__temp, int(self.__ft_size_slider.get()), "italic"))


if __name__ == "__main__":
    App()
