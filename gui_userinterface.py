"""Simple Thread / Async / Await Demo"""

# System Imports
import asyncio
import threading
import time

# Third Party Imports
import PySimpleGUI as sg


class SyncAsyncAwaitDemoWindow:
    """Sync Async Await Demo Window"""

    def __init__(self):
        """Consructor"""
        layout = [
            [sg.Text("Not fetched yet!", key="-output-")],
            [
                sg.ProgressBar(
                    100,
                    orientation="h",
                    expand_x=True,
                    size=(20, 20),
                    key="-progress-",
                )
            ],
            [sg.Button("Submit Sync", key="-submit-sync-")],
            [sg.Button("Submit Async", key="-submit-async-")],
            [sg.Button("Submit Thread", key="-submit-thread-")],
            [sg.Button("Submit Long Run", key="-submit-long-run-")],
            [sg.Button("Exit")],
        ]

        self.window = sg.Window("Async Await Window", layout)

    def run(self):
        """Start the program"""
        self._run_loop()
        self.window.close()

    def _run_loop(self):
        """Run the Event loop"""
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event == "-submit-sync-":
                self._on_submit_sync(event, values)
            elif event == "-submit-async-":
                self._on_submit_async(event, values)
            elif event == "-submit-thread-":
                self._on_submit_thread(event, values)
            elif event == "-submit-long-run-":
                self._on_submit_long_run(event, values)

    # Methods to run when button is clicked
    def _on_submit_sync(self, event, values):
        """Do work for submitting synchronously"""
        self.window["-output-"].update("Fetching Name")
        name = self._get_name()
        self.window["-output-"].update(name)

    def _on_submit_async(self, event, values):
        """Do work for submitting asyncronously"""
        self.window["-output-"].update("Fetching Name")
        name = asyncio.run(self._get_name_async())
        self.window["-output-"].update(name)

    def _on_submit_thread(self, event, values):
        """Do work for submitting using threads"""
        self.window["-output-"].update("Fetching Name")
        task = threading.Thread(
            target=self._get_name_thread,
            args=("-done-long-run-",),
        )
        task.start()

    def _on_submit_long_run(self, event, values):
        """Do work for submitting with long running"""
        self.window["-output-"].update("Fetching Name Long Running")
        self.window.perform_long_operation(self._get_name, "-done-long-run-")

    # The simulated "long-running-tasks" that our buttons will trigger.
    def _get_name(self):
        """Get name from long running task"""
        for i in range(0, 20):
            time.sleep(0.5)
            self.window["-progress-"].update((i * 5) + 5)
        return "David Barnes"

    async def _get_name_async(self):
        """Get name from long running task asyncronously"""
        for i in range(0, 20):
            await asyncio.sleep(0.5)
            self.window["-progress-"].update((i * 5) + 5)
        return "David Barnes"

    def _get_name_thread(self, end_key):
        """Get name from long running task using a thread"""
        for i in range(0, 20):
            time.sleep(0.5)
            self.window["-progress-"].update((i * 5) + 5)
        self.window["-output-"].update("David Barnes")
