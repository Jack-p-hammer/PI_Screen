#!/usr/bin/env python3
"""
Test script to verify all widgets work properly
"""

def test_widget_imports():
    """Test that all widgets can be imported"""
    try:
        from widgets.weather import WeatherWidget
        print("✅ Weather widget imported successfully")
        
        from widgets.clock import ClockWidget
        print("✅ Clock widget imported successfully")
        
        from widgets.quote import QuoteWidget
        print("✅ Quote widget imported successfully")
        
        from widgets.finance import FinanceWidget
        print("✅ Finance widget imported successfully")
        
        from widgets.system_monitor import SystemMonitorWidget
        print("✅ System monitor widget imported successfully")
        
        from widgets.news import NewsWidget
        print("✅ News widget imported successfully")
        
        from widgets.calendar_widget import CalendarWidget
        print("✅ Calendar widget imported successfully")
        
        from widgets.coloredbox import ColoredBox
        print("✅ Colored box imported successfully")
        
        from widgets.config_manager import ConfigManager
        print("✅ Config manager imported successfully")
        
        from widgets.event_editor import EventEditor
        print("✅ Event editor imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_widget_creation():
    """Test that widgets can be instantiated"""
    try:
        from widgets.weather import WeatherWidget
        from widgets.clock import ClockWidget
        from widgets.quote import QuoteWidget
        from widgets.finance import FinanceWidget
        from widgets.system_monitor import SystemMonitorWidget
        from widgets.news import NewsWidget
        from widgets.calendar_widget import CalendarWidget
        
        # Test widget creation
        weather = WeatherWidget()
        print("✅ Weather widget created successfully")
        
        clock = ClockWidget()
        print("✅ Clock widget created successfully")
        
        quote = QuoteWidget()
        print("✅ Quote widget created successfully")
        
        finance = FinanceWidget("QQQ")
        print("✅ Finance widget created successfully")
        
        system_monitor = SystemMonitorWidget()
        print("✅ System monitor widget created successfully")
        
        news = NewsWidget()
        print("✅ News widget created successfully")
        
        calendar = CalendarWidget()
        print("✅ Calendar widget created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Widget creation error: {e}")
        return False

def test_psutil():
    """Test psutil functionality"""
    try:
        import psutil
        
        # Test basic psutil functions
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"✅ psutil working - CPU: {cpu_percent:.1f}%, RAM: {memory.percent:.1f}%, Disk: {disk.percent:.1f}%")
        return True
        
    except Exception as e:
        print(f"❌ psutil error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Raspberry Pi Dashboard Widgets")
    print("=" * 50)
    
    # Test imports
    print("\n📦 Testing widget imports...")
    imports_ok = test_widget_imports()
    
    # Test widget creation
    print("\n🔧 Testing widget creation...")
    creation_ok = test_widget_creation()
    
    # Test psutil
    print("\n💻 Testing psutil functionality...")
    psutil_ok = test_psutil()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"   Creation: {'✅ PASS' if creation_ok else '❌ FAIL'}")
    print(f"   psutil: {'✅ PASS' if psutil_ok else '❌ FAIL'}")
    
    if imports_ok and creation_ok and psutil_ok:
        print("\n🎉 All tests passed! Dashboard should work properly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.") 