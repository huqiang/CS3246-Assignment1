from Tkinter import *

PAD_X = 1
PAD_Y = 1
IPAD_X = 2
IPAD_Y = 2
BORDER_WIDTH = 0

class ResultsTable(Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        Frame.__init__(self, parent, background="black")
        self._widgets = []
        self._rows = rows
        self._columns = columns
        self._checkbox_states = []
        for row in range(rows):
            current_row = []
            # for column in range(columns):
            
            rank_label = Label(self, text="", borderwidth=BORDER_WIDTH, width=5)
            rank_label.grid(row=row, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y, ipadx=IPAD_X, ipady=IPAD_Y)
            current_row.append(rank_label)

            file_label = Label(self, text="", borderwidth=BORDER_WIDTH, width=10)
            file_label.grid(row=row, column=1, sticky="nsew", padx=PAD_X, pady=PAD_Y, ipadx=IPAD_X, ipady=IPAD_Y)
            current_row.append(file_label)

            title_label = Label(self, text="", borderwidth=BORDER_WIDTH, width=50, wraplength=500, anchor='w', justify='left')
            title_label.grid(row=row, column=2, sticky="nsew", padx=PAD_X, pady=PAD_Y, ipadx=IPAD_X, ipady=IPAD_Y)
            current_row.append(title_label)

            synopsis_label = Label(self, text="", borderwidth=BORDER_WIDTH, width=75, wraplength=750, anchor='w', justify='left')
            synopsis_label.grid(row=row, column=3, sticky="nsew", padx=PAD_X, pady=PAD_Y, ipadx=IPAD_X, ipady=IPAD_Y)
            current_row.append(synopsis_label)

            if row == 0:
                relevance_label = Label(self, text="", borderwidth=BORDER_WIDTH, width=10)
            else:
                cb_state = IntVar()
                cb_state.set(0)
                relevance_label = Checkbutton(self, variable=cb_state)
                self._checkbox_states.append(cb_state)
            relevance_label.grid(row=row, column=4, sticky="nsew", padx=PAD_X, pady=PAD_Y, ipadx=IPAD_X, ipady=IPAD_Y)
            current_row.append(relevance_label)

            self._widgets.append(current_row)

        self.init_table_headers()

    def init_table_headers(self):
        table_headers = ['Rank', 'File', 'Title', 'Synopsis', 'Relevant']
        for i in range(len(table_headers)):
            self.set(i, 0, table_headers[i])

    def set(self, column, row, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def reset_table(self):
        for i in range(self._rows):
            for j in range(self._columns):
                self.set(j, i, '')
        for i in range(1, self._rows):
            self._checkbox_states[i-1].set(0)
        self.init_table_headers()

    def get_checked_results(self):
        checked_docs = []
        print self._checkbox_states
        for i in range(1, self._rows):
            if self._checkbox_states[i-1].get() == 1:
                checked_docs.append(self._widgets[i][1].cget('text'))
        print checked_docs
        return checked_docs
