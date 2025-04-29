import gi
import psutil
import signal
import time
import os
from datetime import timedelta

gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

"""Элементы"""
cpu_info = "ЦПУ"
ram_loading = "ОЗУ"
swap_loading = "Подкачка"
disk_loading = "Диск"
lan_speed = "Сеть"
uptime_label = "Время работы"
settings_label = "Настройки"
exit_app = "Выход"
apply_label = "Применить"
cancel_label = "Отмена"
time_update = 1

class SystemUsage:
    """Мониторинг ресурсов системы"""

    @staticmethod
    def get_cpu_temp():
        """Температура ЦПУ"""
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            return int(temps['coretemp'][0].current)
        return 0  # Возвращаем 0, если не можем получить температуру

    @staticmethod
    def get_cpu_usage():
        """Загрузка ЦПУ"""
        return psutil.cpu_percent()

    @staticmethod
    def get_ram_usage():
        """Загрузка ОЗУ"""
        memory = psutil.virtual_memory()
        return memory.used / (1024 ** 3), memory.total / (1024 ** 3)

    @staticmethod
    def get_swap_usage():
        """Загрузка подачки"""
        swap = psutil.swap_memory()
        return swap.used / (1024 ** 3), swap.total / (1024 ** 3)

    @staticmethod
    def get_disk_usage():
        """Диск"""
        disk = psutil.disk_usage('/')
        return disk.used / (1024 ** 3), disk.total / (1024 ** 3)

    @staticmethod
    def get_network_speed(prev_data):
        """Скорость сети"""
        net = psutil.net_io_counters()
        current_time = time.time()
        elapsed = current_time - prev_data['time']
        recv_speed = (net.bytes_recv - prev_data['recv']) / elapsed / 1024 / 1024
        sent_speed = (net.bytes_sent - prev_data['sent']) / elapsed / 1024 / 1024
        prev_data['recv'] = net.bytes_recv
        prev_data['sent'] = net.bytes_sent
        prev_data['time'] = current_time
        return recv_speed, sent_speed

    @staticmethod
    def get_uptime():
        """Время работы"""
        seconds = time.time() - psutil.boot_time()
        return str(timedelta(seconds=seconds)).split(".")[0]


class SettingsDialog(Gtk.Dialog):
    """Диалоговое окно настроек"""

    def __init__(self, parent, visibility_settings):
        super().__init__(title="Настройки отображения", transient_for=parent, flags=0)
        self.set_default_size(250, 200)
        self.add_buttons(cancel_label, Gtk.ResponseType.CANCEL, apply_label, Gtk.ResponseType.OK)
        self.visibility_settings = visibility_settings
        box = self.get_content_area()

        """Чекбоксы для каждого параметра"""
        self.cpu_check = Gtk.CheckButton(label=cpu_info)
        self.cpu_check.set_active(self.visibility_settings['cpu'])
        box.add(self.cpu_check)

        self.ram_check = Gtk.CheckButton(label=ram_loading)
        self.ram_check.set_active(self.visibility_settings['ram'])
        box.add(self.ram_check)

        self.swap_check = Gtk.CheckButton(label=swap_loading)
        self.swap_check.set_active(self.visibility_settings['swap'])
        box.add(self.swap_check)

        self.disk_check = Gtk.CheckButton(label=disk_loading)
        self.disk_check.set_active(self.visibility_settings['disk'])
        box.add(self.disk_check)

        self.net_check = Gtk.CheckButton(label=lan_speed)
        self.net_check.set_active(self.visibility_settings['net'])
        box.add(self.net_check)

        self.uptime_check = Gtk.CheckButton(label=uptime_label)
        self.uptime_check.set_active(self.visibility_settings['uptime'])
        box.add(self.uptime_check)

        self.show_all()


