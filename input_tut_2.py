import imp
import kivy
from kivy.app import App # Builds the app functionality
from kivy.uix.label import Label # Allows the creation of Labels
from kivy.uix.gridlayout import GridLayout # Allows the grid layout for a grid type layout.
from kivy.uix.textinput import TextInput # 
from kivy.uix.button import Button
from matplotlib.pyplot import cla

# FOCUSES ON ADDING WIDGETS SUCH AS BUTTONS AND LABELS TO A LAYOUT.

class MyGridLayout(GridLayout):
    # Initialize infinite keywords
    def __init__(self, **kwargs):
        # Call grid layout constructo
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 2

        # Add widgets
        self.add_widget(Label(text="Name: "))
        # Add Input Box
        self.name = TextInput(multiline=False)
        self.add_widget(self.name)

        # Add widgets
        self.add_widget(Label(text="Favorite Pizza: "))
        # Add Input Box
        self.pizza = TextInput(multiline=False)
        self.add_widget(self.pizza)

        # Add widgets
        self.add_widget(Label(text="Favorite Color: "))
        # Add Input Box
        self.color = TextInput(multiline=False)
        self.add_widget(self.color)

        # Create a Submit Button
        self.submit = Button(text="Submit", font_size = 32)
        # Bind the botton to make it do something.
        self.submit.bind(on_press = self.press)  # self.press points to the press function below so that the button knows what to do.
        self.add_widget(self.submit)

        

    def press(self, instance): # A function that tells the button what to do.
        name = self.name.text
        pizza = self.pizza.text
        color = self.color.text
        #print(f'Hello {name}, you like {pizza} pizza and your favorite color is {color}.')
        self.add_widget(Label(text=f'Hello {name}, you like {pizza} pizza and your favorite color is {color}.'))
        self.name.text = ""
        self.pizza.text = ""
        self.color.text = ""

class MyApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()