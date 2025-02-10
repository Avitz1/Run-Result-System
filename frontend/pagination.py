class Pagination:
    def __init__(self, data, rows_per_page=5):
        self.data = data  # Full dataset
        self.rows_per_page = rows_per_page  # Number of rows per page
        self.current_page = 1  # Start on the first page

    def get_page_data(self):
        """Returns the data for the current page."""
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = self.current_page * self.rows_per_page
        return self.data[start_idx:end_idx]

    def total_pages(self):
        """Returns the total number of pages."""
        return (len(self.data) // self.rows_per_page) + (1 if len(self.data) % self.rows_per_page > 0 else 0)

    def next_page(self):
        """Move to the next page if possible."""
        if self.current_page < self.total_pages():
            self.current_page += 1
        return self.get_page_data()

    def previous_page(self):
        """Move to the previous page if possible."""
        if self.current_page > 1:
            self.current_page -= 1
        return self.get_page_data()

    def reset(self):
        """Reset pagination to the first page."""
        self.current_page = 1
        return self.get_page_data()



