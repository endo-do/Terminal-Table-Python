"""
Documentation:
- I will to column as col through out this documentation
- Each Function will have a short explanation at the start that explains the general purpose and each argument
- If a documentation would be the exact same as a similar above it will be replaced with '...'
"""


### General Functions

def restructure(data, structure, fill_with_empty_columns=None, fill_with_empty_rows=None, empty_dicts=None, empty_lists=None, empty_cells=None, replace_empty=None):
    
    """
    Restructures the given data based on the specified structure.

    Args:
    - data: The data to be restructured.
    - structure: The desired form in which data will be restructured (e.g., "list").
    - fill_with_empty_columns: If True, adds columns that are not specified, otherwise skips them during table printing.
    - fill_with_empty_rows: [Commentary missing]
    - empty_dicts: Specifies how an empty dict looks like.
    - empty_lists: [Commentary missing]
    - empty_cells: Specifies how an empty cell looks like.
    - replace_empty: Content to replace when an empty dict/list/cell is specified.

    Returns:
    - The restructured and cleaned data.
    """

    # if the data is an empty list return it empty
    if data in empty_lists:
        return [replace_empty]
    
    else:
        
        # get the structure of the data with the type() function
        data_type = type(data) 
        if data_type is list:
            element_type = type(data[0]) 
        elif data_type is dict:
            element_type = type(next(iter(data.values()))) 
        
        # restructers the data into a list
        if structure == "list":    
            data_structure = data_type.__name__

            # if data is a dictionary
            if data_structure == "dict":            

                # sorts all the keys that represent the columns in ascending order and saves them
                columns = list(data.keys())
                columns = sorted(columns)

                # adds empty columns if specified in fill_with_empty_columns
                if fill_with_empty_columns:
                    if len(columns) >= 2:
                        for i in range(columns[0], columns[-1]):
                            if i not in columns:
                                data[i] = replace_empty

                # sorts the dictionary and restructeres it to a list
                data = dict(sorted(data.items()))
                data = [i for i in list(data.values())]
            
            # goes through all cells to replace any cell that was specified as empty with the given replace_empty var
            for index, i in enumerate(data):
                if i in empty_cells:
                    data[index] = replace_empty

            # returns the restructured and cleaned data as a list
            return data
        
        # restructures the data into a list_in_list structure
        if structure == "list_in_list":
            data_structure = f"{element_type.__name__}_in_{data_type.__name__}"

            # if the data is a dict_in_list structure
            if data_structure == "dict_in_list":
                
                # adds empty rows if specified in fill_with_empty_rows
                if fill_with_empty_rows:
                    rows = [key for d in data for key in d]
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data.append({row:[]})
                
                # sorts data and creates a var for the restructured data
                new_content = []
                data = sorted(data, key=lambda d: next(iter(d)))

                # restructures the data and cleans it
                for line in data:    
                    if any(str(val) in empty_dicts for val in line.values()):
                        new_content.append([replace_empty])
                    else:
                        new_content.extend([char for char in line.values()])
                
                # replaces the old data with the new sorted and cleaned data
                data = new_content

            # if the data is a list_in_dict structure
            elif data_structure == "list_in_dict":
                
                # ...
                if fill_with_empty_rows:
                    rows = list(data.keys())
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data[row] = []
                
                # ...
                new_content = []
                data = dict(sorted(data.items()))
                
                # ...
                for line in data.values():
                    if line in empty_lists:
                        new_content.append([replace_empty])
                    else:
                        new_content.append(line)
                
                # ...
                data = new_content

            # if the data is a dict_in_dict structure
            elif data_structure == "dict_in_dict":
                
                # ...
                if fill_with_empty_rows:
                    rows = list(data.keys())
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data[row] = {}
                
                # ...
                if fill_with_empty_columns:
                    for key, row in data.items():
                        columns = list(row.keys())
                        if len(columns) >= 2:
                            for col in range(columns[0], columns[-1]):
                                if col not in columns:
                                    data[key][col] = replace_empty
                
                # ...
                new_content = []
                data = {k: dict(sorted(v.items())) if isinstance(v, dict) else v for k, v in sorted(data.items())}

                # ...
                for line in data:
                    if data[line] in empty_dicts:
                        new_line = [replace_empty]
                    else:
                        new_line = []
                        for cell in data[line].values():
                            if str(cell) in empty_cells:
                                cell = replace_empty
                            new_line.append(cell)
                    new_content.append(new_line)
                
                # ...
                data = new_content
            
            # Goes through the data and replaces every cell that is specified as empty with the replace_empty var
            new_content = []
            for line in data: 
                new_content.append([str(char) if char not in empty_cells else replace_empty for char in line])
                data = new_content 
            
            # returns the restructured and cleaned data as a list_in_list
            return data



