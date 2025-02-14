from data_handler import DataHandler

class EventHandlers:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.current_page = 0
        self.last_id = None
        self.total_pages = 0

    def get_tools(self):
        return DataHandler.get_tools()

    def tool_selected(self):
        selected_tool = self.dashboard.tool_selector.combo_box.currentText()
        if selected_tool != "Select a Tool":
            fields = DataHandler.get_fields(selected_tool)
            self.dashboard.update_filters(fields)
            self.current_page = 0
            self.last_id = None
            self.dashboard.set_pagination_buttons_enabled(False, False)

    def search_data(self):
        selected_tool = self.dashboard.tool_selector.combo_box.currentText()
        if selected_tool != "Select a Tool":
            filters = self.get_filters()
            data, columns, last_id, total_pages = DataHandler.get_filtered_data(selected_tool, filters, self.current_page, self.last_id)
            self.dashboard.update_table(data, columns)
            self.last_id = last_id
            self.total_pages = total_pages
            self.dashboard.update_pagination(total_pages)
            self.dashboard.set_pagination_buttons_enabled(self.current_page < self.total_pages - 1, self.current_page > 0)

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.search_data()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.search_data()

    def go_to_page(self):
        try:
            page = int(self.dashboard.pagination_controls.page_input.text()) - 1
            if 0 <= page < self.total_pages:
                self.current_page = page
                self.search_data()
        except ValueError:
            pass

    def get_filters(self):
        filters = {}
        for i in range(self.dashboard.filter_selector.layout.count()):
            filter_layout = self.dashboard.filter_selector.layout.itemAt(i)
            if filter_layout and filter_layout.layout():
                field_label = filter_layout.layout().itemAt(0).widget().text()
                field_input = filter_layout.layout().itemAt(1).widget().text()
                filters[field_label[:-1]] = field_input
        return filters

    def sort_data(self, column_index):
        self.dashboard.sort_table(column_index)