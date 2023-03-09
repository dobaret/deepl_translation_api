# This script allows you to select one or more subtitle files and translate them into a target language. It uses the DeepL API to perform the translation.

# Modules
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox
import deepl
import os
import sys

# Call the deepl_key environment variable
auth_key = os.environ["deepl_key"]

# Initialize DeepL
translator = deepl.Translator(auth_key)

# Create the file dialog window
root = tk.Tk()

# Allow the user to simply exit the program
def on_closing():
    sys.exit()
root.protocol("WM_DELETE_WINDOW", on_closing)

# Open a file dialog and ask the user to select one or more subtitle files
input_path = fd.askopenfilenames(title='Sélectionnez un fichier', filetypes=[("Formats autorisés","*.docx; .pptx; .pdf; .html; .htm; .txt; .xlf; .xliff")])

# Open a file dialog and ask the user to select one or more subtitle files
if not input_path:
    tkinter.messagebox.showerror("Erreur","Vous n'avez pas sélectionné de fichier, veuillez en sélectionner un pour continuer.")
    sys.exit()

# Create a label to explain what to do
label = tk.Label(root, text="Veuillez sélectionner une langue cible :")
label.pack(padx=10, pady=10)

# Create a dropdown menu for the target language
var = tk.StringVar(root)
var.set("") # default value

# All languages supported by the DeepL API
language_options = ["BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "LT", "LV", "NL", "PL", "PT-BR", "PT-PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH"]

# Put the previous languages in a dropdown menu
dropdown = tk.OptionMenu(root, var, *language_options)
dropdown.pack()

# Asks the user to confirm their selection
tk.Button(root, text="OK", command=root.destroy).pack(padx=10, pady=10)
root.mainloop()

# Get the selected language code
target_lang = var.get()

# check if target language is selected 
if not target_lang:
    tkinter.messagebox.showerror("Erreur","Vous n'avez pas sélectionné de langue cible, veuillez en sélectionner une pour continuer.")
    sys.exit()

# Set the output path for the translated files
output_path = os.path.join(os.path.dirname(input_path[0]), target_lang)

# Create the output folder if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Iterate through the selected files
for file in input_path:

    # Get the file name
    file_name = os.path.basename(file)
    print(f"Traduction en cours : {file_name}")

    # Set the output file path
    output_file = os.path.join(output_path, file_name)
    
    try:
        
        # Translate the file and save it to the output path
        translator.translate_document_from_filepath(
            file,
            output_file,
            target_lang=target_lang
        )

    except deepl.DocumentTranslationException as error:
        # If an error occurs during document translation after the document was
        # already uploaded, a DocumentTranslationException is raised. The
        # document_handle property contains the document handle that may be used to
        # later retrieve the document from the server, or contact DeepL support.
        doc_id = error.document_handle.id
        doc_key = error.document_handle.key
        print(f"Error after uploading ${error}, id: ${doc_id} key: ${doc_key}")
    except deepl.DeepLException as error:

        # Errors during upload raise a DeepLException
        print(error)
        
    print("Traduction terminée.")
    