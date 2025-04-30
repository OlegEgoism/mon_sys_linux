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
Посмотрите, как OFF_RES работает на практике:
[![OFF_RES Видео-демо](https://img.youtube.com/vi/AVzxt623t2A/0.jpg)](https://www.youtube.com/watch?v=lcWTL0O7paI)

-  ЗАПУСК В РЕЖИМИ РАЗАРБОТКИ.

📁 Установка apt для Debian/Ubuntu (основные библиотеки).
```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```
📁 Python-зависимости.
```bash
pip install -r requirements.txt
```

📁 Дополнительно (для GNOME Shell).
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