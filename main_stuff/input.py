from tkinter import Scrollbar
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.scrollview import ScrollView
import csv
from plyer import filechooser
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from requests import head

Window.size = (400,400)

# Global variables
# Stored information as a dictionary with the keys being the values stored from the column head.
data_list = []
data_per_column = {} # Column: Data of Column
can_be_float_converted = {} # 
path = ""
stat_options = {}
count_dictionary = {} # Column: Data Value: Count of Data Value
percentage_dictionary = {} # Column: Unique Data Value: Percentage Ratio of Data Value to total

# Used for calculations of float data types.
# Each dictionary is broken out by KEY: KEY: KEY: Data or List
data_per_unique_dictionary = {} # Column of Unique Values: Unique Data Value: Column to analyze: All Data From CSV file as a list
sum_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Sum: Sum
max_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Max: Max
min_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Min: Min
avg_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Avg: Avg
median_dictionary = {} # Column of Unique Values: Unique Data Values: Column to Sum: Sum
total_records = 0 # Total Row of Records
column_count = 0
header_column =[]
header_run = {}
calc_header_run = {}



# Declare Screens
class Startup(Screen):

    def press(self):
        global header_column

    # Used to open csv file.
    def file_selector(self):
        global path, header_column, data_list, column_count, total_records, index, data_per_column, can_be_float_converted, header_run, calc_header_run
        header_run.clear()
        calc_header_run.clear()
        path = filechooser.open_file(title="Pick a CSV file..", 
                             filters=[("Comma-separated Values", "*.csv")])
        name = path[0]
        file = open(name)
        csvreader = csv.reader(file)
        header_column = next(csvreader)
        local = str(header_column)
        data_list = [row for row in csvreader]
        column_count = len(header_column)
        total_records = len(data_list)

        # All data from CSV file will be stored in data_per_column for processing.
        # Achieved by DF = pd.read_csv(FILEPATH[0])
        index = 0
        for each_column in header_column:
            data_per_column[each_column] = [0] * total_records
            for each in range(0,total_records):
                data_per_column[each_column][each] = data_list[each][index]
            index += 1
        
        # Checks for the ability to convert data in a column to a floating point for math purposes.
        # Achieved by result = DF.select_dtypes(include='number')
        for each in data_per_column:
            if "ID" in each or "id" in each:
                can_be_float_converted[each] = False
            else:
                can_be_float_converted[each] = self.data_type_checker(data_per_column[each])
        file.close()
        
    # Checks if a data type can be converted to a float for math calculations. 
    # Achieved by result = DF.select_dtypes(include='number') as stated previously
    def data_type_checker(self,some_list): 
        can_be_converted = True
        for each in some_list:
            try:
                float(each)
            except ValueError:
                can_be_converted = False
            if can_be_converted == False:
                return can_be_converted
        return can_be_converted

    # Determines what is stat options can be worked based on data types. Uses "can_be_float_converted" dictionary as an input.
    # IN PROGRESS: This can be achieved by creating a functions that takes in the df column and a boolean- num or not
    # df_column_methods which will include all required pandas methods. 
    # based on the boolean -> exactly how Rey has implemented it, we will selectively run the methods
    # e.g. df.nunique() will give uniqe counts from the data in a column
    def options(self,some_dictionary):
        global stat_options
        for each in some_dictionary:
            if some_dictionary[each] == True:
                stat_options[each] = ["Counts Per Value", "Percentage Ratio", "Sum", "Max", "Min", "Average", "Median"]
            else:
                stat_options[each] = ["Counts Per Value", "Percentage Ratio"]

class Display_1(Screen):
    global can_be_float_converted, header_run

    def go_next_function(self, value):
        if self.manager.current == 'display_1':
            self.manager.current = 'display_2'
            self.manager.transition.direction = "right"
            self.clear_up_page()
    
    def checkbox_function(self, checkbox, value):
        return value

    def data_fill(self):
        global header_column, header_run
        
        grid = GridLayout(
            cols = 1
            )
        go_back = Button(text="Next",
            font_size = 24
			)
        go_back.bind(on_press = self.go_next_function)
        grid1 = GridLayout(cols = 2 )
        grid1.add_widget(Label(text='Group By', font_size = 24))
        grid1.add_widget(go_back)
        for each in header_column:
            if can_be_float_converted[each] is False:
                grid1.add_widget(Label(text=each))
                # new_checkbox = CheckBox()
                header_run[each] = CheckBox()
                header_run[each].bind(active = self.checkbox_function)
                grid1.add_widget(header_run[each])
        grid.add_widget(grid1)
        self.add_widget(grid)

    
    def clear_up_page(self):
        self.clear_widgets()


