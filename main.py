# Jake Prisby, Abdel Rahman Albasha, and Nathaniel Burton
# CS 465 
# Winter 2024
# Project #1 

from pack.InfoRetrieval import InfoRetrieval
from pack.InfoRetrieval import soundex, process_string
import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, master):
        self.master = master
        master.title("Text Analysis GUI")

        # Create tabs
        self.tabControl = ttk.Notebook(master)

        # Queries Tab
        self.query_frame = ttk.Frame(self.tabControl)
        self.tabControl.add(self.query_frame, text='Queries')
        self.query_op = 'and'
        self.create_query_tab()

        # Statistics Tab
        self.stats_frame = ttk.Frame(self.tabControl)
        self.tabControl.add(self.stats_frame, text='Word Statistics')
        self.create_stats_tab()

        # Inverted Index Tab
        self.doc_stats_frame = ttk.Frame(self.tabControl)
        self.tabControl.add(self.doc_stats_frame, text='Document Statistics')
        self.create_doc_tab()

        # Pack the tabs
        self.tabControl.pack(expand=1, fill="both")

    def create_query_tab(self):
        # Widgets for Queries Tab
        self.query_label = tk.Label(self.query_frame, text="Enter words:")
        self.query_label.grid(row=0, column=0, padx=10, pady=10)

        self.query_entry1 = tk.Entry(self.query_frame, width=30)
        self.query_entry1.grid(row=0, column=1, padx=10, pady=10)

        self.and_or_var = tk.StringVar()
        self.and_or_var.set("and")

        self.operation_button = tk.Button(self.query_frame, text='AND', command=self.query_op_switch)
        self.operation_button.grid(row=0, column=2, padx=10, pady=10)

        self.query_entry2 = tk.Entry(self.query_frame, width=30)
        self.query_entry2.grid(row=0, column=3, padx=10, pady=10)

        self.submit_button = tk.Button(self.query_frame, text="Submit", command=self.on_query_submit)
        self.submit_button.grid(row=0, column=4, padx=10, pady=10)

        res_label = tk.Label(self.query_frame, text="Results:", anchor='w')
        res_label.grid(row=1, column=0, columnspan=5, sticky="ew", padx=10)

        self.query_res_tb = tk.Text(self.query_frame, height=10, width=100, wrap='word')
        self.query_res_tb.grid(row=2, column=0, columnspan=5, padx=10, pady=(0, 10))
        self.query_res_tb.config(state=tk.DISABLED)

    def on_query_submit(self):
        res = []
        try:
            try:
                word1 = self.query_entry1.get()
            except:
                word1 = ''
            word1 = process_string(word1)[0]
            try:
                word2 = self.query_entry2.get()
            except:
                word2 = ''
            word2 = process_string(word2)[0]
            res = IR.binary_query(word1, word2, self.query_op)
        except: 
            pass
        self.query_res_tb.config(state=tk.NORMAL)
        self.query_res_tb.delete('1.0', 'end')
        self.query_res_tb.insert(tk.END, str(res))
        self.query_res_tb.config(state=tk.DISABLED)
        
    def query_op_switch(self):
        if self.query_op == 'and':
            self.query_op = 'or'
        else:
            self.query_op = 'and'
        self.operation_button.config(text=self.query_op.upper())

    def create_stats_tab(self):
        # Widgets for Statistics Tab
        self.stat_scroll_bar_frame = ttk.Frame(self.stats_frame)
        self.stat_scroll_bar_frame.pack(side='left', fill='both', expand='true')

        self.stats_listbox = tk.Listbox(self.stat_scroll_bar_frame, selectmode=tk.SINGLE )
        self.stats_listbox.pack(side='left', fill='both', expand=True)
        self.stats_listbox.bind("<<ListboxSelect>>", self.on_word_select)
        
        self.stat_scroll = tk.Scrollbar(self.stat_scroll_bar_frame)
        self.stat_scroll.pack(side='right', fill='both')
        self.stats_listbox.config(yscrollcommand= self.stat_scroll.set)
        self.stat_scroll.config(command = self.stats_listbox.yview)


        self.stat_tb_scroll_bar_frame = ttk.Frame(self.stats_frame)
        self.stat_tb_scroll_bar_frame.pack(side='right', fill='both', expand='true')

        self.stats_tb = tk.Text(self.stat_tb_scroll_bar_frame, wrap='word')
        self.stats_tb.pack(side='left', fill='both', expand=True)

        self.stat_tb_scroll = tk.Scrollbar(self.stat_tb_scroll_bar_frame)
        self.stat_tb_scroll.pack(side='right', fill='both')
        self.stats_tb.config(yscrollcommand= self.stat_tb_scroll.set)
        self.stat_tb_scroll.config(command=self.stats_tb.yview)

        self.stats_tb.config(state=tk.DISABLED)

        # Load all of the terms into the list box
        words = sorted(IR.inverted_index.keys())
        for word in words:
            self.stats_listbox.insert(tk.END, word)

    def on_word_select(self, event):
        selected_word = self.stats_listbox.get(self.stats_listbox.curselection())

        str = 'Term Specific Stats:\n'
        str += f"Word: {selected_word}\n"
        str += f"Term Frequency: {IR.word_total_occurence(selected_word)}\n"
        str += f'Doc Frequency: {len(IR.inverted_index[selected_word])}\n'
        str += "Posting List(doc name: freq in doc):\n"
        for doc in IR.inverted_index[selected_word]:
            if (doc != IR.inverted_index[selected_word][-1]):
                str += f'\t{doc}: {IR.word_counter[doc][selected_word]},\n'
            else:
                str += f'\t{doc}: {IR.word_counter[doc][selected_word]}\n'

        str += f"Soundex Code: {soundex(selected_word)}\n"

        str+= '\nGlobal Stats:\n'
        str+= f'Top 100th Word: {IR.get_nth_most_frequent_word(100)}\n'
        str += f'Top 500th Word: {IR.get_nth_most_frequent_word(500)}\n'
        str += f'Top 1000th Word: {IR.get_nth_most_frequent_word(1000)}\n'
        self.stats_tb.config(state=tk.NORMAL)
        self.stats_tb.delete('1.0', 'end')
        self.stats_tb.insert(tk.END, str)
        self.stats_tb.config(state=tk.DISABLED)

    def create_doc_tab(self):
        # Widgets for Inverted Index Tab
        self.doc_scrollbar_frame = ttk.Frame(self.doc_stats_frame)
        self.doc_scrollbar_frame.pack(side='left', fill='both', expand=True)

        self.doc_stats_listbox = tk.Listbox(self.doc_scrollbar_frame, selectmode=tk.SINGLE)
        self.doc_stats_listbox.pack(side='left', fill='both', expand=True)
        self.doc_stats_listbox.bind("<<ListboxSelect>>", self.on_doc_select)

        self.doc_scrollbar = tk.Scrollbar(self.doc_scrollbar_frame)
        self.doc_scrollbar.pack(side='right', fill='both', expand=True)
        self.doc_stats_listbox.config(yscrollcommand=self.doc_scrollbar.set)
        self.doc_scrollbar.config(command=self.doc_stats_listbox.yview)

        self.doc_stats_tb = tk.Text(self.doc_stats_frame, wrap='word')
        self.doc_stats_tb.pack(side='right', fill='both', expand=True)
        self.doc_stats_tb.config(state=tk.DISABLED)
        docs = sorted(IR.word_counter.keys())
        for doc in docs:
            self.doc_stats_listbox.insert(tk.END, doc)

    def on_doc_select(self, event):
        selected_doc = self.doc_stats_listbox.get(self.doc_stats_listbox.curselection())
        str = 'Document Specific Stats:\n'
        str += f'Document: {selected_doc}\n'
        str += f"Distinct Words: {IR.doc_unique_word_count(selected_doc)}\n"
        str += f'Total Words: {IR.doc_total_word_count(selected_doc)}\n'

        str += '\nCollection Stats: \n'
        str += f'Distinct Words: {IR.collection_unique_word_count()}\n'
        str += f"Total Words: {IR.collection_total_word_count()}\n"
        self.doc_stats_tb.config(state=tk.NORMAL)
        self.doc_stats_tb.delete('1.0', 'end')
        self.doc_stats_tb.insert(tk.END, str)
        self.doc_stats_tb.config(state=tk.DISABLED)


if __name__ == '__main__':
    IR = InfoRetrieval() # Information retrieval object
    # Create the main window
    root = tk.Tk()
    app = App(root)
    # Run the main loop
    root.mainloop()