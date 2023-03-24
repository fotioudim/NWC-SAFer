from rich.panel import Panel

class ErrorPanel(Panel):
    def __init__(self, *args, **kwargs):
        super(ErrorPanel, self).__init__(*args, **kwargs)
        self.title = "Error"
        self.title_align = "left"
        self.border_style = "red"