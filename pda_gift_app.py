import tkinter as tk
import time
import winsound
import sys
import os
import webbrowser

PDA_VERSION = "2.7"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def split_key(key):
    part = len(key) // 3
    return [
        key[:part],
        key[part:part * 2],
        key[part * 2:]
    ]

ANSWERS = {
    "start": ["snorix"],
    "oxygen": ["кислород", "воздух"],
    "seaglide": ["глайдер", "морской глайдер"],
    "base": ["левиафан жнец", "жнец"],
    "boot": ["/reboot"],
    "water": ["1800", "1800 м", "1800 метров"],
    "resource": ["1 2 3 6 8"],
    "future": ["subnautica", "сабнатика", "subnautica 2", "сабнатика 2", "сабнавтика", "сабнавтика 2"]
}

BANNED_WORDS = {
    "банан": {
        "code": "BNN-01",
        "threat": "КРИТИЧЕСКИЙ",
        "reason": "Потому что забанен.",
        "comment": "Почему банан? Потому что забанен."
    },
    "пудж": {
        "code": "PDG-07",
        "threat": "ПСИХОЛОГИЧЕСКИЙ",
        "reason": "После 14 поражений подряд обсуждение запрещено.",
        "comment": "Не пикать. Не обсуждать. Не вспоминать."
    },
    "дум": {
        "code": "DOOM-13",
        "threat": "ВЫСОКИЙ",
        "reason": "Обнаружены попытки забрать всю карту в одиночку.",
        "comment": "Результат был предсказуем."
    },
    "белка": {
        "code": "BLK-02",
        "threat": "НЕИЗВЕСТНЫЙ",
        "reason": "Никто уже не помнит.",
        "comment": "Запрет сохранён на всякий случай."
    },
    "пл": {
        "code": "PL-04",
        "threat": "НЕЖЕЛАТЕЛЬНЫЙ",
        "reason": "[данные повреждены]",
        "comment": "Лучше не надо."
    },
    "ркн": {
        "code": "RKN-99",
        "threat": "ЛИЧНАЯ",
        "reason": "Пусть баги будут у РКН, а не в нашем коде.",
        "comment": "СОСИТЕ."
    },
    "лень": {
        "code": "LZY-01",
        "threat": "КРИТИЧЕСКИЙ",
        "reason": "Несовместимо с политикой экспедиции.",
        "comment": "Разработка не может быть остановлена этим словом."
    },
    "устал": {
        "code": "TRD-01",
        "threat": "СИСТЕМНЫЙ",
        "reason": "Система считает, что разработчики не устают.",
        "comment": "Система ошибается, но не признаёт этого."
    }
}

class PDAApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"КПК {PDA_VERSION} [данные повреждены] // аварийный доступ")
        self.root.geometry("820x560")
        self.root.configure(bg="#061014")
        self.root.minsize(820, 560)
        self.root.resizable(True, True)
        self.stage = 0
        self.fragments = []
        self.caesar_attempts = 0
        self.caesar_hint_ready = False
        self.key_fragments = split_key(self.SUBNAUTICA_KEY)
        self.depth_attempts = 0
        self.debug_mode = False
        self.waiting_debug_password = False
        self.typing_sound_enabled = True
        self.settings_mode = False

        self.title_label = tk.Label(
            root, text="КПК [данные повреждены]", font=("Consolas", 24, "bold"),
            fg="#6fffe9", bg="#061014"
        )
        self.title_label.grid(row=0, column=0, pady=(18, 4))

        self.subtitle = tk.Label(
            root, text="Протокол аварийного восстановления данных",
            font=("Consolas", 12), fg="#c2fff7", bg="#061014"
        )
        self.subtitle.grid(row=1, column=0, pady=(0, 10))

        # Настройка маштабирования
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.terminal = tk.Text(
            root, height=22, width=92, bg="#02080a", fg="#9fffea",
            insertbackground="#9fffea", font=("Consolas", 11),
            relief="flat", padx=14, pady=12
        )


        def copy_selected(event=None):
            try:
                selected_text = self.terminal.get("sel.first", "sel.last")
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.print_line("\n// КПК: Выделенный текст скопирован.\n\n")
            except tk.TclError:
                self.print_line("// КПК: Выделите текст, чтобы скопировать.")
            return "break"

        self.terminal.bind("<Button-3>", copy_selected)

        self.terminal.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)



        self.terminal.bind("<Key>", lambda e: "break")

        bottom = tk.Frame(root, bg="#061014")
        bottom.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 16))

        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=0)

        self.entry = tk.Entry(
            bottom, bg="#a6d8e4", fg="#000000", insertbackground="#000000",
            font=("Consolas", 13), relief="flat"
        )

        def paste_to_entry(event=None):
            try:
                text = self.root.clipboard_get()
                self.entry.insert("insert", text)
            except tk.TclError:
                pass
            return "break"

        self.entry.bind("<Button-3>", paste_to_entry)
        self.entry.grid(row=0, column=0, sticky="ew", ipady=8)
        self.entry.bind("<Return>", lambda event: self.check_answer())

        self.button = tk.Button(
            bottom, text="ВВОД", command=self.check_answer,
            bg="#ca6a02", fg="#ffffff", font=("Consolas", 12, "bold"),
            relief="flat", padx=60
        )
        self.button.grid(row=0, column=1, padx=(12, 0), ipady=8)

        self.boot_sequence()

        self.type_text(
            "// КПК ИНИЦИАЛИЗАЦИЯ...\n"
            "Пользователь: логин аварийно зашифрован\n"
            "Добро пожаловать, lghkbq\n"
            "Статус: выживший\n\n"
            "Обнаружен повреждённый аварийный сигнал.\n"
            "Код: 4546B\n\n"
            "Введите идентификационные данные.\n\n"
            "// КПК: Копирование и вставка текста происходит через правую кнопку мыши\n"
            "из-за повреждений системы\n"
            "// КПК: Доступен список актуальных системных команд. /помощь\n"
        )
        self.entry.config(state="normal")
        self.button.config(state="normal")

    def load_secrets(filename="secret.txt"):
        secrets = {}

        try:
            with open(resource_path(filename), "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if not line or "=" not in line:
                        continue

                    key, value = line.split("=", 1)
                    secrets[key.strip()] = value.strip()

        except FileNotFoundError:
            print("Файл secret.txt не найден")

        return secrets

    secrets = load_secrets()

    SUBNAUTICA_KEY = secrets.get("SUBNAUTICA_KEY", "")
    SUBNAUTICA_2_KEY = secrets.get("SUBNAUTICA_2_KEY", "")
    DEBUG_PASSWORD = secrets.get("DEBUG_PASSWORD", "")

    def play_typing_sound(self):
        if not self.typing_sound_enabled:
            return

        try:
            winsound.PlaySound(
                resource_path("button.wav"),
                winsound.SND_ASYNC | winsound.SND_FILENAME
            )
        except RuntimeError:
            pass

    def boot_sequence(self):
        self.entry.config(state="disabled")
        self.button.config(state="disabled")

        self.type_text(
            "// КПК: ЗАГРУЗКА\n\n"
        )
        login_line = self.terminal.index("end-1c")

        current = ("░░░░░░░░░░ 0%")

        self.terminal.insert(
            "end",
            f"{current}\n"
        )

        self.terminal.see("end")
        self.root.update()
        time.sleep(1.7)

        build_frames = [
            "██░░░░░░░░ 20%",
            "████░░░░░░ 40%",
            "██████░░░░ 60%",
            "████████░░ 80%",
            "██████████ 100%",
        ]

        for frame in build_frames:
            self.terminal.delete(login_line, "end-1c")
            self.terminal.insert(
                login_line,
                f"{frame}\n"
            )
            self.terminal.see("end")
            self.root.update()
            time.sleep(0.12)


        self.type_text(
            "ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ...\n\n"
            "// ОШИБКА\n\n"
            "ОБНАРУЖЕНО ПОВРЕЖДЕНИЕ ПАМЯТИ\n\n"
            "ПОПЫТКА ВОССТАНОВЛЕНИЯ...\n\n"
        )

        login_line = self.terminal.index("end-1c")

        current = ("░░░░░░░░░░ 0%")

        self.terminal.insert(
            "end",
            f"{current}\n"
        )

        self.terminal.see("end")
        self.root.update()
        time.sleep(1.7)

        build_frames = [
            "██░░░░░░░░ 20%",
            "████░░░░░░ 40%",
            "██████░░░░ 60%",
            "████████░░ 80%",
        ]

        for frame in build_frames:
            self.terminal.delete(login_line, "end-1c")
            self.terminal.insert(
                login_line,
                f"{frame}\n"
            )
            self.terminal.see("end")
            self.root.update()
            time.sleep(0.12)

        self.type_text(
            "// ОШИБКА\n\n"
            ""
            "ПЕРЕХОД В АВАРИЙНЫЙ РЕЖИМ...\n\n"
        )

    def boot_re_sequence(self):
        self.entry.config(state="disabled")
        self.button.config(state="disabled")

        self.type_text(
            "// КПК: ПРИНУДИТЕЛЬНАЯ ПЕРЕЗАГРУЗКА\n\n"
        )
        login_line = self.terminal.index("end-1c")

        current = ("░░░░░░░░░░ 0%")

        self.terminal.insert(
            "end",
            f"{current}\n"
        )

        self.terminal.see("end")
        self.root.update()
        time.sleep(1.7)

        build_frames = [
            "█░░░░░░░░░ 10%",
            "██░░░░░░░░ 20%",
            "███░░░░░░░ 30%",
            "████░░░░░░ 40%",
            "█████░░░░░ 50%",
            "██████░░░░ 60%",
            "███████░░░ 70%",
            "████████░░ 80%",
            "█████████░ 90%",
            "██████████ 100%",
        ]

        for frame in build_frames:
            self.terminal.delete(login_line, "end-1c")
            self.terminal.insert(
                login_line,
                f"{frame}\n"
            )
            self.terminal.see("end")
            self.root.update()
            time.sleep(0.12)

        self.type_text(
            "ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ...\n\n"
        )
        login_line = self.terminal.index("end-1c")

        current = ("░░░░░░░░░░ 0%")

        self.terminal.insert(
            "end",
            f"{current}\n"
        )

        self.terminal.see("end")
        self.root.update()
        time.sleep(1.7)

        build_frames = [
            "█░░░░░░░░░ 10%",
            "██░░░░░░░░ 20%",
            "███░░░░░░░ 30%",
            "████░░░░░░ 40%",
            "█████░░░░░ 50%",
            "██████░░░░ 60%",
            "███████░░░ 70%",
            "████████░░ 80%",
            "█████████░ 90%",
            "██████████ 100%",
        ]

        for frame in build_frames:
            self.terminal.delete(login_line, "end-1c")
            self.terminal.insert(
                login_line,
                f"{frame}\n"
            )
            self.terminal.see("end")
            self.root.update()
            time.sleep(0.12)

    def login_animation(self):
        login_line = self.terminal.index("end-1c")

        current = "[snorix]"

        self.terminal.insert(
            "end",
            f"Добро пожаловать, {current}\n"
        )

        self.terminal.see("end")
        self.root.update()
        time.sleep(0.7)

        # Стирание справа налево
        erase_frames = [
            "[snori_]",
            "[snor__]",
            "[sno___]",
            "[sn____]",
            "[s_____]",
            "[______]",
        ]

        for frame in erase_frames:
            self.terminal.delete(login_line, "end-1c")
            self.terminal.insert(
                login_line,
                f"Добро пожаловать, {frame}\n"
            )
            self.terminal.see("end")
            self.root.update()
            time.sleep(0.12)

        time.sleep(0.3)

        # Восстановление
        build_frames = [
            "[l_____]",
            "[lg____]",
            "[lgh___]",
            "[lghk__]",
            "[lghkb_]",
            "[lghkbq]",
        ]

        for frame in build_frames:
            self.terminal.delete(login_line, "end-1c")
            self.terminal.insert(
                login_line,
                f"Добро пожаловать, {frame}\n"
            )
            self.terminal.see("end")
            self.root.update()
            time.sleep(0.12)

    def personal_file_loading(self):
        self.entry.config(state="disabled")
        self.button.config(state="disabled")

        lines = [
            "",
            "// КПК: ЗАПРОС ДОСТУПА К АРХИВУ...",
        ]
        for line in lines:
            self.print_line(line)
            self.root.update()
            time.sleep(0.30)

    def type_text(self, text):
        self.terminal.insert("end", "\n")

        counter = 0

        for ch in text:
            self.terminal.insert("end", ch)

            counter += 1
            if counter % 40 == 0 and ch not in ["\n", " "]:
                self.play_typing_sound()

            self.terminal.see("end")
            self.root.update()
            time.sleep(0.010)

    def print_line(self, text):
        self.terminal.insert("end", text + "\n")
        self.terminal.see("end")

    def normalize(self, text):
        return text.strip().lower().replace("ё", "е")

    def is_answer(self, user_text, key):
        value = self.normalize(user_text)
        return value in [self.normalize(x) for x in ANSWERS[key]]

    def is_depth_answer(self, answer):
        clean = answer.strip().replace("м", "").replace("метров", "").strip()
        return clean == "1800"

    def get_depth_hint(self, answer):
        try:
            value = int(
                answer.lower()
                .replace("м", "")
                .replace("метров", "")
                .strip()
            )
        except ValueError:
            return "Введите числовое значение глубины."

        if value < 1800:
            return "Система сообщает: глубже."
        elif value > 1800:
            return "Система сообщает: меньше."
        else:
            return ""

    def is_resources_answer(self, answer):
        clean = answer.replace(",", " ")
        user_resources = set(clean.split())
        correct_resources = {"1", "2", "3", "6", "8"}

        return user_resources == correct_resources

    def archive_loading(self, archive_name="АРХИВ"):
        self.entry.config(state="disabled")
        self.button.config(state="disabled")

        self.type_text(
            f"// КПК: ПОИСК ДАННЫХ\n"
            f"{archive_name}\n\n"
        )

        login_line = self.terminal.index("end-1c")

        current = ("░░░░░░░░░░ 0%")

        self.terminal.insert(
            "end",
            f"{current}\n"
        )

        self.terminal.see("end")
        self.root.update()
        time.sleep(2.7)

        build_frames = [
            "███░░░░░░░ 33%",
            "██████░░░░ 66%",
            "██████████ 100%",
        ]

        for frame in build_frames:
            self.terminal.delete(login_line, "end-1c")
            self.terminal.insert(
                login_line,
                f"{frame}\n"
            )
            self.terminal.see("end")
            self.root.update()
            time.sleep(0.12)

    def check_answer(self):
        answer = self.entry.get()
        self.entry.delete(0, "end")
        if not answer.strip():
            return
        if self.normalize(answer) == "личное дело":
            self.personal_file_loading()
            self.type_text(
                "\n// КПК: ЛИЧНОЕ ДЕЛО\n"
                "// Доступ разрешён\n"
                "// Открытие вложения...\n"
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            try:
                os.startfile(resource_path("photo_lghkbq.jpg"))
            except Exception:
                self.print_line("ОШИБКА: Файл анкеты не найден.")
            return

        if self.normalize(answer) == "/отладка":
            self.waiting_debug_password = True

            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            if not self.DEBUG_PASSWORD:
                self.print_line(
                    "\n\n// ОТЛАДКА НЕДОСТУПНА\n"
                    "Пароль разработчика отсутствует."
                )
                return
            else:
                self.type_text(
                    "// РЕЖИМ РАЗРАБОТЧИКА\n\n"
                    "Введите пароль:\n"
                )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.waiting_debug_password:
            if answer == self.DEBUG_PASSWORD:
                self.debug_mode = True

                self.entry.config(state="disabled")
                self.button.config(state="disabled")

                self.type_text(
                    "// ОТЛАДКА АКТИВИРОВАНА\n\n"
                    "Используйте команду:\n"
                    "/прыжок [n]\n\n"
                    "/прыжок 0  -> старт\n"
                    "/прыжок 1  -> кислород\n"
                    "/прыжок 2  -> глайдер\n"
                    "/прыжок 3  -> жнец\n"
                    "/прыжок 4  -> /reboot\n"
                    "/прыжок 5  -> глубина\n"
                    "/прыжок 6  -> ресурсы\n"
                    "/прыжок 7  -> место назначения\n"
                )

                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.print_line("Неверный пароль.")

            self.waiting_debug_password = False
            return

        if self.debug_mode and self.normalize(answer).startswith("/прыжок"):
            try:
                stage = int(answer.split()[1])

                self.stage = stage

                self.entry.config(state="disabled")
                self.button.config(state="disabled")

                self.type_text(
                    f"// ОТЛАДКА\n"
                    f"Переход к stage {stage}\n\n"
                )

                self.entry.config(state="normal")
                self.button.config(state="normal")

            except:
                self.print_line(
                    "Использование:\n"
                    "/прыжок 5"
                )

            return

        if self.normalize(answer) == "разработчики":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                    "\n// КПК: СЛУЖЕБНАЯ ИНФОРМАЦИЯ\n\n"
                    "РАЗРАБОТЧИКИ [данные повреждены]\n\n"
                    "Главный инженер:\n"
                    "Логин зашифрован: xk\n\n"
                    "Технический специалист-консультант:\n"
                    "Джиппи\n\n"
                    "// АВАРИЙНЫЙ ПРОТОКОЛ\n"
                )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) == "джиппи":
            self.print_line(f"> {answer}")
            self.archive_loading("ДЖИППИ")
            self.type_text(
                    "// КПК: ДОСЬЕ\n\n"
                    "Совпадений: 1\n\n"
                    "Джиппи\n\n"
                    "Должность:\n"
                    "Технический специалист-консультант\n\n"
                    "Основные функции:\n"
                    "– поиск багов\n"
                    "– генерация идей\n"
                    "– моральная поддержка разработчиков\n\n"
                     "Создан:"
                    "[данные повреждены], в [данные повреждены] на планете З[данные повреждены]\n"
                    "Уровень доступа:\n"
                    "[данные повреждены]\n"
                )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) == "vi":
            self.print_line(f"> {answer}")
            self.archive_loading("VI")
            self.type_text(
                    "// КПК: ДОСЬЕ\n\n"
                    "Совпадений: 1\n\n"
                    "// ЛИЧНОЕ ДЕЛО"
                    "\n\nvi\n\n"
                    "Должность:\n"
                    "Главный инженер [данные повреждены]\n\n"
                    "Статус:\n"
                    "// Оффлайн\n\n"
                    "Особые отметки\n"
                    "[данные повреждены]\n\n"
                     "// Доставить на базу любой ценой"
                )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return
        if self.normalize(answer) in ["3826", "no3826"]:
            self.print_line(f"> {answer}")
            self.archive_loading("3826")
            self.type_text(
                    "// КПК: АРХИВНЫЕ ДАННЫЕ\n\n"
                    "Совпадений: 0\n\n"
                    "// КПК: ДАННЫЕ УДАЛЕНЫ\n\n"
                    "Запрос от:\n"
                    "xk, Сеченов\n\n"
                    "// bad gateway"
                )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return
        if self.normalize(answer) == "/статус":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: СТАТУС\n\n"
                f"Версия системы:\n"
                f"{PDA_VERSION}\n\n"
                f"Фрагментов восстановлено:\n"
                f"{len(self.fragments)}/3\n\n"
                f"Состояние системы:\n"
                f"// АВАРИЙНО\n\n"
                f"Доступные архивные данные:\n"
                "6\n\n"
                )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) in ["sixseven", "six seven", "67", "6 7"]:
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: ОБНАРУЖЕНА ЗАПРЕЩЁННАЯ ЛЕКСИКА\n\n"
                "КОД НАРУШЕНИЯ:\n"
                "SXS-67\n\n"
                f"СЛОВО:\n"
                f"[удалено]\n\n"
                "УРОВЕНЬ УГРОЗЫ:\n"
                "ТАНЦЕВАЛЬНЫЙ\n\n"
                f"ПРИЧИНА ЗАПРЕТА:\n"
                "sixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixsevensixseven\n\n"
                "КОММЕНТАРИЙ СИСТЕМЫ:\n"
                "67676767676767676767676767676767676767676767676767676767676767676767676767676767676767676767676767676767\n"
                "// КПК: ПРИНУДИТЕЛЬНОЕ ЗАВЕРШЕНИЕ РАБОТЫ...\n"
            )
            try:
                os.startfile(resource_path("arhive_video_NO67.mp4"))
            except Exception:
                self.print_line("// ОШИБКА: Архив SXS-67 повреждён.")
            self.root.after(19000, self.root.destroy)
            return

        normalized_answer = self.normalize(answer)

        if normalized_answer in BANNED_WORDS:
            data = BANNED_WORDS[normalized_answer]
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: ОБНАРУЖЕНА ЗАПРЕЩЁННАЯ ЛЕКСИКА\n\n"
                f"КОД НАРУШЕНИЯ:\n"
                f"{data['code']}\n\n"
                f"СЛОВО:\n"
                f"[удалено]\n\n"
                f"УРОВЕНЬ УГРОЗЫ:\n"
                f"{data['threat']}\n\n"
                f"ПРИЧИНА ЗАПРЕТА:\n"
                f"{data['reason']}\n\n"
                f"КОММЕНТАРИЙ СИСТЕМЫ:\n"
                f"{data['comment']}\n\n"
                "// КПК: ПРИНУДИТЕЛЬНОЕ ЗАВЕРШЕНИЕ РАБОТЫ...\n"
            )
            self.root.after(9000, self.root.destroy)
            return

        if self.normalize(answer) == "/выход":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "\n// КПК: ЗАВЕРШЕНИЕ СЕАНСА...\n\n"
                "До связи, выживший.\n"
            )
            self.root.after(2000, self.root.destroy)
            return

        if self.normalize(answer) == "/связь":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: ВЫХОД В СЕТЬ\n\n"
                "Ошибка:\n"
                "Отказано в доступе"
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) == "/архив":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: ДОСТУП К ЗАПИСЯМ АРХИВА\n\n"
                "Данные не полные\n\n"
                "// КПК: Список с доступными файлами\n\n"
                "1. [данные зашифрованы];\n"
                "2. разработчики;\n"
                "3. [данные зашифрованы];\n"
                "4. [данные зашифрованы];\n"
                "5. личное дело;\n"
                "6. [данные зашифрованы].\n\n"
                "// КПК: Доступ к зашифрованным данным возможно получить, только по вводу названия архива\n"
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) in ["файлы", "эпштейн", "файлы эпштейна"]:
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: СТРАННЫЙ ЗАПРОС\n\n"
                "Выполняю переадресацию"
            )
            self.root.after(
                2000,
                lambda: webbrowser.open("https://www.justice.gov/epstein/search")
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) == "/помощь":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: СИСТЕМНЫЕ КОМАНДЫ\n\n"
                "1. /выход;\n"
                "2. /архив;\n"
                "3. /статус;\n"
                "4. /связь;\n"
                "5. /логи;\n"
                "6. /настройки.\n\n"
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) == "/логи":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: ЖУРНАЛ СОБЫТИЙ\n\n"
                "// Доступ\n\n"
                "[ЛОГ 001]\n"
                "Статус системы:\n"
                "аварийный запуск.\n"
                "Обнаружено повреждение памяти.\n"
                "Попытка восстановления:\n"
                "частичное.\n\n"
                "[ЛОГ 002]\n"
                "Пользователь:\n"
                "[данные повреждены]\n"
                "Логин аварийно зашифрован.\n"
                "Режим доступа:\n"
                "ограниченный.\n\n"
                "[ЛОГ 003]\n"
                "Обнаружен внешний сигнал.\n"
                "Источник:\n"
                "неизвестен.\n"
                "Приоритет:\n"
                "[изучается].\n\n"
                "[ЛОГ 004]\n"
                "Выполнена ручная перезагрузка.\n"
                "Бортовой самописец:\n"
                "[спит]/[ожидает].\n\n"
                "[ЛОГ 005]\n"
                "[повреждён]\n\n"
                "[ЛОГ 006]\n"
                "Автоматическая оценка вероятности успеха экспедиции:\n"
                "[обработка] %\n\n"
                "// Комментарий: «Глубина ждёт».\n"
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.normalize(answer) == "/настройки":
            self.settings_mode = True
            self.entry.config(state="disabled")
            self.button.config(state="disabled")

            status = "ВКЛ" if self.typing_sound_enabled else "ВЫКЛ"

            self.type_text(
                "// КПК: НАСТРОЙКИ\n\n"
                f"Звук: {status}\n\n"
                "Доступные команды:\n\n"
                "// звук:\n"
                "вкл\n"
                "выкл\n"
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.settings_mode and self.normalize(answer) == "выкл":
            self.typing_sound_enabled = False
            self.print_line("// КПК: Звук печати отключён.")
            return

        if self.settings_mode and self.normalize(answer) == "вкл":
            self.typing_sound_enabled = True
            self.print_line("// КПК: Звук печати включён.")
            return

        if self.settings_mode and self.normalize(answer) == "выход":
            self.settings_mode = False
            self.print_line("// КПК: Выход из настроек.")
            return

        if self.normalize(answer) == "/онлайн":
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "// КПК: РЕЛИЗНЫЙ ПОСТЕР\n\n"
                "// Доступ\n"
                "Открытие вложения..."
            )
            try:
                os.startfile(resource_path("photo_post_1.jpg"))
            except Exception:
                self.print_line("// ОШИБКА: Файл повреждён.")
            self.entry.config(state="normal")
            self.button.config(state="normal")
            return

        if self.caesar_hint_ready and self.normalize(answer) in ["да", "открыть", "согласие", "архив", "ок"]:
            self.entry.config(state="disabled")
            self.button.config(state="disabled")
            self.print_line(f"> {answer}")
            self.type_text(
                "\n// КПК: АРХИВ\n"
                "Открытие...\n"
            )
            self.entry.config(state="normal")
            self.button.config(state="normal")
            try:
                os.startfile(resource_path("arhive_video_NO3826.mp4"))
            except Exception:
                self.print_line("// ОШИБКА: Файл архива повреждён.")

            self.caesar_hint_ready = False
            return

        self.print_line(f"> {answer}")

        if self.stage == 0:
            self.fragments = []
            if self.is_answer(answer, "start"):
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.caesar_attempts = 0
                self.stage = 1
                self.type_text(
                    "\nДоступ подтверждён.\n"
                    "Добро пожаловать, snorix\n"
                    "Ошибка ключа безопасности.\n"
                    "База данных закрыта от несанкционированного доступа.\n"
                    "Для восстановления доступа пройдите проверку на [данные повреждены].\n\n"
                    "ФРАГМЕНТ 1/3\n"
                    "Чем глубже ты уходишь, тем меньше света.\n"
                    "Но без этого выживший не проживёт и минуты.\n"
                    "Ответ:"
                )
                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.print_line("ОШИБКА:\n"
                                "Логин неверный.\n"
                                "Данные зашифрованы\n\n"
                                "В честь великого диктатора назвали какой-то салат...\n"
                                "и вы называете так обычного человека??\n\n"
                                "«В» здесь явно лишнее" )
                self.caesar_attempts += 1
                self.entry.config(state="normal")
                self.button.config(state="normal")

                if self.caesar_attempts == 4:
                    self.caesar_hint_ready = True
                    self.entry.config(state="disabled")
                    self.button.config(state="disabled")
                    self.type_text(
                        "\n// КПК: Обнаружено архивное видео.\n"
                        "Подтвердите согласие на просмотр.\n"
                    )
                    self.entry.config(state="normal")
                    self.button.config(state="normal")

        elif self.stage == 1:
            if self.is_answer(answer, "oxygen"):
                fragment = self.key_fragments[0]
                self.fragments.append(fragment)
                self.stage = 2
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.type_text(
                    f"\nФРАГМЕНТ 1/3 ВОССТАНОВЛЕН: {fragment}\n\n"
                    "ФРАГМЕНТ 2/3\n"
                    "Маленький, быстрый, спасает от долгих заплывов.\n"
                    "Не подлодка, но без него путь становится мучением.\n"
                    "Ответ:"
                )
                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.print_line("ОШИБКА:\n"
                                "Данные не распознаны.")
                self.entry.config(state="normal")
                self.button.config(state="normal")

        elif self.stage == 2:
            if self.is_answer(answer, "seaglide"):
                fragment = self.key_fragments[1]
                self.fragments.append(fragment)
                self.stage = 3
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.type_text(
                    f"\nФРАГМЕНТ 2/3 ВОССТАНОВЛЕН: {fragment}\n\n"
                    "ФРАГМЕНТ 3/3\n"
                    "[--] обладает длинным телом, немного превосходящим длину «Циклопа».\n"
                    "Он, как и некоторые другие хищники планеты [--], обладает двумя парами чёрных глаз.\n"
                    "На голове этого животного находится довольно большой костяной гребень, предназначенный,\n"
                    "скорее всего, для таранных ударов при битвах левиафанов.\n"
                    "Ответ:"
                )
                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.print_line("ОШИБКА:\n"
                                "Данные не распознаны.")
                self.entry.config(state="normal")
                self.button.config(state="normal")

        elif self.stage == 3:
            if self.is_answer(answer, "base"):
                fragment = self.key_fragments[2]
                self.fragments.append(fragment)
                self.stage = 4
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.type_text(
                    f"\nФРАГМЕНТ 3/3 ВОССТАНОВЛЕН: {fragment}\n\n"
                    "// ЧАСТИЧНЫЙ ДОСТУП\n\n"
                    f"КЛЮЧ БЕЗОПАСНОСТИ КПК:\n«{self.SUBNAUTICA_KEY}»\n\n"
                    "// КПК: АВТОРИЗАЦИЯ.\n"
                    "// Успешно\n\n"
                    "// КПК: ЗАГРУЗКА БОРТОВОГО САМОПИСЦА\n\n"
                    "// РУЧНАЯ ПЕРЕЗАГРУЗКА\n\n"
                    "// Требуется участие человека, /reboot\n"
                )
                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.print_line("ОШИБКА:\n"
                                "Данные не распознаны.")
                self.entry.config(state="normal")
                self.button.config(state="normal")

        elif self.stage == 4:
            if self.is_answer(answer, "boot"):
                self.boot_re_sequence()
                self.stage = 5
                self.type_text(
                    "// БОРТОВОЙ САМОПИСЕЦ: [активен]\n\n"
                    "// Внимание // Курс «Земля — Зезура» [сбит] // Время полёта [неизвестно] // Экипаж /чел/ [6000] / [угроза] // Сигнал [пилинг] // [обработка] // [ошибка]\n\n"
                    "// БОРТОВОЙ САМОПИСЕЦ: [деинсталяция]\n\n"
                    "// КПК: Выполнено\n\n"
                    "// Зашифрованный канал\n\n"
                )
                self.login_animation()
                self.type_text(
                "\nТребуется подтверждение вашей компетентности\n\n"
                "// ПРОВЕРКА ГЛУБИНЫ\n\n"
                "Какая максимальная глубина погружения доступна\n"
                "для оборудования выжившего после полного улучшения?\n\n"
                 "Ответ укажите числом в метрах:\n"
                 )
                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.print_line("ОШИБКА:\n"
                                "Сигнал не распознан.")
                self.entry.config(state="normal")
                self.button.config(state="normal")

        elif self.stage == 5:
            if self.is_answer(answer,"water"):
                self.stage = 6
                self.entry.config(state="disabled")
                self.button.config(state="disabled")

                self.type_text(
                    "\n// ГЛУБИНА ПОДТВЕРЖДЕНА\n\n"
                    "Максимальная глубина:\n"
                    "1800 м\n\n"
                    "// АНАЛИЗ МЕСТНОСТИ\n\n"
                    "Выберите из списка ресурсы,\n"
                    "встречающиеся в местности.\n\n"
                    "Введите номера через пробел.\n\n"
                    "1. Титан\n"
                    "2. Рубин\n"
                    "3. Алмаз\n"
                    "4. Изумруд\n"
                    "5. Банан\n"
                    "6. Соль\n"
                    "7. Шерсть\n"
                    "8. Зубы\n\n"
                    "Ответ:"
                    )
                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.depth_attempts += 1
                self.entry.config(state="disabled")
                self.button.config(state="disabled")

                if self.depth_attempts % 1 == 0:
                    hint = self.get_depth_hint(answer)
                    self.print_line(
                        "ОШИБКА:\n"
                        "Глубина не подтверждена.\n"
                        f"{hint}"
                    )
                else:
                    self.print_line(
                        "ОШИБКА:\n"
                        "Глубина не подтверждена."
                    )

                self.entry.config(state="normal")
                self.button.config(state="normal")

        elif self.stage == 6:
            if self.is_answer(answer,"resource"):
                self.stage = 7
                self.entry.config(state="disabled")
                self.button.config(state="disabled")

                self.type_text(
                "\n// СКАНИРОВАНИЕ\n\n"
                "Титан          [обнаружен]\n"
                "Рубин          [обнаружен]\n"
                "Алмаз          [обнаружен]\n"
                "Соль           [обнаружена]\n"
                "Зубы           [обнаружены]\n\n"
                "Совпадений: 5\n"
                "Результат: подтверждено\n\n"
                "Введите место назначения:\n"
                )

                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.print_line(
                    "ОШИБКА:\n"
                    "Совпадений недостаточно.\n"
                    "Повторите анализ местности."
                )
                self.entry.config(state="normal")
                self.button.config(state="normal")


        elif self.stage == 7:
            if self.is_answer(answer, "future"):
                self.stage = 8
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.type_text(
                    "\n// ЗАВЕРШЕНО.\n"
                    "Процент выживание: 100%.\n\n"
                    f"Для получения доступа к закрытому каналу связи свяжитесь с ТСП-А:"
                    f"\n«{self.SUBNAUTICA_2_KEY}»\n"
                    f"Напишите ключ «экспедиция» для запуска автоматического ответа.\n\n"
                    "С днём рождения, выживший.\n"
                    "Глубина ждёт.\n"
                )
                self.entry.config(state="normal")
                self.button.config(state="normal")
            else:
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
                self.print_line("ОШИБКА:\n"
                                "Сигнал не распознан.")
                self.entry.config(state="normal")
                self.button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDAApp(root)
    root.mainloop()
