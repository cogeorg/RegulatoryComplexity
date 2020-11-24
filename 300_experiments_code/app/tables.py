from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('Id', show=True)
    correctanswer = Col('Correct Answer', show=True)
    Col('Your Answer', show=True)