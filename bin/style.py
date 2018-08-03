# -*- coding: utf-8 -*-#


class Style:
    COMMON_STYLE = """
            QCheckBox { spacing: 10px;}
            QCheckBox::indicator {width: 20px;height: 20px;}
            QCheckBox::indicator:unchecked {image:url(../res/check_unsel.png);}
            QCheckBox::indicator:checked {image:url(../res/check_sel.png);}
            
            QLineEdit {height: 30px;}
            QLineEdit {selection-color: white;}
            QLineEdit {margin: 2px;}
        """
