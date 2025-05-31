#!/usr/bin/env python3
"""
monitor_windows_internals.py
Description: Monitors key Windows 11 internals such as CPU, memory, disk, and process information, and prints periodic summaries to the console with colorized output using Rich and Textual.
Author: Paul Watts
"""

import psutil
from rich.console import RenderableType
from rich.text import Text
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header, Static

# This widget displays the system stats and process table in the TUI.
class SystemStatsWidget(Static):
    # Reactive variables automatically update the UI when changed.
    stats = reactive("")  # Holds the system stats string (CPU, memory, disk)
    table = reactive("")  # Holds the process table as a string

    def render(self) -> RenderableType:
        """
        Render the widget using Rich Text, parsing markup for color.
        Returns a Rich Text object with stats and table.
        """
        text = Text.from_markup(self.stats + "\n\n")  # Parse stats markup
        text.append(Text.from_markup(self.table))  # Parse table markup
        return text

# The main application class for the TUI monitor.
class MonitorApp(App):
    # Key bindings for the app (press 'q' to quit)
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        """
        Compose the UI layout: header, stats widget, and footer.
        """
        yield Header()  # Top bar
        self.stats_widget = SystemStatsWidget()  # Main stats display
        yield self.stats_widget
        yield Footer()  # Bottom bar

    async def on_mount(self) -> None:
        """
        Called when the app starts. Sets up periodic updates.
        """
        self.set_interval(2, self.update_stats)  # Update stats every 2 seconds
        await self.update_stats()  # Initial update

    async def update_stats(self) -> None:
        """
        Gather system stats and update the widget.
        """
        # Get CPU usage percentage
        cpu = f"[bold yellow]CPU Usage:[/] [yellow]{psutil.cpu_percent()}%[/]"
        # Get memory usage
        mem = psutil.virtual_memory()
        memory = (
            f"[bold magenta]Memory:[/] [magenta]{mem.percent}%[/] used "
            f"([green]{mem.used // (1024**2)}MB[/]/[blue]{mem.total // (1024**2)}MB[/])"
        )
        # Get disk usage
        disk = psutil.disk_usage("/")
        disk_str = (
            f"[bold green]Disk:[/] [green]{disk.percent}%[/] used "
            f"([green]{disk.used // (1024**3)}GB[/]/[blue]{disk.total // (1024**3)}GB[/])"
        )
        # Get top 5 processes by memory usage
        processes = sorted(
            psutil.process_iter(["pid", "name", "memory_info"]),
            key=lambda p: p.info["memory_info"].rss if p.info["memory_info"] else 0,
            reverse=True,
        )
        # Build the process table as a list of markup strings with improved alignment
        table_lines = [
            "[bold underline]Top 5 Processes by Memory Usage:[/]",  # Table header
            f"[bold cyan]{'PID':>6}[/]  [bold white]{'Name':<24}[/]  [bold magenta]{'Memory (MB)':>12}[/]",  # Column titles
            f"{'-'*6}  {'-'*24}  {'-'*12}",  # Divider line
        ]
        for proc in processes[:5]:
            try:
                mem_mb = proc.info["memory_info"].rss // (1024**2)
                # Truncate long process names for neat columns
                name = (proc.info['name'][:21] + '...') if len(proc.info['name']) > 24 else proc.info['name']
                table_lines.append(
                    f"[cyan]{proc.info['pid']:>6}[/]  [white]{name:<24}[/]  [magenta]{mem_mb:>12}[/]"
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue  # Skip processes that can't be accessed
        # Combine stats and table for display
        stats = f"{cpu}\n{memory}\n{disk_str}"
        self.stats_widget.stats = stats
        self.stats_widget.table = "\n".join(table_lines)

# Entry point for the script

def main() -> None:
    """
    Start the Textual TUI application.
    """
    MonitorApp().run()

if __name__ == "__main__":
    main()