class SystemTrayApp:
    """Приложение для системного трея"""

    def __init__(self):
        self.indicator = appindicator.Indicator.new("system_monitor", "", appindicator.IndicatorCategory.SYSTEM_SERVICES)
        icon_path = os.path.join(os.path.dirname(__file__), "logo.png")
        self.indicator.set_icon_full(icon_path, "System Monitor")
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # Настройки видимости элементов
        self.visibility_settings = {
            'cpu': True,
            'ram': True,
            'swap': True,
            'disk': True,
            'net': True,
            'uptime': True
        }

        self.menu = Gtk.Menu()  # Создание меню

        """Элементы меню"""
        self.cpu_temp_item = Gtk.MenuItem(label=f"{cpu_info}: N/A")
        self.ram_item = Gtk.MenuItem(label=f"{ram_loading}: N/A")
        self.swap_item = Gtk.MenuItem(label=f"{swap_loading}: N/A")
        self.disk_item = Gtk.MenuItem(label=f"{disk_loading}: N/A")
        self.net_item = Gtk.MenuItem(label=f"{lan_speed}: N/A")
        self.uptime_item = Gtk.MenuItem(label=f"{uptime_label}: N/A")
        self.separator = Gtk.SeparatorMenuItem()  # Разделитель
        self.settings_item = Gtk.MenuItem(label=settings_label)
        self.quit_item = Gtk.MenuItem(label=exit_app)

        self.update_menu_visibility()  # Добавляем элементы в меню с учетом настроек видимости

        """Обработчики событий"""
        self.settings_item.connect("activate", self.show_settings)
        self.quit_item.connect("activate", self.quit)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        self.prev_net_data = {
            'recv': psutil.net_io_counters().bytes_recv,
            'sent': psutil.net_io_counters().bytes_sent,
            'time': time.time()
        }

    def update_menu_visibility(self):
        """Обновляет видимость элементов меню в соответствии с настройками"""
        for item in self.menu.get_children():
            self.menu.remove(item)

        if self.visibility_settings['cpu']:
            self.menu.append(self.cpu_temp_item)

        if self.visibility_settings['ram']:
            self.menu.append(self.ram_item)

        if self.visibility_settings['swap']:
            self.menu.append(self.swap_item)

        if self.visibility_settings['disk']:
            self.menu.append(self.disk_item)

        if self.visibility_settings['net']:
            self.menu.append(self.net_item)

        if self.visibility_settings['uptime']:
            self.menu.append(self.uptime_item)

        self.menu.append(self.separator)
        self.menu.append(self.settings_item)
        self.menu.append(self.quit_item)

        self.menu.show_all()  # Обновляем отображение меню

    def show_settings(self, widget):
        """Показывает диалог настроек"""
        dialog = SettingsDialog(None, self.visibility_settings)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            """Обновляем настройки видимости"""
            self.visibility_settings['cpu'] = dialog.cpu_check.get_active()
            self.visibility_settings['ram'] = dialog.ram_check.get_active()
            self.visibility_settings['swap'] = dialog.swap_check.get_active()
            self.visibility_settings['disk'] = dialog.disk_check.get_active()
            self.visibility_settings['net'] = dialog.net_check.get_active()
            self.visibility_settings['uptime'] = dialog.uptime_check.get_active()

            self.update_menu_visibility()  # Обновляем меню

        dialog.destroy()

    def update_info(self):
        """Обновление информации в меню"""
        cpu_temp = SystemUsage.get_cpu_temp()
        cpu_usage = SystemUsage.get_cpu_usage()
        ram_used, ram_total = SystemUsage.get_ram_usage()
        disk_used, disk_total = SystemUsage.get_disk_usage()
        swap_used, swap_total = SystemUsage.get_swap_usage()
        net_recv_speed, net_sent_speed = SystemUsage.get_network_speed(self.prev_net_data)
        uptime = SystemUsage.get_uptime()

        """Обновляем только видимые элементы"""
        if self.visibility_settings['cpu']:
            self.cpu_temp_item.set_label(f"{cpu_info}: {cpu_usage:.0f}%  🌡{cpu_temp}°C")

        if self.visibility_settings['ram']:
            self.ram_item.set_label(f"{ram_loading}: {ram_used:.1f}/{ram_total:.1f} GB")

        if self.visibility_settings['swap']:
            self.swap_item.set_label(f"{swap_loading}: {swap_used:.1f}/{swap_total:.1f} GB")

        if self.visibility_settings['disk']:
            self.disk_item.set_label(f"{disk_loading}: {disk_used:.1f}/{disk_total:.1f} GB")

        if self.visibility_settings['net']:
            self.net_item.set_label(f"{lan_speed}: ↓{net_recv_speed:.1f}/↑{net_sent_speed:.1f} MB/s")

        if self.visibility_settings['uptime']:
            self.uptime_item.set_label(f"{uptime_label}: {uptime}")

        """Обновляем в трее (CPU и RAM)"""
        tray_text = ""
        if self.visibility_settings['cpu']:
            tray_text += f"  {cpu_info}: {cpu_usage:.0f}%"
        if self.visibility_settings['ram']:
            tray_text += f"  {ram_loading}: {ram_used:.1f}GB"

        self.indicator.set_label(tray_text, "")

        return True

    def quit(self, *args):
        """Завершение работы приложения"""
        Gtk.main_quit()

    def run(self):
        """Запуск основного цикла"""
        GLib.timeout_add_seconds(time_update, self.update_info)  # Обновление каждую секунду
        Gtk.main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = SystemTrayApp()
    app.run()