class Display_2(Screen):
    global can_be_float_converted, calc_header_run
    def go_next_function(self, value):
        if self.manager.current == 'display_2':
            self.manager.current = 'startup'
            self.manager.transition.direction = "right"
            self.clear_up_page()
    
    def checkbox_function(self, checkbox, value):
        return value


    def data_fill(self):
        global header_column, calc_header_run
        grid = GridLayout(
            cols = 1
            )
        go_back = Button(text="Finish",
            font_size = 24
			)
        go_back.bind(on_press = self.go_next_function)
        grid1 = GridLayout(cols = 2 )
        grid1.add_widget(Label(text='Calculatable', font_size = 24))
        grid1.add_widget(go_back)
        for each in header_column:
            if can_be_float_converted[each] is True:
                grid1.add_widget(Label(text=each))
                calc_header_run[each] = CheckBox()
                calc_header_run[each].bind(active = self.checkbox_function)
                grid1.add_widget(calc_header_run[each])
        grid.add_widget(grid1)
        self.add_widget(grid)

    
    def clear_up_page(self):
        self.clear_widgets()

# Data Analysis screen/window
class Display_3(Screen):
    """Screen for displaying statistics from given csv file."""
    global data_per_column, data_per_unique_dictionary, sum_dictionary, max_dictionary, min_dictionary, avg_dictionary, median_dictionary, header_run

    def switchScreens(self, value):
        """Switch from display screen to startup screen."""
        if self.manager.current == 'display_3':
            self.manager.current = 'startup'
            self.manager.transition.direction = "right"
            self.clear_up_page()
    
    def clear_up_page(self):
        self.clear_widgets()

    def build_columns_as_tabs(self):
        """Create, populate & add tabbed_panel"""
        global path
        global DF0
        DF = pd.read_csv(path[0])
        tp = TabbedPanel()
        tp.do_default_tab = False
        for column_header in header_run:
            if (header_run[column_header].active is True):
                th = TabbedPanelHeader(text=column_header)
                tp.add_widget(th)
                layout = GridLayout(cols = 6 )
                layout.bind(minimum_height=layout.setter('height'))
                result = self.count_per_value(column_header) 
                for calc_column_header in calc_header_run:
                    if (calc_header_run[calc_column_header].active is True):
                        self.per_unique_setup(column_header,calc_column_header)
                        temp_list = self.calcs_per_unique(column_header, calc_column_header)
                        for each in temp_list:
                            result.append(each)
                for each in result:
                    layout.add_widget(each)
                th.content = layout
        for calc_column_header in calc_header_run:
            if (calc_header_run[calc_column_header].active is True):
                th = TabbedPanelHeader(text=calc_column_header)
                tp.add_widget(th)
                result = str(DF[calc_column_header].describe())
                new_label_calc = Label(text = result, halign = 'left', font_size = 32)
                th.content = new_label_calc

        # Add back button to bottom of display screen
        grid = GridLayout(cols=1)
        back_btn = Button(
            text="Select Another Data Set", 
            size_hint_y = None, # turns off auto sizing for height.  Needs to be set to none if trying to manually set.
            height = 50) # manually sets the height of button.
        back_btn.bind(on_press=self.switchScreens)
        grid.add_widget(tp)
        grid.add_widget(back_btn)
        self.add_widget(grid)


    def count_per_value(self, column):
        checked_list = []
        global count_dictionary, percentage_dictionary, total_records
        count_dictionary[column] = {}
        percentage_dictionary[column] = {}
        result = []
        for each in range(2):
            result.append(Label(text = ""))
        result.append(Label(text = "Counts & Perctentage Ratios Per " + column, font_size = 24, halign = 'left'))
        for each in range(3):
            result.append(Label(text = ""))
        some_num = 15
        for each in data_per_column[column]:
            if each not in checked_list:
                checked_list.append(each)
                count_dictionary[column][each] = data_per_column[column].count(each)
                percentage_dictionary[column][each] = round(((count_dictionary[column][each] / total_records)*100),2)               
                result.append(Label(text = each))
                result.append(Label(text = ("Count = " + str(count_dictionary[column][each]))))
                result.append(Label(text = ("Percentage Ratio = " + str(percentage_dictionary[column][each])), halign = 'left'))
                result.append(Label(text = ""))
                result.append(Label(text = ""))
                result.append(Label(text = ""))
            else:
                continue
        return result

    # Stores all data per column, unique_value, column_to_store into data_per_unique_dictionary for future prints and functions.
    # Prepares other dictionaries for certain values.
    def per_unique_setup(self,column,column_to_store):
        global data_per_column, data_per_unique_dictionary, sum_dictionary, max_dictionary, min_dictionary, avg_dictionary, median_dictionary
        data_per_unique_dictionary[column] = {}
        sum_dictionary[column] = {} # Column: Unique Data Value: Count of Data Value
        max_dictionary[column] = {}
        min_dictionary[column] = {}
        avg_dictionary[column] = {}
        median_dictionary[column] = {}
        checked_list = []
        for each in data_per_column[column]:
            if each not in checked_list:
                checked_list.append(each)
                data_per_unique_dictionary[column][each] = {}
                sum_dictionary[column][each] = {}
                max_dictionary[column][each] = {}
                min_dictionary[column][each] = {}
                avg_dictionary[column][each] = {}
                median_dictionary[column][each] = {}

                data_per_unique_dictionary[column][each][column_to_store] = []
                sum_dictionary[column][each][column_to_store] = []
                max_dictionary[column][each][column_to_store] = []
                min_dictionary[column][each][column_to_store] = []
                avg_dictionary[column][each][column_to_store] = []
                median_dictionary[column][each][column_to_store] = []
            else:
                continue
        for each in range(0,total_records):
            data_per_unique_dictionary[column][str(data_per_column[column][each])][column_to_store].append(float(data_per_column[column_to_store][each]))

    
    # Calculate sums per unique item.
    def calcs_per_unique(self,column,column_to_stat):
        global data_per_unique_dictionary
        result = []
        for each in range(2):
            result.append(Label(text = ""))
        result.append(Label(text = "Sum, Min, Max, Average, & Median Per " + column + " for the column " + column_to_stat, font_size = 24))
        for each in range(3):
            result.append(Label(text = ""))
        if column not in data_per_unique_dictionary:
            self.per_unique_setup(column,column_to_stat)
        for each in data_per_unique_dictionary[column]:
            sum_dictionary[column][each][column_to_stat] = round(np.sum(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            min_dictionary[column][each][column_to_stat] = round(min(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            max_dictionary[column][each][column_to_stat] = round(max(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            avg_dictionary[column][each][column_to_stat] = round(np.average(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            median_dictionary[column][each][column_to_stat] = round(np.median(data_per_unique_dictionary[column][each][column_to_stat]), 2)
            result.append(Label(text = str(each)))
            result.append(Label(text = ("Sum = " + str(sum_dictionary[column][each][column_to_stat])), halign = 'left'))
            result.append(Label(text = ("Min = " + str(min_dictionary[column][each][column_to_stat])), halign = 'left'))
            result.append(Label(text = ("Max = " + str(max_dictionary[column][each][column_to_stat])), halign = 'left'))
            result.append(Label(text = ("Average = " + str(avg_dictionary[column][each][column_to_stat])), halign = 'left'))
            result.append(Label(text = ("Median = " + str(median_dictionary[column][each][column_to_stat])), halign = 'left'))
        return result

kv_file = Builder.load_file('inputStatDesign.kv')

class MyApp(App):
    # Window Title
    title = 'QuickStat'

    def build(self):
        return ScreenManager()

if __name__ == '__main__':
    MyApp().run()