### The Table Class
        
class Table:
    def __init__(
        self,
        content,
        space_left=1,
        space_right=1,
        orientation="left",
        min_width=None,
        max_width=None,
        same_sized_cols=True,
        fill_with_empty_rows=True,
        fill_with_empty_columns=True,
        empty_cells=["", "#empty"],
        empty_lists=[[], [""], ["#empty"]],
        empty_dicts=[{}, {""}, {"#empty"}],
        replace_empty="",
        header={"row": ["#default"]},
    ):
        
        """
        Initialize a Table object with specified parameters

        Args:
        - content: content of the table in a list_in_list, list_in_dict, dict_in_list or dict_in_dict structure
        - space_left: int: space from the content of a cell to the border on the left side
        - space_right: ... on the right side ...
        - orientation: str: "left" or "right" | orientates the content to the left or to the right side of the cell
        - min_width: int: minimum width of a cell. spaces will be added when to short
        - max_width: int: maximum width of a cell. content will be shortened when to long
        - same_sized_cols: bool: toggles same width for each column
        - fill_with_empty_rows: bool: toggles filling empty rows for every not specified row in content
        - fill_with_empty_columns: ... columns ... columns ...
        - empty_cells: list: specifies what is considered as an empty cell
        - empty_lists: ... list
        - empty_dicts: ... dict
        - replace_empty: str: replaces empty cells and the content of empty lists and dicts
        - header: dict {header_type:[header]}: header_type: str: "row" or "col", "header": list or dict: content of the header
        """
    
        self.content = content 
        self.space_left = space_left 
        self.space_right = space_right 
        self.orientation = orientation 
        self.min_width = min_width 
        self.max_width = max_width 
        self.same_sized_cols = same_sized_cols 
        self.fill_with_empty_rows = fill_with_empty_rows 
        self.fill_with_empty_columns = fill_with_empty_columns 
        self.empty_cells = empty_cells 
        self.empty_lists = empty_lists 
        self.empty_dicts = empty_dicts 
        self.replace_empty = replace_empty 
        self.header = header
        
        # set the header_actions to 'insert'
        self.header_action_col = "insert"
        self.header_action_row = "insert"

        # restructure the given content
        self.content = restructure(self.content, "list_in_list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)

   
    def add_row(self, index, row):
        
        """
        Adds a row at specified index into the content of the tablet

        Args:
        - index: int: specifies at what index the column will be added
        - row: the content of the new row in a dict or list structure
        
        """

        # handle index if specified as counting from the end because will be working with the insert function that doesnt add element at last place with index = -1
        if index == -1:
            index = "end"
        else:
            if index < 0:
                index += 1
            # offset the index by 1 when the row header is active to insert the content accurate
            if "row" in self.header:
                index += 1
        
        # restructure the row to a list structure
        row = restructure(row, "list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)
        
        # add a place holder header if col header is active to prevent errors later on when handling the headers
        if "col" in self.header:
            row.insert(0, "")
        
        # handle inserting at last place
        if index == "end":
            self.content.append(row)
        else:
            self.content.insert(index , row)
        
        # set the headers to update for later on
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"

   
    def add_column(self, index, column):

        """
        Adds a column at specified index into the content of the table
        
        Args:
        - index: int: specifies at what index the column will be added
        - column: the content of the new row in a dict or list structure
        """

        # ...
        if index == -1:
            index = "end"
        else:
            if index < 0:
                index += 1
            # ... column ...
            if "col" in self.header:
                index += 1
        
        # ...
        column = restructure(column, "list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)
        
        # ...
        if "row" in self.header:
            column.insert(0, "")
        
        # ...
        for i in range(len(column)):
            if index == "end":
                self.content.append(column[i])
            else:
                self.content[i].insert(index, column[i])
        
        # ...
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"


    def remove_row(self, index):
        
        """
        removes the row at specified index from the table

        Args:
        - index: int: specifies which row will be removed
        """
        
        # offset the index by one when row header is active to remove the correct row
        if "row" in self.header:
            index += 1

        # remove the specified row
        self.content.pop(index)
        
        # set the headers to update for later on
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"


    def remove_column(self, index):
        
        """
        removes the column at specified index from the table
        
        Args:
        - index: int: specifies which column will be removed
        """

        # ... column ... column
        if "col" in self.header:
            index += 1
        
        # ... column
        for i in self.content:
            i.pop(index)
        
        # ...
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"


    def replace_cell(self, row, col, replace=None):
        
        """
        replaces the content of the specified cell with the specified content
        
        Args:
        - row: int: specifies in which row the cell is in
        - col: int: ... column ...
        - replace: str/int: specifies with what the cell's content will be replaced
        """
        # if replacemen was not specified it will be replaced with standart empty content specified in the table
        if replace == None:
            replace = self.replace_empty
        
        # handle index offset due to headers
        if "row" in self.header:
            row += 1
        if "col" in self.header:
            col += 1
        
        # replace the content
        self.content[row][col] = replace


    def swap_cols_rows(self):

        """
        swaps the columns with the rows and vice versa

        """

        # swap the headers
        if "row" in self.header:
            if "col" in self.header:
                col = self.header["col"]
                self.header["col"] = self.header["row"]
                self.header["row"] = col
            else:
                self.header["col"] = self.header["row"]
                del self.header["row"]
        elif "col" in self.header:
            self.header["row"] = self.header["col"]
            del self.header["col"]

        # swap the columns with the rows and vice versa
        self.content = list(map(list, zip(*self.content)))

        # set the headers to update for later on
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"

    
    def conf_header(self, header, action, content=None, index=None):
        """
        add, remove or edit headers

        Args:
        - header: {header_type:header_content}: 
            - header_type ("row" or "col") specifies which header will be edited
            - header_content (in dict or list structure OR in str when editing a specific header) specifies the content
                - [#default] automaticly sets the header to a simple col/row count
        - action: str: 'add', 'remove', 'edit' or fully 'replace' existing header
        - index: int: when editing a specific header specifies the row or column
        """
        
        # handle removing a header
        if action.lower() == "remove":
            if header in self.header:
                
                # delete the header and its implemented content from of the table
                del self.header[header]
                if header == "row":
                    self.content.pop(0)
                elif header == "col":
                    for i in self.content:
                        i.pop(0)

        # handle editing the header of a specific row or column
        elif action.lower() == "edit":
            
            # handle the row header
            if header == "row" and "row" in self.header:
            
                # replace the header with specified content and set header_action to update
                self.header["row"][index] = content
                self.header_action_row = "update"
            
            # ... col ...
            elif header == "col" and "col" in self.header:
                
                # ...
                self.header["col"][index] = content
                self.header_action_col = "update"
        
        # handle adding or replacing existing
        elif action.lower() == "add" or action.lower() == "replace":
            
            # handle row header
            if header == "row":
                if header not in self.header:
                    self.header_action_row = "insert"
                else:
                    self.header_action_row = "update"
            
            # handle col header
            elif header == "col":
                if header not in self.header:
                    self.header_action_col = "insert"
                else:
                    self.header_action_col = "update"
        
            # add the specified header or replace it if it already exists
            self.header[header] = restructure(content, "list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)

    
    def display(self):

        """
        the main function that displays the table
        """

        # handle the row header such as implementing it to the table or update it if necessary
        if "row" in self.header:
            
            # handle 'update' header action
            if self.header_action_row == "update":
                
                # remove the implemented header and set action the 'insert' to fully update the header
                self.content.pop(0)
                self.header_action_row = "insert"

            # handle 'insert' header action
            if self.header_action_row == "insert":
                
                # recalculate the count of columns
                self.columns = 0
                for row in self.content:
                    if len(row) > self.columns: 
                        self.columns = len(row)

                # if header content is not specified implement the default one
                if self.header["row"] == ["#default"]:    
                    self.header["row"] = [f"{index+1}." for index in range(0, self.columns)]

                # if header content is specified by user
                else: 
                    
                    # add empty headers if header content doesnt cover all rows
                    if len(self.header["row"]) < self.columns -1 if "col" in self.header else self.columns:
                        for i in range(self.columns -1 if "col" in self.header else self.columns - len(self.header["row"])):
                            self.header["row"].append(self.replace_empty)
             
                # implement the header into the content of the table
                self.content = [self.header["row"]] + self.content
        
        # ... col ...
        if "col" in self.header:

            # ...
            if self.header_action_col == "update":
            
                # ...
                for i in self.content:
                    i.pop(0)    
                self.header_action_col = "insert"

            # ...
            if self.header_action_col == "insert":

                # ...
                if self.header["col"] == ["#default"]:
                    self.header["col"] = [f"{index+1}." for index in range(0, len(self.content))]

                # ...
                else:

                    # ... columns
                    if len(self.header["col"]) < len(self.content):
                        for i in range(len(self.content) - len(self.header["col"])):
                            self.header["col"].append(self.replace_empty)

                # handle if row and col header are active
                if "row" in self.header:
                    self.header["col"].pop(-1)
                    self.header["col"].insert(0, self.replace_empty)

                # ... 
                for index, i in enumerate(self.header["col"]):
                    self.content[index] = [i] + self.content[index]

        # set header actions to nothing
        self.header_action_col = "nothing"
        self.header_action_row = "nothing"

        # recalculate the counts fo columns and rows
        self.rows = len(self.content)
        self.columns = 0
        for row in self.content:
            if len(row) > self.columns: 
                self.columns = len(row)

        # adding empty cells to fill up missing cells
        for row in self.content:
            
            while len(row) < self.columns:
                row.append(self.replace_empty)

        # calculating the amount of chars per column = width of the column
        self.max_chars = []
        for cell in range(self.columns): 
            self.max_chars.append(0)
        for row in self.content: 
            active_column = 0
            for cell in row:
                if len(str(cell)) > self.max_chars[active_column]: 
                    self.max_chars[active_column] = len(str(cell))
                active_column += 1
        column_index = 0  
        
        # set a minimum width for each column if specified
        if self.min_width != None:
            for index, i in enumerate(self.max_chars):
                if self.min_width > int(i):
                    self.max_chars[index] = self.min_width
        
        # ... maximum ...
        if self.max_width != None:
            for index, i in enumerate(self.max_chars):
                if self.max_width < int(i):
                    self.max_chars[index] = self.max_width

        # implement the same size for each column if specified
        if self.same_sized_cols:
            self.max_chars = [max(self.max_chars) for i in self.max_chars]

        ### printing the table
    
        # print the headline
        print("╔", end="")
        for column in self.max_chars:
            print("═" * self.space_left, end="")  
            print("═" * column, end="")  
            print("═" * self.space_right, end="")  
            
            if column_index == len(self.max_chars) - 1:  
                print("╗")
            
            else:
            
                if "col" in self.header and column_index == 0:
                    print("╦", end="")
            
                else:
                    print("╤", end="")  
            
            column_index += 1  

        row_index = 0  

        # print each row
        for row in range(self.rows): 
            print("║", end="") 
            column_index = 0

            # for each cell in row
            for column in range(self.columns):
                
                # calculate amount of spaces to add to content to ensure correct sizing of the cell
                spacebar_counter = self.max_chars[column] - len(str(self.content[row][column])) 
                text = str(self.content[row][column])

                # handle if content is larger than max width
                if len(text) > self.max_chars[column_index]:

                    if self.max_chars[column_index] == 2:
                        text = ".."
                    elif int(self.max_chars[column_index]) == 3:
                        text = [i for i in text]
                        text = text[0]
                        text += ("..")
                    
                    elif int(self.max_chars[column_index]) >= 3:
                        text = [i for i in text]
                        text = text[:int(self.max_chars[column_index])-2]
                        text.append("..")
                        textstr = ""
                        for i in text:
                            textstr += i
                        text = textstr
                    spacebar_counter = 0
                
                # handle left orientation
                if self.orientation == "left": 
                    content = text + str(spacebar_counter * " ")  
                
                # ... right ...
                elif self.orientation == "right":
                    content = str(spacebar_counter * " ") + text 

                # print the cell
                print(" " * self.space_left, end="")
                print(content, end="")
                print(" " * self.space_right, end="")
                
                # handle the vertical separators between cells and the right border
                if column_index == self.columns - 1: 
                    print("║") 
                else:
                    if "col" in self.header and column_index == 0:
                        line = "║"
                    else:
                        line = "│" 
                    print(line, end="")
                column_index += 1  
            
            # handle the horizontal sperators between rows and the bottom border
            if row_index == 0 and "row" in self.header: 
                left_border = "╠"
                connection = "═"
                right_border = "╣"
                cross_connection = "╪"

            elif row_index == self.rows - 1:
                left_border = "╚"
                connection = "═"
                right_border = "╝"
                cross_connection = "╧"

            else:
                left_border = "╟"
                connection = "─"
                right_border = "╢"
                cross_connection = "┼"

            print(left_border, end="") 
            column_index = 0

            # print the horizontal separators
            for column in self.max_chars: 
                print(connection * self.space_left, end="")
                print(column * connection, end="") 
                print(connection * self.space_right, end="") 
                
                if column_index == len(self.max_chars) - 1: 
                    print(right_border)
                
                else:
                
                    if "col" in self.header and column_index == 0:
                
                        if row_index == self.rows - 1:
                            print("╩", end="")
                
                        elif "row" in self.header and row_index == 0:
                            print("╬", end="")
                
                        else:
                            print("╫", end="")
                
                    else:
                        print(cross_connection, end="") 

                column_index += 1

            row_index += 1