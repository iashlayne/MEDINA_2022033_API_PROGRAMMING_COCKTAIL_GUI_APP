import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json


# Created a class CocktailGUIApp:
class CocktailGUIApp:
    # defined a method self window for the GUI app self and window for tkinter 
    def __init__(self, window):
        self.window = window
        # Title of the Gui app
        self.window.title("Cocktail Drinks GUI App")
        # Size of the window
        self.window.geometry("1350x832")
        # Resizable False for constant window
        self.window.resizable(False, False)
        
        # image path of the background
        image_path = "/Users/iashlaynemedina/Desktop/New Folder With Items 2/SY 2023-2024/CC SEM 2 2024 Files/Programming API/Images/image_1.png"
        # To open the image path from the file 
        image = Image.open(image_path)
        # Putting image inside the tkinter
        photo = ImageTk.PhotoImage(image)
        
        # Label for the background photo
        background_label = tk.Label(window, image=photo)
        background_label.image = photo  
        # Creating the size of the bg photo
        background_label.place(relwidth=1, relheight=1.2)
        
        # Image path for the "Looking for cocktail?"
        image_path = "/Users/iashlaynemedina/Desktop/New Folder With Items 2/SY 2023-2024/CC SEM 2 2024 Files/Programming API/Images/entry_1.png"
         # To open the image path from the file 
        image = Image.open(image_path)
        # Putting image inside the tkinter
        photo = ImageTk.PhotoImage(image)
        
        # Label for the photo inside the window, bg property black
        self.image_label = tk.Label(self.window, image=photo, bg="black")
        self.image_label.image = photo
        # Size properties of the "Looking for cocktail?" image
        self.image_label.place(x=600, y=40)
        
        # Created an empty dictionary "id_drinks {}"
        self.id_drinks = {}
        
        # Created a variable for the api link from the given api's
        self.smart_searchbar_api = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s='
        
        # GUI App tkinter method make_widgets
        self.make_widgets()
    
    
    # Defined a method make_widgets
    def make_widgets(self):
        
        # Defined a variable for the search bar "Entry" for user able to search the cocktail drink and text, color, bg properties
        self.search_entry = tk.Entry(self.window, width=15, font="Arial 30", border=3, bg="white", fg="black")
        # Using variable place for the placing of the search bar using anchor x and y
        self.search_entry.place(x=40, y=40, anchor=tk.NW)
        # Using method insert for the search cocktail text inside the search bar
        self.search_entry.insert(0, "Search cocktail...")
        # Using method bind to connect it to the searchbar 
        self.search_entry.bind('<FocusIn>', self.user_search_in)
        self.search_entry.bind('<FocusOut>', self.user_search_out)
        
        # Define variable "suggestion_cocktail_list" for the list of cocktail drinks using the Class Listbox to show the list of drinks
        self.suggestion_cocktail_list = tk.Listbox(self.window)
        # Suggestion available cocktail list
        self.suggestion_cocktail_list.place()
        # Using method place_forget() when the search query is unactive or empty it will hide
        self.suggestion_cocktail_list.place_forget()
        # When the key is released after pressing it will bind when show_suggestions method will be called
        self.search_entry.bind('<KeyRelease>', self.show_suggestions)
    
    # Defined a method when mouse enters the search entry bar 
    def user_search_in(self, event):
        if self.search_entry.get() == "Search cocktail...":
            self.search_entry.delete(0, tk.END)  # Delete default text
            self.search_entry.config(fg="black")  # Change text color
            
    # Defined a method when mouse exits the search entry bar 
    def user_search_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search cocktail...")  
            self.search_entry.config(fg="grey")  
        
        # Defined variable for the label of the Drink Name text, design, color, size and placing properties
        self.drink_name_label = tk.Label(self.window, text="", relief='raised', font="Chalkboard 20", bg="black", fg="white")
        self.drink_name_label.place(x=700, y=200, anchor=tk.CENTER, width=400, height=45)
        
        # Defined variable for the label of the Category of Drink text, design, color, size and placing properties
        self.category_name_label = tk.Label(self.window, text="", relief='raised',font="Chalkboard 15", bg="black", fg="white")
        self.category_name_label.place(x=400, y=300, anchor=tk.CENTER, width=230, height=40)
        
        # Defined variable for the label of the Alcoholic name text, design, color, size and placing properties
        self.alcoholic_name_label = tk.Label(self.window, text="", relief='raised', font="Chalkboard 15", bg="black", fg="white")
        self.alcoholic_name_label.place(x=1000, y=301, anchor=tk.CENTER, width=230, height=40)
        
        # Defined variable for the label of the Image design, color, size and placing properties
        self.drink_image_label = tk.Label(self.window, relief="solid", bd=5)
        self.drink_image_label.place(x=700, y=450, anchor=tk.CENTER, width=350, height=350)
        
        # Defined variable for the label of the Ingredient drink text, design, color, size and placing properties
        self.ingredients_text = tk.StringVar()
        self.ingredients_name_label = tk.Label(self.window, textvariable=self.ingredients_text, text="", relief='raised', font="Chalkboard 13", bg="black", fg="white")
        self.ingredients_name_label.place(x=700, y=670, anchor=tk.CENTER, width=900, height=50)
    
    # Define a method to get the details of the drink id from api link
    def get_details(self, drink_id):
        response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}')
        data = response.json()
        return data['drinks'][0] if 'drinks' in data else None
    
    # Define a method to show the suggestions from the api
    def show_suggestions(self, event):
        search_query = self.search_entry.get().lower()
        
        #if search_query from the api smart search bar
        if search_query:
            response = requests.get(f'{self.smart_searchbar_api}{search_query}')
            
             #if the response and request is successful
            if response.status_code == 200:
                # it will store in data
                data = response.json()
                
                # Clears the existing items in cocktail list
                self.suggestion_cocktail_list.delete(0, tk.END)
                
                # Iterating the data "drinks" received from JSON data
                for drink in data['drinks']:
                    
                    # Created a variable string drink_details drink name and id in listbox
                    drink_details = f"{drink['strDrink']} - {drink['idDrink']}"
                    # Inserted the string at the end as an item of suggestion_cocktail_list
                    self.suggestion_cocktail_list.insert(tk.END, drink_details)
                    # drink id will be associated in id_drinks {dictionary}
                    self.id_drinks[drink['idDrink']] = drink
                
                # placing the listbox below the smart search bar
                self.suggestion_cocktail_list.place(x=self.search_entry.winfo_x(), y=self.search_entry.winfo_y() + self.search_entry.winfo_height())
                # binds/connects the event <ButtonRelease-1> to show_details
                self.suggestion_cocktail_list.bind('<ButtonRelease-1>', self.show_details)
                
            # if the response status code = 200, means failed, printing request failed
            else:
                print(f'Request Failed {response.status_code}')
        # if the search queries none it will the suggestion list
        else:
            self.suggestion_cocktail_list.place_forget()
            
    # Retrieve the index on selected drink from suggestion list
    def show_details(self, event):
        selection = self.suggestion_cocktail_list.curselection()
        # if there's selection
        if selection:
            # retrieve details of user selected drink using ID
            user_selected_id = self.suggestion_cocktail_list.get(selection).split("-")[-1].strip()
            # extract the drink ID from the user selected drink
            drink_info = self.id_drinks.get(user_selected_id)
            
            # To check if the drink info is available
            if drink_info:
                # To update the drink name label of the selected drink
                self.drink_name_label.config(text=f"Name: {drink_info['strDrink']}")
                # To update the category name label of the selected drink
                self.category_name_label.config(text=f"Category: {drink_info['strCategory']}")
                # To update the alcoholic name label of the selected drink
                self.alcoholic_name_label.config(text=f"Alcoholic: {drink_info['strAlcoholic']}")
                
                # Retrive the image link/url 
                image_link = drink_info['strDrinkThumb']
                # request to get the image 
                response = requests.get(image_link)
                 #if the response and request is successful
                if response.status_code == 200:
                    # The image will open
                    drink_image = Image.open(BytesIO(response.content))
                    # resize the image
                    drink_image = drink_image.resize((400, 400), Image.LANCZOS)
                    # convert the image to Tkinter format
                    drink_image = ImageTk.PhotoImage(drink_image)
                    # To update the label of the drink image
                    self.drink_image_label.config(image=drink_image)
                    # To update the reference image in label
                    self.drink_image_label.image = drink_image
                    
                    # Content for Ingredients
                    ingredients_text_content = "Ingredients: "
                    # Iterate the ingredients and measure available
                    for c in range(1, 16):
                        # Get drink ingredients
                        ingredients = drink_info.get(f'strIngredient{c}')
                        # Get drink measures
                        measures = drink_info.get(f'strMeasure{c}')
                      
                        # If ingredients and measures available
                        if ingredients and measures:
                            # Append the measure and ingredients
                            ingredients_text_content += f"{measures} + {ingredients}"
                    # To update the ingredients label
                    self.ingredients_text.set(ingredients_text_content)
                    # To hide suggestion cocktail list
                    self.suggestion_cocktail_list.place_forget()
                # Prints an error if getting image for the drink info
                else:
                    print(f'Error getting image for {drink_info["strDrink"]}')
            # Print message drink is not available
            else:
                print(f'Cocktail Drink not found for {user_selected_id}')
                
# To run the TKINTER mainloop
if __name__ == "__main__":
    root = tk.Tk()
    app = CocktailGUIApp(root)
    root.mainloop()

