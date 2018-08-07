# -*- coding: utf-8 -*-#


class Style:
    COMMON_STYLE = """
            QCheckBox { spacing: 10px;}
            QCheckBox::indicator {width: 20px;height: 20px;}
            QCheckBox::indicator:unchecked {image:url(../res/check_unsel.png);}
            QCheckBox::indicator:checked {image:url(../res/check_sel.png);}
            
            
            QLineEdit {height: 30px;
                       border:1px solid #D7D7D7;
                       selection-color: white;
                       margin: 2px;}
            
            QLabel {height: 40px;}
            
            QComboBox {height:30px;
                       width:120px;
                       color:black;
                       selection-color: black;
                       selection-background-color: #FFFFFF;
                       border:1px solid #D7D7D7;
                       background-color:#FFFFFF;
            }
            
            QComboBox::down-arrow{
                       image:url(../res/task_expand.png);
                       border-left-width: 1px;
                       border-left-color: darkgray;
            }
            QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 20px;
            }
            QComboBox QAbstractItemView{
                       height:30px;
                       width:100px;
                       color:black;
                       background-color:#FFFFFF;
                       selection-color: black;
                       selection-background-color: #ECF6FE;
            }
                       
            QComboBox QAbstractItemView::item{
                       height: 30px;
            }
            QListView::item {
                       height: 30px;
                       background: white;
            }
                
            QPushButton {height: 30px;
                         background-color:#FFFFFF;
                         border:1px solid #A5A5A5;
                         padding-left:25px;
                         padding-right:25px;
            }
        """
