

####
"""
TODO:
- selection: add a third state for 'branch' cells => 'partly selected' (when some children are selected, not all)
  (currently, shows as 'not selected')

"""


#TODO: import only required fields?
from Qt.QtCore import Qt as qt

from Qt.QtWidgets import (
    QWidget,

    QVBoxLayout,
    QHBoxLayout,

    QTableWidget,
    QTableWidgetItem,
    QHeaderView,

    QGroupBox,


    QCheckBox,


...
)



#TODO: find better name
class TreeTable(QWidget):

    #TODO: allow no header (if all 'column_names' are ""?)
    #TODO: add flags?
    def __init__(self, column_names, parent=None):
        super(TreeTable, self).__init__(parent)

        #TODO: if 'column_names' is string => convert to list (split(","))


        self.build(column_names)



    def build(self, column_names):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.buildTable(column_names))
        layout.addWidget(self.buildButtons())



    #def setButtonsLabels(self, scan, select, deselect):
    #...

    def buildTable(self, column_names):
        #TODO: need 'self'?
        nb_columns = len(column_names) + 1 # Add 'select' column
        self.table = QTableWidget(0, nb_columns)

        table_header = QHeaderView(qt.Orientation.Horizontal)
        table_header.setStretchLastSection(True)
        self.table.setHorizontalHeader(table_header)
        self.table.setHorizontalHeaderLabels(column_names)
        #TODO: why?
        self.table.horizontalHeader().resizeSection(0, 0)
        self.table.verticalHeader().setVisible(False)

        return self.table


    def buildButtons(self):
        buttons_box = QGroupBox()
        buttons_layout = QHBoxLayout()
        buttons_box.setLayout(buttons_layout)

        self.scan_button = QPushButton("Scan")
        buttons_layout.addWidget(self.scan_button)
        self.select_button = QPushButton("Select All")
        buttons_layout.addWidget(self.select_button)
        self.deselect_button = QPushButton("Deselect All")
        buttons_layout.addWidget(self.deselect_button)

        self.scan_button.released.connect(self.scan)
        self.select_button.released.connect(self.selectAll)
        self.deselect_button.released.connect(self.deselectAll)

        return buttons_box




!!!!
'''
TODO: handle more than single 'filename'
=> filename as first column, +other columns
(same as before, but with list instead of string for leaf values)
(if no other columns => INPUT: [ path ], OUTPUT: { path: None }
Example:
INPUT:
[
[ path1, value11, value12 ]
[ path2, value21, value22 ]
[ branch1/branch11/path4, value41, value42 ]
[ branch1/path3, value31, value32 ]
]
OUTPUT:
{
    '_LEAVES': {
        path1: [ value11, value12 ],
        path2: [ value21, value22 ]
    },
    branch1: {
        branch11: {
            '_LEAVES': {
                path4: [ value41, value42 ]
            }
        },
        '_LEAVES': {
            path3: [ value31, value32 ]
        }
    }
}
'''
    '''
    #TODO: rename!
    @staticmethod
    def getTree(full_paths):
        tree_names = { "_LEAVES": [] }

        for full_path in full_paths:
            dir_dict = tree_names

            sub_path = os.path.dirname(full_path)
            file_name = os.path.basename(full_path)
            if sub_path:
                sub_dirs = sub_path.split("/")
                for sub_dir in sub_dirs:
                    if not sub_dir in dir_dict:
                        dir_dict[sub_dir] = { "_LEAVES": [] }
                    dir_dict = dir_dict[sub_dir]

            if not file_name in dir_dict["_LEAVES"]:
                dir_dict["_LEAVES"].append(file_name)

        return tree_names
    '''
    #TODO: rename (function+params)!
    @staticmethod
    def getTree(data_lines):
        tree_names = { "_LEAVES": [] }

        for data_line in data_lines:
            dir_dict = tree_names

            full_path = data_line[0]

            #TODO: handle other separator (use a class field 'self.separator')
            sub_path = os.path.dirname(full_path)
            file_name = os.path.basename(full_path)
            if sub_path:
                sub_dirs = sub_path.split("/")
                for sub_dir in sub_dirs:
                    if not sub_dir in dir_dict:
                        dir_dict[sub_dir] = { "_LEAVES": [] }
                    dir_dict = dir_dict[sub_dir]

            if not file_name in dir_dict["_LEAVES"]:
                dir_dict["_LEAVES"].append([file_name, data_line[1:]])

        return tree_names



    def refreshTable(self):
        nb_rows = self.table.rowCount()

        if nb_rows == 0:
            self.select_button.setEnabled(False)
            self.deselect_button.setEnabled(False)
            return

        for index in range(nb_rows):
            self.table.showRow(index)

            item = self.table.cellWidget(index, 1)
            parent_index = item.property("parent")

            if parent_index == None:
                continue

            while parent_index != None:
                parent = self.table.cellWidget(parent_index, 1)
                parentExpand = parent.property("expand")
                if not parentExpand:
                    self.table.hideRow(index)
                    break

                parent_index = parent.property("parent")


        #self.table.resizeColumnsToContents()

        self.select_button.setEnabled(True)
        self.deselect_button.setEnabled(True)





    def clear(self):
        # Safety check (if executed before finished building
        if (
            not hasattr(self, "table")
            or not self.table.rowCount()
        ):
            return

        self.table.setRowCount(0)
        #TODO: required?
        #self.refreshTable()


    def update(self):
        #TODO: see how to pass data!
        '''
        tex_path = self.tex_path_edit.text()

        if (
            not tex_path
            or not os.path.isdir(tex_path)
        ):
            self.clearShadersTable()
            return

        if tex_path != self.scanned_tex_path:
            self.clearShadersTable()
            self.scanned_tex_path = tex_path
        '''

        ####
        #TODO: FIX UPDATE! (instead of clear+refill)
        self.clear()
        ####
        self.fillTable()


