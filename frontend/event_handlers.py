from data_handler import DataHandler

class EventHandlers:
    def __init__(self, dashboard):
        self.dashboard = dashboard

    def tool_selected(self):
        selected_tool = self.dashboard.tool_selector.combo_box.currentText()
        if selected_tool != "Select a Tool":
            data, columns = DataHandler.get_data(selected_tool)
            self.dashboard.update_table(data, columns)