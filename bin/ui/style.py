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
            
            QComboBox::drop-down {
                        image:url(../res/task_expand.png);
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 20px;
            }
            QComboBox QAbstractItemView{
                       color:black;
                       background-color:#FFFFFF;
                       selection-color: black;
                       selection-background-color: green;
                       border: 1px solid #666666;
            }
                       
            QComboBox QAbstractItemView::item{
                       height: 30px;
            }
                            
            QPushButton {height: 30px;
                         background-color:#FFFFFF;
                         border:1px solid #A5A5A5;
                         padding-left:25px;
                         padding-right:25px;
            }   
            QPushButton:hover {background-color:#47A2ED; 
                               color: black;
                               border-style:outset}
            QSpinBox {
                        height: 30px;
                        width: 100px;
                        border: 1px solid #D7D7D7;
            }             
            QSpinBox::down-button{
                        image:url(../res/icon_arrow_down.png);
            }
            QSpinBox::up-button{
                        image:url(../res/icon_arrow_up.png);
            }
        """

    # option使用button
    SELECT_BUTTON = """
            QPushButton {height: 24px;
                         background-color:#FFFFFF;
                         border:1px solid #A5A5A5;
                         padding-left:25px;
                         padding-right:25px;
                         
            }
            QPushButton:hover {background-color:#47A2ED; 
                               color: black;
                               border-style:outset}
            QPushButton:click {background-color:#47A2ED; 
                               color: black;
                               border-style:inset}
    """

    # 左侧栏使用button
    TASKS_BUTTON = """
            QPushButton {height: 45px;
                         margin:0px;
                         color:white;
                         background-color:#4BAEB3;
                         border:1px solid #4BAEB3;
            }
    """
    LEFT_SIDE_BUTTON = """
            QPushButton {height: 45px;
                         margin:0px;
                         color:#333333;
                         background-color:#EBEBEB;
                         border:1px solid #EBEBEB;
            }
            QPushButton:hover { 
                               color: #4BAEB3;
                               }
    """

    # 右侧栏使用button
    OTHER_BUTTON = """
            QPushButton {height: 30px;
                         background-color:#FFFFFF;
                         border:1px solid #A5A5A5;
                         padding-left:25px;
                         padding-right:25px;
            }   
            QPushButton:hover {
                               color: #4BAEB3;
                               }
    """

    PROCEED_BUTTON = """
            QPushButton {height: 30px;
                         background-color:#FFFFFF;
                         border:2px solid #4BAEB3;
                         padding-left:25px;
                         padding-right:25px;
            }   
            QPushButton:hover {
                               color: #4BAEB3;
            }
    """
    TABLE = """
            QTableWidget {
                         selection-background-color:#EDF7F8;
                         selection-color:black;
            }
            QTableWidget::Item:hover {
                         background:#EDF7F8;
                         color:black;
            }
            QTableWidget::item:selected {
                         background:#EDF7F8;
                         color:red;
            }
            # QTableWidget QHeaderView::section{
            #              background-color:#FFFFFF;
            # }
    """

