#!/usr/bin/env python3
"""
Performance monitoring script for the Raspberry Pi Dashboard
"""

import psutil
import time
import threading
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.monitoring = True
        self.stats = []
        
    def start_monitoring(self):
        """Start monitoring system performance"""
        print("🔍 Starting performance monitoring...")
        print("Press Ctrl+C to stop monitoring")
        print("-" * 60)
        
        try:
            while self.monitoring:
                # Get system stats
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Get process stats for Python
                python_processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        if 'python' in proc.info['name'].lower():
                            python_processes.append(proc.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                # Calculate total Python CPU and memory usage
                total_python_cpu = sum(p['cpu_percent'] for p in python_processes)
                total_python_memory = sum(p['memory_percent'] for p in python_processes)
                
                # Record stats
                stat = {
                    'timestamp': datetime.now(),
                    'cpu_total': cpu_percent,
                    'cpu_python': total_python_cpu,
                    'memory_total': memory.percent,
                    'memory_python': total_python_memory,
                    'disk_usage': disk.percent,
                    'python_processes': len(python_processes)
                }
                self.stats.append(stat)
                
                # Display current stats
                print(f"[{stat['timestamp'].strftime('%H:%M:%S')}] "
                      f"CPU: {cpu_percent:5.1f}% (Python: {total_python_cpu:5.1f}%) | "
                      f"RAM: {memory.percent:5.1f}% (Python: {total_python_memory:5.1f}%) | "
                      f"Disk: {disk.percent:5.1f}% | "
                      f"Python processes: {len(python_processes)}")
                
                time.sleep(5)  # Update every 5 seconds
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            self.print_summary()
    
    def print_summary(self):
        """Print performance summary"""
        if not self.stats:
            print("No data collected")
            return
            
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 60)
        
        # Calculate averages
        avg_cpu = sum(s['cpu_total'] for s in self.stats) / len(self.stats)
        avg_cpu_python = sum(s['cpu_python'] for s in self.stats) / len(self.stats)
        avg_memory = sum(s['memory_total'] for s in self.stats) / len(self.stats)
        avg_memory_python = sum(s['memory_python'] for s in self.stats) / len(self.stats)
        
        # Find peaks
        max_cpu = max(s['cpu_total'] for s in self.stats)
        max_cpu_python = max(s['cpu_python'] for s in self.stats)
        max_memory = max(s['memory_total'] for s in self.stats)
        max_memory_python = max(s['memory_python'] for s in self.stats)
        
        print(f"Monitoring duration: {len(self.stats) * 5} seconds")
        print(f"Data points collected: {len(self.stats)}")
        print()
        print("📈 AVERAGE USAGE:")
        print(f"  CPU Total:     {avg_cpu:5.1f}%")
        print(f"  CPU Python:    {avg_cpu_python:5.1f}%")
        print(f"  Memory Total:  {avg_memory:5.1f}%")
        print(f"  Memory Python: {avg_memory_python:5.1f}%")
        print()
        print("📊 PEAK USAGE:")
        print(f"  CPU Total:     {max_cpu:5.1f}%")
        print(f"  CPU Python:    {max_cpu_python:5.1f}%")
        print(f"  Memory Total:  {max_memory:5.1f}%")
        print(f"  Memory Python: {max_memory_python:5.1f}%")
        
        # Performance recommendations
        print("\n💡 RECOMMENDATIONS:")
        if avg_cpu_python > 20:
            print("  ⚠️  Python processes using high CPU - consider reducing update frequency")
        if avg_memory_python > 15:
            print("  ⚠️  Python processes using high memory - check for memory leaks")
        if avg_cpu_total > 80:
            print("  ⚠️  High overall CPU usage - system may be overloaded")
        if avg_memory_total > 90:
            print("  ⚠️  High memory usage - consider closing other applications")
        
        if avg_cpu_python < 10 and avg_memory_python < 10:
            print("  ✅ Performance looks good!")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False

def main():
    monitor = PerformanceMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    main() 