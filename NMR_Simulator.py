import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
import math as mt
#Main definitions of the window
window = tk.Tk()
window.title("Multiplet Generator")
window.state("zoomed")
#labels_and_entries is a list that is used to generate the labels and entry boxes on the window
labels_and_entries = ["j1label","j1entry","m1label","m1entry","j2label","j2entry","m2label","m2entry","j3label","j3entry","m3label","m3entry"]
#make_graphs checks if the stick and realistic multiplet graphs should be shown on screen
make_graphs = 0
#make_spectrum_graph checks if the spectrum should be shown on screen
make_spectrum_graph = 0
#These two spectrum lists are for making the full spectrum (multiple multiplets) graph
spectrum_x_values = []
spectrum_y_values = []
#These two temp lists are for keeping the input couplings etc between destroying / making the window
temp_J = []
temp_multiplicities = []
#stop_code is to stop a function from proceeding if an error is found, this stops tkinter showing errors and 
#incorrect calcuations from happening.
stop_code = 0
#W_half is the width at half height of each peak in Hz
W_half = 0.5
#This function makes the window
def make_window():
    global second_frame
    #This gets all widgets (labels, entry boxes, buttons etc) packed with .grid in the window "window" and 
    #puts them in a list
    grid_widgets = window.grid_slaves()
    #Same as above but for widgets packed with .pack
    pack_widgets = window.pack_slaves()
    #This destroys all widgets on the window "window" to prevent overlapping of widgets, overlapping can cause readability
    #issues and performance issues.
    for a in grid_widgets:
        a.destroy()
    for a in pack_widgets:
        a.destroy()
    #Make and packthe first frame
    first_frame = tk.Frame(window)
    first_frame.pack(fill=tk.BOTH, expand=1)
    #Make and packthe canvas
    canvas = tk.Canvas(first_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    #Make and pack the scrollbar
    scrollbar = tk.Scrollbar(first_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    #Configure the canvas with the scrollbar command
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
    #Make a second frame to contain all the labels, entries, graphs and buttons
    second_frame = tk.Frame(canvas)
    #New window on canvas
    canvas.create_window((0,0), window=second_frame, anchor="nw")
    #You must create two frames and a canvas to allow for scrolling as shown above, the scroll bar scrolls the first 
    #frame which has the second frame, containing all the stuff I want to diplay, within it.
    #Make and pack w_half_label and w_half_entry
    w_half_label = tk.Label(second_frame, text="Width at half height / Hz:")
    w_half_label.grid(row =0, column=0)
    global w_half_entry
    w_half_entry = tk.Entry(second_frame)
    w_half_entry.grid(row=0, column=1)
    #.insert is to make sure the box starts off with something and doesn't go blank when re running make_window()
    w_half_entry.insert(-1, W_half)
    global temp_J,temp_multiplicities
    #This try and except block below makes sure the previously entered J values stay in the entry box after a graph 
    #has been generated. Without this the boxes would be empty when the graphs are generated but this is just the
    #list generation part.
    try:
        len_temp_J = len(temp_J)
        len_temp_J = int(len(labels_and_entries)/4) - len_temp_J 
        if len_temp_J != 0:
            for x in range(len_temp_J):
                temp_J.append("")
    except:
        temp_J = []
        for o in range(int(len(labels_and_entries)/4)):
            temp_J.append("")
    #This try and except block below makes sure the previously entered multipicities stay in the entry box 
    #after a graph has been generated. Without this the boxes would be empty when the graphs are generated
    #but this is just the list generation part.
    try:
        len_temp_multipicities = len(temp_multiplicities)
        len_temp_multipicities = int(len(labels_and_entries)/4) - len_temp_multipicities 
        if len_temp_multipicities != 0:
            for x in range(len_temp_multipicities):
                temp_multiplicities.append("")
    except:
        temp_multiplicities = []
        for o in range(int(len(labels_and_entries)/4)):
            temp_multiplicities.append("")
    #it is necessary to use this for loop to allow the user to add more entries if they require.    
    for o in range(int(len(labels_and_entries)/4)):
        '''In this loop, each input row has 4 widgets (2 labels and 2 entry boxes). These four have corresponding variables
        whose names are stored in the list labels_and_entries. You can't call a named variable from a list so the globals() 
        function is used to access the global symbol table to allow the strings containing the variable names to be
        used as the variable (the syntax is globals()[variable_name]. These variables are then assigned as either labels 
        or entry boxes and placed on the window by the .grid command from tkinter. 
        To add an undefined amount of input rows to the window, the program must be
        able to make new variables during runtime. Since the number of variables isn't known at startup, creating these
        input rows must be done based on how many there variables currently are therefore the for loop method is the solution
        to this problem. labels_and_entries[(4*o)] is to call the element with the name of the variable we want to use,
        in this case the name is at the index 4*o. On the first run when o=0, index 0 (4*o), 1 ((4*o)+1), 2 ((4*o)+2) and 3 
        ((4*o)+3) are accessed, the next run o increases to 1 and the indexes 4-7 can be accessed.'''
        globals()[labels_and_entries[(4*o)]] = tk.Label(second_frame,text ="J Value (2 d.p) / Hz: ")
        globals()[labels_and_entries[(4*o)]].grid(row = o+1, column = 0)
        globals()[labels_and_entries[(4*o)+1]] = tk.Entry(second_frame)
        globals()[labels_and_entries[(4*o)+1]].grid(row = o+1, column = 1)
        #This .insert line is the implementation of the list generated in the first try and except block above
        globals()[labels_and_entries[(4*o)+1]].insert(-1,temp_J[o])
        globals()[labels_and_entries[(4*o)+2]] = tk.Label(second_frame,text ="Number of H atoms with this coupling: ")
        globals()[labels_and_entries[(4*o)+2]].grid(row = o+1, column = 2)
        globals()[labels_and_entries[(4*o)+3]] = tk.Entry(second_frame)
        globals()[labels_and_entries[(4*o)+3]].grid(row = o+1, column = 3)
        #This .insert line is the implementation of the list generated in the second try and except block above
        globals()[labels_and_entries[(4*o)+3]].insert(-1,temp_multiplicities[o])
    
    #The finish button generates the graphs with the function click()
    finish = tk.Button(second_frame, text="Click to generate graphs",command=click)
    finish.grid(row=int(len(labels_and_entries)/4)+1, column=0)
    #The addentry button adds a new entry row with the function add_entry()
    addentry = tk.Button(second_frame, text="Add another entry row", command=add_entry)
    addentry.grid(row =int(len(labels_and_entries)/4)+1, column=3)
    global make_graphs, offset_entry, number_of_hydrogens_entry, add_to_spec
    #If the graphs have been made make_graphs = 1, this then puts all the graphs on screen and spectrum related buttons on.
    if make_graphs == 1:
        #From here to offset_label definition, is putting the realistic and stick spectra (with labels) on the screen via tkinter 
        #The next 12 lines are to display the stick and realistic graphs.
        stickimg = ImageTk.PhotoImage(file="stick.png")
        fullimg = ImageTk.PhotoImage(file ="full.png")
        stick_label = tk.Label(second_frame, text="NMR stick multiplet graph:")
        stick_label.grid(row=int(len(labels_and_entries)/4)+2, column=0)
        stick = tk.Label(second_frame, image=stickimg)
        stick.photo = stickimg
        stick.grid(row=int(len(labels_and_entries)/4)+2, column=1)
        full_label = tk.Label(second_frame, text="NMR realistic multiplet graph:")
        full_label.grid(row=int(len(labels_and_entries)/4)+3, column=0)
        full = tk.Label(second_frame, image=fullimg)
        full.photo = fullimg
        full.grid(row=int(len(labels_and_entries)/4)+3, column=1)
        #offset is the ppm at which the multiplet being added to the spectrum is centred
        offset_label = tk.Label(second_frame, text = "Multiplet position (2 d.p) / ppm: ")
        offset_label.grid(row =int(len(labels_and_entries)/4)+3, column=2)
        offset_entry = tk.Entry(second_frame)
        offset_entry.grid(row =int(len(labels_and_entries)/4)+3, column=3)
        #number_of_hydrogens is how many hydrogens the multiplet in question corresponds to
        number_of_hydrogens_label = tk.Label(second_frame, text = "Number of hydrogens in this environment: ")
        number_of_hydrogens_label.grid(row =int(len(labels_and_entries)/4)+2, column=2)
        number_of_hydrogens_entry = tk.Entry(second_frame)
        number_of_hydrogens_entry.grid(row =int(len(labels_and_entries)/4)+2, column=3)
        #add_to_spec is a button that runs the add_to_spectrum command (adding the multiplet to a spectrum list) when clicked
        add_to_spec = tk.Button(second_frame, text="Add multiplet to spectrum",command=add_to_spectrum)
        add_to_spec.grid(row=int(len(labels_and_entries)/4)+4, column=0)
        #if spectrum_x_values is empty, no multiplets have been added to the spectrum, otherwise give the user the ability
        #to show the spectrum (show_spectrum button)
        if spectrum_x_values == []:
            pass
        else:
            #show_spectrum is a button that displays the entire spectrum so far when clicked
            show_spectrum = tk.Button(second_frame, text="Show spectrum", command=make_spectrum)
            show_spectrum.grid(row=int(len(labels_and_entries)/4)+4, column=1)
        #make_graphs = 0 is to free up screen real estate when the graphs are not explicitly asked for by the user.
        make_graphs = 0
    global make_spectrum_graph
    #If the show_spectrum button has been pressed, make_spectrum_graph = 1, this if statement checks for that and shows the 
    #spectrum if make_spectrum_graph = 1.
    if make_spectrum_graph == 1:
        spectrumimg = ImageTk.PhotoImage(file="spectrum.png")
        spectrum_label = tk.Label(second_frame, text="NMR Spectrum:")
        spectrum_label.grid(row=int(len(labels_and_entries)/4)+5, column=0)
        spectrum = tk.Label(second_frame, image=spectrumimg)
        spectrum.photo = spectrumimg
        spectrum.grid(row=int(len(labels_and_entries)/4)+5, column=1)
        #make_spectrum_graph = 0 is to free up screen real estate when the spectrum is not explicitly asked for by the user.
        make_spectrum_graph = 0
    #This mainloop makes the window
    window.mainloop()

def main_code():
    global x_values_curve, y_values_curve
    #The first peak representing the hydrogen (corresponding the to multiplet) set at 0 (x_values = [0])
    x_values = [0]
    #This for loop goes through the peaks in x_values list and creates a new list containing double the peaks 
    #(one at + J/2 and one at -J/2 from each element in x_values), it does this for each J coupling in J_values
    #J_values is the list of J couplings given with the multiplicites built in e.g two hydrogens with J = 7
    #will result in J_values containing 3 7s ([7,7,7])
    for a in J_values:
        half = a/2
        list_2 = []
        for b in x_values:
            list_2.append(b-half)
            list_2.append(b+half)
            x_values = list_2
    new_x =[]
    y =[]
    #count starts at 1 and is used for calculating peak intensities below
    count = 1
    #You must sort here to get all the same x values next to eachother in the list, allowing for simple addition in the 
    #form of the count below
    x_values = sorted(x_values)
    #This for loop counts all the J values of the same type to get the respective peak heights in the list y,
    #it also gives a list containing one of x value (e.g only one 7 is contained in this list) in the list new_x
    for a in range(len(x_values)):
        #You need this if statement first to stop the program looking for a value out of the range i.e x_values[a+1] where 
        #a is the last index in x_values. You use len(x_values)-1 since the last index is one less than the range.
        if a == (len(x_values)-1):
            #The last peak always has a relative height of 1 (the smallest)
            y.append(1)
            new_x.append(x_values[a])
        #The two elif statements below, count how many times a specific x value appers in the list, then adds x value to 
        #the list new_x and adds the count (the peak height) to the y list
        elif x_values[a] == x_values[a+1]:
            count = count+1
        elif count != 1:
            y.append(count)
            new_x.append(x_values[a])
            count = 1
        #When the x value in question only appears once in the list, it is added to the new_x list and its height is recoreded as 1
        #in the y list
        else:
            y.append(1)
            new_x.append(x_values[a])
    #These empty lists will be filled with values corresponding to the accurate NMR multiplet graph
    x_values_curve = []
    y_values_curve = []
    #If new_x = [0], it means there is no other hydrogens to be coupled with, meaning the user requested a singlet. 
    #In which case J_values is an empty list so Pre_J should be used instead.
    if new_x == [0]:
        #Here mt.ceil is to find the closest whole number larger (smaller for negative) than the variable in question, 
        #since it calculates ceiling, for negative numbers -mt.ceil(-variable) is required.
        #As W_half increases, the further out you will need to go to start getting negligible y values, 
        #+(max(J_values)*2*W_half is a qualitative solution to this problem.
        #start and end are the starting and ending positions for the x_values_curve list
        start = -mt.ceil(-new_x[0]+(float(Pre_J[0])*2*W_half))
        end = mt.ceil(new_x[-1]+(float(Pre_J[0])*2*W_half))
    else:
        start = -mt.ceil(-new_x[0]+(max(J_values)*2*W_half))
        end = mt.ceil(new_x[-1]+(max(J_values)*2*W_half))
    #This while loop creates a list of x values, each separated by 0.01 and each a multiple of 0.01 due to the 
    #fact that it starts at an integer, this is essential for making the spectrum
    #because if the x values aren't uniform, summing y values of like x values would be difficult.
    while True:
        if start > end:
            break
        else:
            #This is creating the x_values_curve list
            x_values_curve.append(start)
            #This is creating a corresponding y_curve list with only zeros which is added to later
            y_values_curve.append(0)
            start = round(start + 0.01,2)
    #for y_index in range(len(y)) means the loop goes through each element of the list y (the list containing all the line 
    #peaks). This method of using the index is because we also need the corresponding peak x value (new_x[y_index]) 
    #since the Lorentzian line equation depends on how far the current x value is from the peak x value.
    for y_index in range(len(y)):
        #temp_y is the list containing all the y values for each x_values_curve element for one peak at a time
        temp_y = []
        for x in x_values_curve:
            #Lorentzian line equation
            temp_y.append((y[y_index]*(W_half**2))/((W_half**2) + (4*((new_x[y_index]-x)**2))))
        #This adds the elements for the two lists together then the for loop starts again with the next y_index element
        y_values_curve = [sum(g) for g in zip(temp_y,y_values_curve)]

    #This is the realistic curve plot
    plt.plot(x_values_curve,y_values_curve)
    plt.xlabel("Hz")
    plt.savefig("full.png")
    #This is the start of the stick figure plot.
    plt.figure(2)
    #This for loop is to plot each point as a line from 0 to its true height (both points with the same x value),
    #this is necessary to stop the plotted points from joining up and making the graph a mess.
    for a in range(len(new_x)):
        plt.plot([new_x[a],new_x[a]],[0,y[a]])
    plt.xlabel("Hz")
    plt.savefig("stick.png")
    plt.close('all')

#This function corresponds to the button that generates the stick and realistic graphs
def click():
    #temp_J and temp_multiplicities must be made global to allow for their current values to remain in the entry boxes 
    #when make_window runs, otherwise every time graphs are made or a new entry
    #row is added, all the entry boxes would be wiped giving a bad user experience
    global temp_J,temp_multiplicities,Pre_J
    temp_multiplicities = []
    multiplicities = []
    temp_J = []
    Pre_J = []
    Errors = []
    #This for loop is getting all the current entry box values.
    for o in range(int(len(labels_and_entries)/4)):
        temp_J.append(globals()[labels_and_entries[(4*o)+1]].get())
        temp_multiplicities.append(globals()[labels_and_entries[(4*o)+3]].get())
    #stop_code must be global to allow stopping the code before this variable is defined in this function.
    #This allows removal of the error labels below, if these labeles are not removed, subesquent presses of the button
    #that have errors in will make the error box unreadable due to overlapping error messages.
    global stop_code
    #These two below must be global to allow destuction of them before they are defined in this function. They must be 
    #destroyed before they are defined otherwise you get the overlapping of errors mentioned above. If they are destroyed
    #after they are defined, the error messages dissapear without user input or with specific user input to remove them.
    #Both of those implementations are worse than the current one.
    global Errors_label
    global Errors_list
    #If stop_code = 1 here, that means there was an error and now the click function is being run again, the error 
    #labels are destroyed because if there is another error, the code won't reach make_window, this means
    #the error labels will start overlapping and become unreadable
    if stop_code == 1:
        Errors_label.destroy()
        Errors_list.destroy()
        stop_code = 0
    #This for loop gets rid of all the empty values for which J and multiplicity aren't defined, it also checks for 
    #pairs or J and multiplicity, if there are values without a partner then it asks the user to correct this.
    for a in range(len(temp_multiplicities)):
        if temp_multiplicities[a] == "" and temp_J[a] == "":
            pass
        elif temp_multiplicities[a] == "" or temp_J[a] =="":
            Errors.append("Please make sure all J values have a correponding number of H atoms with this coupling and vice versa")
            stop_code = 1
        else:
            Pre_J.append(temp_J[a])
            multiplicities.append(temp_multiplicities[a])
    #J_values set to global so it can be used outside of this function in the main_code() function
    global J_values
    J_values = []
    #same with W_half as J_values above
    global W_half
    #Error trapping on W_half
    try:
        W_half = float(w_half_entry.get())
        if W_half<0:
            raise ValueError
    except ValueError:
        stop_code = 1
        Errors.append(str(w_half_entry.get())+" is an invalid input, please input a positive number")
    #Error trapping on Multiplicities and J values
    for a in range(len(multiplicities)):
        try:
            n2 = float(Pre_J[a])
            if n2<0:
                raise ValueError
        except ValueError:
            stop_code = 1
            Errors.append(str(Pre_J[a])+" is an invalid input, please input a positive number")
        try:
            n = int(multiplicities[a]) 
            if n<0:
                #Cannot have negative number of H atoms with this coupling
                raise ValueError
            if n>=20:
                #If too large it can take a long time or fail due to lack of memory
                raise ValueError
        except ValueError:
            stop_code = 1
            Errors.append(str(multiplicities[a])+" is an invalid input, please input a positive integer below 20")
    #This stops the main code from running if there is an error and then creates labels to tell the user what they did wrong
    if stop_code == 1:
        Errors_label = tk.Label(second_frame, text="Errors:")
        Errors_label.grid(row=int(len(labels_and_entries)/4)+1, column=1)
        Errors_list = tk.Label(second_frame, text=Errors)
        Errors_list.grid(row=int(len(labels_and_entries)/4)+1, column=2)
        return
    #This for loop provides a list of J values with the multiplicities built in e.g. a J value of 7 with 2 corresponding 
    #hydrogens becomes [...,7,7,7...] where ... represents the other values in the list
    for a in range(len(multiplicities)):
        for x in range(int(multiplicities[a])):
            J_values.append(float(Pre_J[a]))
    #We now have the inputs in the right format, next we execute main_code()
    main_code()
    #make_graphs needs to be global to allow it to be accessed and changed in the make_window function
    global make_graphs
    #This means graphs have been generated so they will be displayed in the make_window function
    make_graphs = 1
    make_window()

def add_entry():
    #This adds 4 entries to the labels_and_entries list, these make the labels and entries on the window in the make_window 
    #function see the make_window fuction for more details
    labels_and_entries.append("j"+str(int(len(labels_and_entries)/4)+1)+"label")
    labels_and_entries.append("j"+str(int(len(labels_and_entries)/4)+1)+"entry")
    labels_and_entries.append("m"+str(int(len(labels_and_entries)/4)+1)+"label")
    labels_and_entries.append("m"+str(int(len(labels_and_entries)/4)+1)+"entry")
    make_window()

#This function adds the current x_values_curve and y_values_curve to the spectrum_x_values and spectrum_y_values
def add_to_spectrum():
    global x_values_curve, y_values_curve, spectrum_x_values, spectrum_y_values, stop_code, Errors_label, Errors_list
    variable_x = 0
    errors_spec = []
    #If stop_code = 1 here, that means there was an error and now the code is being run again, the error 
    #labels are destroyed because if there is another error, the code won't reach make_window, this means
    #the error labels will start overlapping and become unreadable
    if stop_code == 1:
        Errors_label.destroy()
        Errors_list.destroy()
        stop_code = 0
    #This checks if the required inputs have been given
    if offset_entry.get == "" and number_of_hydrogens_entry.get() == "":
        stop_code = 2
    elif offset_entry.get() == "" or number_of_hydrogens_entry.get() =="":
        stop_code = 2
    #If stop_code = 2, at least one of the inputs is missing, if this isn't the case the code proceeds to error checking
    #the inputs given
    if stop_code == 2:
        errors_spec.append("Please input numbers for both offset and number of hydrogens")
        stop_code = 1
    else:
        #Error trapping number_of_hydrogens and offset
        try:
            number_of_hydrogens = int(number_of_hydrogens_entry.get())
            if number_of_hydrogens < 0:
                raise ValueError
        except ValueError:
            stop_code = 1
            errors_spec.append(str(number_of_hydrogens_entry.get())+" is an invalid input, please input a positive integer")
        try:
            offset = (300*round(float(offset_entry.get()),2))
            #offset is the peak shift set by user (2 d.p) in Hz (this calculation is for a 300MHz machine)
        except ValueError:
            errors_spec.append(str(offset_entry.get())+" is an invalid input, please input a number")
            stop_code = 1
    #If stop_code = 1, an error has occured and the function must be stopped along with error labels being created to 
    #inform the user what they did wrong
    if stop_code == 1:
        Errors_label = tk.Label(second_frame, text="Errors:")
        Errors_label.grid(row=int(len(labels_and_entries)/4)+1, column = 1)
        Errors_list = tk.Label(second_frame, text=errors_spec)
        Errors_list.grid(row=int(len(labels_and_entries)/4)+1, column = 2)
        #return exits the function, stopping the rest from running
        return
    converted_y_values = []
    #This for loop converts the y values to make the multiplet proportional to the number of hydrogens it represents
    #sum(y_value_curve) aproximately equals the area under the curve
    for a in y_values_curve:
        converted_y_values.append(number_of_hydrogens*(a/sum(y_values_curve)))
    y_values_curve = converted_y_values
    position = 0
    #position keeps track of the starting index
    after_before = 2
    #after_before keeps track of if the first x value of the multiplet being added is before (0), after (1) or within  
    #the existing values (2).
    #If the spectrum lists are empty, the spectrum_x_values list is filled with x_values_curve + offset and 
    #the spectrum_y_values = y_values_curve
    if spectrum_x_values == []:
        for a in x_values_curve:
            spectrum_x_values.append(round((a+offset),2))
        spectrum_y_values = y_values_curve
    #If the spectrum lists aren't empty, you must find out where the multiplet being added is relative to the values in 
    #spectrum_x_values
    else:
        if spectrum_x_values[0] > (x_values_curve[0] + offset):
            #checks if starting value of the added multiplet is smaller than the first value of the existing spectrum list.
            after_before = 0
        elif spectrum_x_values[-1] < (x_values_curve[0] + offset):
            #checks if starting value of the added multiplet is larger than the last value of the existing spectrum list.
            after_before = 1
        #after_before is default 2 so if it wasn't changed in the above if or elif, then the added multiplet starts within
        #the current spectrum_x_values.
        if after_before == 2:
            #This for loop finds the index in spectrum_x_values corresponding to the first x_values_curve element
            for a in spectrum_x_values:
                if a == (x_values_curve[0] + offset):
                    break
                else:
                    position = position + 1
            #This while loop extends the spectrum_x_values list (and the spectrum_y_values list) until the whole range of 
            #the new multiplet is added, or if the range is already included it does nothing.
            while True:
                if round((spectrum_x_values[-1]+0.01),2) > (x_values_curve[-1] + offset):
                    break
                else:
                    spectrum_x_values.append(round((spectrum_x_values[-1]+0.01),2))
                    spectrum_y_values.append(0)
            #This for loop adds the y_value_curve values to the spectrum_y_values values    
            for a in y_values_curve:
                spectrum_y_values[position] = round((spectrum_y_values[position] + a),2)
                position = position + 1
        #elif the added multiplet starts after spectrum_x_values
        elif after_before == 1:
            variable_x = spectrum_x_values[-1]
            #This while loop adds to spectrum_x_values and spectrum_y_values until all multiplet x values are included.
            while True:
                variable_x = round(variable_x + 0.01,2)
                #must be rounded to 2 d.p even though 0.01 and variable_x should be 2 d.p, this is because computers  
                #don't store numbers as fixed point decimals unless told to.
                spectrum_x_values.append(variable_x)
                spectrum_y_values.append(0)
                if variable_x == (x_values_curve[0] + offset):
                    position = len(spectrum_x_values) - 1
                if variable_x == (x_values_curve[-1] + offset):
                    break
            #This for loop adds the y_value_curve values to the spectrum_y_values values.
            for a in y_values_curve:
                spectrum_y_values[position] = spectrum_y_values[position] + a
                position = position + 1
        #elif the added multiplet starts before spectrum_x_values.
        elif after_before == 0:
            pre_x_values = []
            #make list pre_x_values containing the converted values of x_values_curve with this for loop.
            for a in x_values_curve:
                pre_x_values.append(round((a + offset),2))
            #make x_values_curve the converted list.
            x_values_curve = pre_x_values
            #This while loop adds to x_values_curve and y_values_curve until all the spectrum_x_values are included.
            while True:
                if round((x_values_curve[-1]+0.01),2) > spectrum_x_values[-1]:
                    break
                else:
                    x_values_curve.append(round((x_values_curve[-1]+0.01),2))
                    y_values_curve.append(0)
            #This for loop finds the index corresponding to the first x_values_curve element.
            for a in x_values_curve:
                if a == (spectrum_x_values[0]):
                    break
                else:
                    position = position + 1
            #This for loop adds the spectrum_y_values values to the y_values_curve values.
            for a in spectrum_y_values:
                y_values_curve[position] = y_values_curve[position] + a
                position = position + 1
            spectrum_x_values = x_values_curve
            spectrum_y_values = y_values_curve
    #The add_to_spec button is destroyed so the user cannot accidentally add the same multiplet multiple times.
    add_to_spec.destroy()
    #This adds the show_spectrum button.
    show_spectrum = tk.Button(second_frame, text="Show spectrum", command=make_spectrum)
    show_spectrum.grid(row=int(len(labels_and_entries)/4)+4, column=1)
#This function plots the spectrum from spectrum_x_values and spectrum_y_values.
def make_spectrum():
    global make_spectrum_graph
    make_spectrum_graph = 1
    converted_to_ppm = []
    #this for loop converts the spectrum_x_values in Hz to ppm based on a 300MHz machine.
    for a in spectrum_x_values:
        converted_to_ppm.append(a/300)
    #plt.xlim(max(converted_to_ppm), min(converted_to_ppm)) plots the max and min x values in reverse, 
    #allowing the graph to go from left to right for highest to lowest x values.
    plt.xlim(max(converted_to_ppm), min(converted_to_ppm))
    plt.plot(converted_to_ppm,spectrum_y_values)
    #plt.yticks([]) removes the y axis ticks and labels, this was done because these y values don't give you much information
    #and can look bad. The y values weren't removed for the single multiplet graphs because those y values give clear 
    #information, here the highest peak doesn't correspond to anything since the
    #y values are scaled based on the area under the curve not the height of the highest peak. 
    plt.yticks([])
    plt.xlabel("ppm")
    plt.savefig("spectrum.png")
    #plt.savefig("spectrum.pdf")
    plt.close('all')
    make_window()

#Start window loop
make_window()