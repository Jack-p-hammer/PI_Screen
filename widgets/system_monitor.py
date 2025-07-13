from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import psutil
import time

class SystemMonitorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 2
        
        # Create labels for different metrics
        self.cpu_label = Label(text="CPU: Loading...", font_size='12sp', size_hint_y=None, height=20)
        self.memory_label = Label(text="RAM: Loading...", font_size='12sp', size_hint_y=None, height=20)
        self.disk_label = Label(text="Disk: Loading...", font_size='12sp', size_hint_y=None, height=20)
        self.temp_label = Label(text="Temp: Loading...", font_size='12sp', size_hint_y=None, height=20)
        
        # Add labels to layout
        self.add_widget(self.cpu_label)
        self.add_widget(self.memory_label)
        self.add_widget(self.disk_label)
        self.add_widget(self.temp_label)
        
        # Cache for system data
        self.last_update = 0
        self.cached_data = None
        self.update_interval = 10  # 10 seconds
        self.first_update = True  # Flag for first update

    def render(self, parent):
        parent.add_widget(self)
        self.update()

    def update(self):
        current_time = time.time()
        
        # Skip cache check on first update or if forced
        if self.first_update:
            self.first_update = False
            self.last_update = 0  # Force update
        
        # Only update if enough time has passed
        if current_time - self.last_update < self.update_interval and self.cached_data and not self.first_update:
            return
            
        try:
            # CPU usage (with shorter interval for more accurate reading)
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_gb = memory.used / (1024**3)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_gb = disk.used / (1024**3)
            
            # CPU temperature (Raspberry Pi specific)
            temp_text = "Temp: N/A"
            try:
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                    temp_celsius = float(f.read()) / 1000
                    temp_fahrenheit = temp_celsius * 9/5 + 32
                    temp_text = f"Temp: {temp_fahrenheit:.1f}°F"
            except:
                pass
            
            # Cache the data
            self.cached_data = {
                'cpu': cpu_percent,
                'memory': (memory_percent, memory_gb),
                'disk': (disk_percent, disk_gb),
                'temp': temp_text
            }
            self.last_update = current_time
            
            # Update labels
            self.cpu_label.text = f"CPU: {cpu_percent:.1f}%"
            self.memory_label.text = f"RAM: {memory_percent:.1f}% ({memory_gb:.1f}GB)"
            self.disk_label.text = f"Disk: {disk_percent:.1f}% ({disk_gb:.1f}GB)"
            self.temp_label.text = temp_text
                
        except Exception as e:
            print(f"System monitor update failed: {e}")
            # Use cached data if available
            if self.cached_data:
                self.cpu_label.text = f"CPU: {self.cached_data['cpu']:.1f}%"
                mem_pct, mem_gb = self.cached_data['memory']
                self.memory_label.text = f"RAM: {mem_pct:.1f}% ({mem_gb:.1f}GB)"
                disk_pct, disk_gb = self.cached_data['disk']
                self.disk_label.text = f"Disk: {disk_pct:.1f}% ({disk_gb:.1f}GB)"
                self.temp_label.text = self.cached_data['temp']
            else:
                self.cpu_label.text = f"Error: {e}" 