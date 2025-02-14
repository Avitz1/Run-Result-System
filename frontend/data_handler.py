import re

class DataHandler:
    @staticmethod
    def get_tools():
        # This method should return a list of tool names from the backend
        return ["Tool 1", "Tool 2", "Tool 3"]

    @staticmethod
    def get_fields(tool_name):
        # This method should return a dictionary of fields and their types for the selected tool
        # Here, we'll return dummy data for demonstration purposes
        if tool_name == "Tool 1":
            return {"user": "string", "project": "string", "tag": "string"}
        elif tool_name == "Tool 2":
            return {"user": "string", "project": "string", "tag": "string", "aberrant_cells": "list", "avg_aberration": "float"}
        else:
            return {"user": "string", "project": "string", "tag": "string", "edge_focus": "list"}

    @staticmethod
    def get_filtered_data(tool_name, filters, page, last_id):
        # This method should fetch filtered data for the selected tool from the backend with pagination
        # Here, we'll return dummy data for demonstration purposes
        all_data = [
            {"user": "kenobi", "project": "falcon", "tag": "cred_opens-2.2-signal0872-", "aberrant_cells": ["/hier0/hier1/cell0", "/hier0/hier3/cell2"], "avg_aberration": 1.4892732007, "edge_focus": [0, 0, 1, 0]},
            {"user": "skywalker", "project": "xwing", "tag": "cred_opens-2.3-signal0872-", "aberrant_cells": ["/hier0/hier1/cell1", "/hier0/hier3/cell3"], "avg_aberration": 1.3892732007, "edge_focus": [1, 0, 1, 0]},
            {"user": "solo", "project": "millennium", "tag": "cred_opens-2.4-signal0872-", "aberrant_cells": ["/hier0/hier1/cell2", "/hier0/hier3/cell4"], "avg_aberration": 1.2892732007, "edge_focus": [1, 1, 1, 0]},
            {"user": "leia", "project": "rebel", "tag": "cred_opens-2.5-signal0872-", "aberrant_cells": ["/hier0/hier1/cell3", "/hier0/hier3/cell5"], "avg_aberration": 1.1892732007, "edge_focus": [0, 1, 1, 0]},
            {"user": "kenobi", "project": "falcon", "tag": "cred_opens-2.2-signal0872-", "aberrant_cells": ["/hier0/hier1/cell0", "/hier0/hier3/cell2"], "avg_aberration": 1.4892732007, "edge_focus": [0, 0, 1, 0]},
            {"user": "skywalker", "project": "xwing", "tag": "cred_opens-2.3-signal0872-", "aberrant_cells": ["/hier0/hier1/cell1", "/hier0/hier3/cell3"], "avg_aberration": 1.3892732007, "edge_focus": [1, 0, 1, 0]},
            {"user": "solo", "project": "millennium", "tag": "cred_opens-2.4-signal0872-", "aberrant_cells": ["/hier0/hier1/cell2", "/hier0/hier3/cell4"], "avg_aberration": 1.2892732007, "edge_focus": [1, 1, 1, 0]},
            {"user": "leia", "project": "rebel", "tag": "cred_opens-2.5-signal0872-", "aberrant_cells": ["/hier0/hier1/cell3", "/hier0/hier3/cell5"], "avg_aberration": 1.1892732007, "edge_focus": [0, 1, 1, 0]},
            {"user": "kenobi", "project": "falcon", "tag": "cred_opens-2.2-signal0872-", "aberrant_cells": ["/hier0/hier1/cell0", "/hier0/hier3/cell2"], "avg_aberration": 1.4892732007, "edge_focus": [0, 0, 1, 0]},
            {"user": "skywalker", "project": "xwing", "tag": "cred_opens-2.3-signal0872-", "aberrant_cells": ["/hier0/hier1/cell1", "/hier0/hier3/cell3"], "avg_aberration": 1.3892732007, "edge_focus": [1, 0, 1, 0]},
            {"user": "solo", "project": "millennium", "tag": "cred_opens-2.4-signal0872-", "aberrant_cells": ["/hier0/hier1/cell2", "/hier0/hier3/cell4"], "avg_aberration": 1.2892732007, "edge_focus": [1, 1, 1, 0]},
            {"user": "leia", "project": "rebel", "tag": "cred_opens-2.5-signal0872-", "aberrant_cells": ["/hier0/hier1/cell3", "/hier0/hier3/cell5"], "avg_aberration": 1.1892732007, "edge_focus": [0, 1, 1, 0]},
        ]

        filtered_data = []
        for record in all_data:
            match = True
            for field, pattern in filters.items():
                if field in record and isinstance(record[field], str):
                    if not re.search(pattern, record[field]):
                        match = False
                        break
            if match:
                filtered_data.append(record)

        # Simulate pagination by returning a subset of the data
        page_size = 4
        start_idx = page * page_size
        end_idx = start_idx + page_size
        paginated_data = filtered_data[start_idx:end_idx]
        last_id = paginated_data[-1]["tag"] if paginated_data else None
        total_pages = (len(filtered_data) + page_size - 1) // page_size

        columns = list(paginated_data[0].keys()) if paginated_data else []
        data = [[record[col] for col in columns] for record in paginated_data]
        return data, columns, last_id, total_pages