!!!!
CONTINUE FROM HERE!
    def fillShadersTable(self):
        #TODO: rewrite with 'getInputs'?
        shader_names = self.controller.getShadersList(
            rule_fields = self.presets.get("rule_fields", {}),
            texture_variant_rule = self.variant_edit.text(),
            texture_novariant_rule = self.novariant_edit.text(),
            shader_tag = self.shader_tag_edit.text(),
            shader_variant_rule = self.shader_variant_edit.text(),
            shader_novariant_rule = self.shader_novariant_edit.text(),
            tex_path = self.tex_path_edit.text(),
            include_subdirectories = self.tex_subdir_checkbox.isChecked()
        )
        logger.info("Shader names: {}".format(shader_names))

        #TODO: if nothing found, add a text ~"make sure the rules are ok" (?)


        # Update the table
        #TODO: make separate function
        ########
        shader_names = self.getTree(shader_names)
        for shader_name in shader_names:
            #print shader_name
            #print shader_names[shader_name]

            #TODO: pass more info (files? fields?)
            data = None #TODO
            self.addShaderTableItem(shader_name, shader_names[shader_name])

        self.refreshShadersTable()
        ########








    def addTableItem(self, value, data, level=0, parent_index=None):

        nbElements = 0

        if value == "_LEAVES":
            # => Leaves list

            nbRows = self.table.rowCount()

            parent = None
            if level:
                #TODO: find faster way
                # Get first row from here with 'level-1'
                for index in range(nbRows, 0, -1):
                    parent_index = index-1
                    item = self.table.cellWidget(parent_index, 0)
                    parent_level = item.property("level")
                    if parent_level < level:
                        parent = parent_index
                        break
                else:
                    raise ValueError("Incoherent data")

            for entry in data:
                nbElements += self.addTableItem(entry, data[entry], level, parent)


        else:
            if isinstance(data, dict):
                # => Branch
                nbElements = 0

                nbRows = self.table.rowCount()
                self.table.insertRow(nbRows)

                self.addCheckBox(nbRows, level)
                self.addTreeCell(False, value, nbRows, level, parent_index)

                # Add the children
                for entry in data:
                    nbElements += self.addTableItem(entry, data[entry], level+1, nbRows)

            elif isinstance(data, list):
                # => Leaf
                nbElements = 1

                nbRows = self.table.rowCount()
                self.table.insertRow(nbRows)

                self.addCheckBox(nbRows, level)

                #self.addLeafCell(value, nbRows, level, parent_index)
                self.addTreeCell(True, value, nbRows, level, parent_index)

                #TODO: add other column data
                '''
                for index, elt in enum(data):
                    setItem col_index+2, elt
                '''

        return nbElements




    def scan(self):
        #TODO: needed? see how to pass data!
        raise Exception("TOSO")

        '''
        tex_path = self.tex_path_edit.text()

        # Check tex path
        invalid = False
        if not tex_path:
            dialogs.alert(
                self,
                "The textures path must be specified",
                "No textures path"
            )
            invalid = True

        elif not os.path.isdir(tex_path):
            dialogs.alert(
                self,
                "Textures path '{}' is not a valid directory".format(
                    tex_path
                ),
                "Directory not found"
            )
            invalid = True

        if invalid:
            self.clearShadersTable()
            return

        if tex_path != self.scanned_tex_path:
            self.clearShadersTable()
            self.scanned_tex_path = tex_path

        self.updateShadersTable()
        '''

    def selectAll(self, select=True):
        for index in range(self.table.rowCount()):
            item = self.table.cellWidget(index, 0)
            self.setSelected(item, select)


    def deselectAll(self):
        self.selectAll(False)


    @staticmethod
    def setSelected(item, checked):
        checkBox = item.findChild(QCheckBox)
        #TODO: if none => ERROR (?)
        if checkBox:
            checkBox.setChecked(checked)
            item.setProperty("select", checked)


    def getSelected():
        ...





    def clickSelected(self):
        checkbox = self.sender()
        parent = checkbox.parent()

        checked = checkbox.isChecked()
        index = parent.property("row")
        level = item.property("level")

        nextIndex = index + 1
        next = self.table.cellWidget(nextIndex, 0)
        while next:
            nextLevel = next.property("level")

            if nextLevel <= level:
                break

            self.setSelected(next, checked)

            nextIndex = nextIndex + 1
            next = self.table.cellWidget(nextIndex, 0)


        #TODO: not needed (?)
        #self.refreshTable()



    def setExpand(self):
        button = self.sender()
        parent = button.parent()

        expand = parent.property("expand")
        expand = not expand

        #TODO: arrow... USE ICONS!
        if expand:
            button.setText("V")
        else:
            button.setText(">")

        parent.setProperty("expand", expand)

        self.refreshTable()







    def addCheckBox(self, row, level, checked=True):
        widget = QWidget()
        layout = QHBoxLayout()
        #layout = QGridLayout()
        widget.setLayout(layout)

        checkbox = QCheckBox()
        layout.setAlignment(qt.AlignCenter)
        layout.addWidget(checkbox)
        #layout.addWidget(checkbox, qt.AlignHCenter)
        #layout.addWidget(checkbox, 0, 0, 1, 1, qt.AlignLeft)
        #layout.addWidget(checkbox, 0, 0, 1, 1, qt.AlignHCenter)

        #TODO: not necessary
        checkbox.setChecked(checked)
        widget.setProperty("select", checked)

        widget.setProperty("level", level)

        #TODO: better way?
        # => way to get row number from widget?
        widget.setProperty("row", row)
        checkbox.toggled.connect(self.clickSelected)

        #TODO: change (inherit from hierarchy)
        widget.setContentsMargins(0, 0, 0, 0)
        checkbox.setStyleSheet("QCheckBox { background-color: rgb(32,32,32); }")
        #checkbox.setStyleSheet("QCheckBox { margin: 0; }")

        widget_item = QTableWidgetItem()
        widget_item.setFlags(qt.NoItemFlags|qt.ItemIsEnabled)
        #if level == 0:
        #    widget_item.setData(qt.BackgroundRole, self.headerColor)


        self.table.setItem(row, 0, widget_item)
        self.table.setCellWidget(row, 0, widget)




    #TOOD: rename?
    def addTreeCell(self, leaf, value, row, level, parent_index):
        widget = QWidget()
        #layout = QHBoxLayout()
        layout = QGridLayout()
        widget.setLayout(layout)

        label = QLabel(value)
        #TODO: change?
        label.setStyleSheet("QLabel { padding-left: %sem; }" % level)
        #layout.addWidget(label, qt.AlignLeft)
        #layout.addWidget(label, 0, 1, 1, 2, qt.AlignLeft)
        layout.addWidget(label, 0, 0, 1, 2, qt.AlignLeft)
        #layout.setContentsMargins(0, 0, 0, 0)
        #widget.setProperty("level", level)
        #selectCheckBox.setStyleSheet("QLabel { QSizePolicy: Maximum; }")

        #TODO: nedeed? => easier to retrieve value
        widget.setProperty("name", value)
        if parent_index != None:
            widget.setProperty("parent", parent_index)


        if leaf:
            widget.setProperty("file", True)
        else:
            #TODO: move to left of label
            # Add the expand button
            #TODO: arrow... MAKE ICONS!
            #expandButton = QPushButton(">")
            expandButton = QPushButton("V")
            #layout.addWidget(expandButton, 0, 3, 1, 1, qt.AlignRight)
            layout.addWidget(expandButton, 0, 2, 1, 1, qt.AlignRight)
            #TODO: can avoid lambda?
            #expandButton.released.connect(lambda:self.setExpand(expandButton, row))
            expandButton.released.connect(
                lambda expandButton=expandButton, row=row:
                self.setExpand(expandButton, row)
            )
            #widget.setProperty("expand", False)
            widget.setProperty("expand", True)

        widgetItem = QTableWidgetItem()
        widgetItem.setFlags(qt.NoItemFlags|qt.ItemIsEnabled)
        #if level == 0:
        #    widgetItem.setData(qt.BackgroundRole, self.headerColor)
        self.table.setItem(row, 1, widgetItem)

        #widget.setStyleSheet("QTableWidget item { padding-left: 50px; }")
        #self.table.setCellWidget(row, 0, widget)
        self.table.setCellWidget(row, 1, widget)


