# Importing libraries
# GUI libraries
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askyesno
#from tkinter import messagebox
from tkinter import filedialog as file_path

# Generates QR codes
import qrcode
# Read QR codes
import cv2

import pyperclip

# GUI
root = Tk()
root.title('QR Code Generator & Reader App') #Prototype name
root.iconbitmap(root, 'icon.ico')
root.geometry('500x480')
root.resizable(height = False, width = False) #App non resizable

# Widgets Styles
# Labels
label_style = ttk.Style()
label_style.configure('TLabel', foreground = '#000000', font = ('Roboto Black', 11))

# Entries
entry_style = ttk.Style()
entry_style.configure('TEntry', font = ('Roboto Bold', 15))

# Butttons
button_style = ttk.Style()
button_style.configure('TButtton', foreground = '#000000', font = ('Roboto Black', 10))

# Tabs
tab_control = ttk.Notebook(root)
generator_tab = ttk.Frame(tab_control)
reader_tab = ttk.Frame(tab_control)

tab_control.add(generator_tab, text = 'QR Code Generator')
tab_control.add(reader_tab, text = 'QR Code Reader')

tab_control.pack(expand = 1, fill = 'both')

# Addin canvas to the tabs
generator_canvas = Canvas(generator_tab, width = 500, height = 400)
generator_canvas.pack()

reader_canvas = Canvas(reader_tab, width = 500, height = 400)
reader_canvas.pack()

# Displays the QRCode Image
# Generator tab
image_label = Label(root)
generator_canvas.create_window(250, 150, window = image_label)

# Entry data
qrdata_label = ttk.Label(root, text = 'QR Code Data', style = 'TLabel')
data_entry = ttk.Entry(root, width = 55, style = 'TEntry')

# Receiving Entry Data
generator_canvas.create_window(70, 330, window = qrdata_label)
generator_canvas.create_window(300, 330, window = data_entry)

filename_label = ttk.Label(root, text = 'Filename', style = 'TLabel')
filename_entry = ttk.Entry(width = 55, style = 'TEntry')

generator_canvas.create_window(84, 360, window = filename_label)
generator_canvas.create_window(300, 360, window = filename_entry)

# Making the buttons
# Reset button
reset_button = ttk.Button(root, text = 'Reset', style = 'TButton', state = DISABLED)


# Reader tab
image_label2 = Label(root)
data_label = ttk.Label(root)
reader_canvas.create_window(250, 150, window = image_label2)
reader_canvas.create_window(250, 300, window = data_label)





# Close app window
def close_app():
    if askyesno(title = 'Close QR Code Generator & Reader App', message = 'Are you sure you want to close the application?'):
        root.destroy()

def generate_qrcode():
    qrcode_data = str(data_entry.get())
    qrcode_name = str(filename_entry.get())

# Check if filename_entry is empty
    if qrcode_name == '':
        showerror(title ='Error', message ='An error ocurred' \
                    '\nThe following is ' \
                    'the cause: \n -> Empty entry field\n' \
                    'Make sure the filename entry field is filled when generating the QRCode')
        
    else:
        if askyesno(title = 'Confirmation', message = f'Do you want to create a QRCode with the provided information?'):
            try:
                qr = qrcode.QRCode(version = 1, box_size = 6, border = 4)
                qr.add_data(qrcode_data)

                # Handle the qr image size
                qr.make(fit = True)

                # Add the name and format to the image
                name = qrcode_name + '.png'
                
                # Make the QR Code and add it color
                qrcode_image = qr.make_image(fill_color = 'black', back_color = 'white')

                qrcode_image.save(name)
                
                global Image

                Image = PhotoImage(file = f'{name}')
                image_label.config(image = Image)
                # Enable the reset button
                reset_button.config(state = NORMAL, command = reset)
            except:
                showerror(title = 'Error', message = 'Please provide a valid filename')

def reset():
    if askyesno(title = 'Reset', message = 'Are you sure you want to reset?'):
        
        # Reset the image label
        image_label.config(image = '')
        
        # Disable the reset button
        reset_button.config(state = DISABLED)
# QR Code Generator Button
generate_button = ttk.Button(root, text = 'Generate QR Code', style = 'TButton', command = generate_qrcode)
generator_canvas.create_window(300, 390, window = reset_button)
generator_canvas.create_window(410, 390, window = generate_button)


def open_dialog():
    name = file_path.askopenfilename()
    file_entry.delete(0, END)
    file_entry.insert(0, name)

# File entry
file_entry = ttk.Entry(root, width = 60, style = 'TEntry')
# Browse files button
browse_button = ttk.Button(root, text = 'Browse', style = 'TButton', command = open_dialog)

reader_canvas.create_window(200, 350, window = file_entry)
reader_canvas.create_window(430, 350, window = browse_button)

def read_qrcode():
    image_file = file_entry.get()

    if image_file == '':
        showerror(title = 'Error', message = 'Please provide a QR Code')

    else:
        try:
            # Use the cv2 library to read the qrcode
            qr_image = cv2.imread(f'{image_file}')
            qr_reader = cv2.QRCodeDetector()

            global qrcode_image

            qrcode_image = PhotoImage(file = f'{image_file}')
            image_label2.config(image = qrcode_image)
            
            # Detect and decode the following information
            data, pts, st_code = qr_reader.detectAndDecode(qr_image)
            data_label.config(text = data)

        except:
            showerror(title = 'Error', message = 'An error occurred while detecting data from the provided file' \
                '\nThe following could be ' \
                'the cause:\n->Wrong image file\n' \
                'Make sure the image file is a valid QRCode')

# Detect button
detect_button = ttk.Button(root, text = 'Read QR Code', style = 'TButton', command = read_qrcode)
reader_canvas.create_window(65, 385, window = detect_button)

# Clipboard button
def copy_to_clipboard():
    data_to_copy = data_label.cget('text')
    pyperclip.copy(data_to_copy)

copy_button = ttk.Button(root, text = 'Copy to Clipboard', style = 'TButton', command = copy_to_clipboard)
reader_canvas.create_window(170, 385, window = copy_button)

root.protocol('WM_DELETE_WINDOW', close_app)
root.mainloop()
