🔌 MON_SYS
- 🇧🇾 Небольшое приложение, отображающее загрузку системных ресурсов в системном трее 🇧🇾 
 
🧾 Основные функции:
- Мониторинг CPU: загрузка и температура процессора.
- Мониторинг RAM: объём используемой оперативной памяти.
- Swap и диск: отображение использования подкачки и диска.
- Скорость сети: приём и передача данных в MB/s.
- Время работы системы (Uptime).

📝 Вся информация записывается в логи. Логи находятся в корне диска /home (Домашняя папка)

🎥 Видео-демо
[![Watch the video](https://img.youtube.com/vi/lcWTL0O7paI/maxresdefault.jpg)](https://www.youtube.com/watch?v=lcWTL0O7paI)

-  ЗАПУСК В РЕЖИМИ РАЗАРБОТКИ.

💡 Установка apt для Debian/Ubuntu (основные библиотеки).
```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
sudo apt install -y build-essential libgirepository1.0-dev gir1.2-glib-2.0 python3-gi python3-gi-cairo gobject-introspection

```
Если буду проблемы добавить
```bash
sudo apt update
sudo apt install python3.10-dev
sudo apt install pkg-config
sudo apt install libcairo2-dev
sudo apt install build-essential
pip install pygobject
```

💡 Python-зависимости.
```bash
pip install -r requirements.txt
```

💡 Дополнительно (для GNOME Shell).
```bash
sudo apt install gnome-shell-extension-appindicator
```

💡 Запуск
```bash
python3 app.py
```

-  СБОРКА ПРИЛОЖЕНИЯ КАК УСТАНОВОЧНЫЙ ПАКЕТ.

💡 Запуск как пакет приложения
```bash
chmod +x build_deb.sh
./build_deb.sh
sudo dpkg -i deb_build/mon-sys.deb
```
💡 Сделай исполняемым:
```bash
chmod +x build_deb.sh
```

💡 Запуск
```bash
./build_deb.sh
```

💡 Установи пакет
```bash
sudo dpkg -i deb_build/mon-sys.deb
```

По вопросам писать на почту 📨: olegpustovalov220@gmail.com 