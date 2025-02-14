class DataHandler:
    @staticmethod
    def get_tools():
        # This method should return a list of tool names from the backend
        return ["Tool 1", "Tool 2", "Tool 3"]

    @staticmethod
    def get_data(tool_name):
        # This method should fetch data for the selected tool from the backend
        # Here, we'll return dummy data for demonstration purposes
        if tool_name == "Tool 1":
            data = [
                ["Run 1", "Success", "2025-02-14"],
                ["Run 2", "Failure", "2025-02-13"]
            ]
            columns = ["Run ID", "Status", "Date"]
        elif tool_name == "Tool 2":
            data = [
                ["Run A", "Success", "2025-02-14", "User A"],
                ["Run B", "Failure", "2025-02-13", "User B"]
            ]
            columns = ["Run ID", "Status", "Date", "User"]
        else:
            data = [
                ["Step 1", "Completed", "2025-02-14", "10 min", "User A"],
                ["Step 2", "Failed", "2025-02-13", "15 min", "User B"]
            ]
            columns = ["Step", "Status", "Date", "Duration", "User"]
        return data, columns