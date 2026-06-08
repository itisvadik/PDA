import tkinter as tk
import time
import winsound
import sys
import os

# НАСТРОЙКИ ПОДАРКА

# Замени эти заглушки на настоящие ключи перед сборкой .exe
SUBNAUTICA_KEY = "AAAAA-BBBBB-CCCCC"
SUBNAUTICA_2_KEY = "https://t.me/tsp_a_bot"

PDA_VERSION = "2.6"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ANSWERS = {
    "start": ["snorix"],
    "oxygen": ["кислород", "воздух"],
    "seaglide": ["глайдер", "морской глайдер"],
    "base": ["левиафан жнец", "жнец"],
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
                self.print_line("\n// КПК: Выделенный текст скопирован.\n")
            except tk.TclError:
                self.print_line("\n// КПК: Выделите текст, чтобы скопировать.")
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
        )

    def play_typing_sound(self):
        try:
            winsound.PlaySound(
                resource_path("button.wav"),
                winsound.SND_ASYNC | winsound.SND_FILENAME
            )
        except RuntimeError:
            pass

    def boot_sequence(self):
        lines = [
            "// КПК: ЗАГРУЗКА",
            "",
            "██████████ 100%",
            "",
            "ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ...",
            "",
            "// ОШИБКА",
            "",
            "ОБНАРУЖЕНО ПОВРЕЖДЕНИЕ ПАМЯТИ",
            "",
            "ПОПЫТКА ВОССТАНОВЛЕНИЯ...",
            "",
            "██░░░░░░░░ 15%",
            "████░░░░░░ 42%",
            "███████░░░ 71%",
            "",
            "// ОШИБКА",
            "",
            "ПЕРЕХОД В АВАРИЙНЫЙ РЕЖИМ..."
        ]

        for line in lines:
            self.print_line(line)
            self.root.update()
            time.sleep(0.50)

    def personal_file_loading(self):
        lines = [
            "\n\n// КПК: ЗАПРОС ДОСТУПА К АРХИВУ...",
            "",
            "██████████ 100%",
            "",
            "ВОССТАНОВЛЕНИЕ ЛИЧНОГО ДЕЛА...",
            "",
            "███░░░░░░░ 33%",
            "██████░░░░ 66%",
            "██████████ 100%"
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

    def archive_loading(self, archive_name="АРХИВ"):
        lines = [
            f"\n\n// КПК: ПОИСК ДАННЫХ "
            "",
            f"{archive_name}",
            "",
            "███░░░░░░░ 33%",
            "██████░░░░ 66%",
            "██████████ 100%",
            "",
            "ПРОВЕРКА ПРАВ ДОСТУПА...",
            "",
            "███░░░░░░░ 33%",
            "██████░░░░ 66%",
            "██████████ 100%",
            "",
            "ДОСТУП РАЗРЕШЁН"
        ]

        for line in lines:
            self.print_line(line)
            self.root.update()
            time.sleep(0.20)

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
            try:
                os.startfile(resource_path("photo_lghkbq.jpg"))
            except Exception:
                self.print_line("ОШИБКА: Файл анкеты не найден.")
            return

        if self.normalize(answer) == "разработчики":
            self.print_line(f"> {answer}")
            self.type_text(
                    "\n// КПК: СЛУЖЕБНАЯ ИНФОРМАЦИЯ\n\n"
                    "РАЗРАБОТЧИКИ [данные повреждены]\n\n"
                    "Главный инженер:\n"
                    "Логин зашифрован: xk\n\n"
                    "Технический специалист-консультант:\n"
                    "Джиппи\n\n"
                    "// АВАРИНЫЙ ПРОТОКОЛ\n"
                )
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
            return
        if self.normalize(answer) == "статус":
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
            return

        if self.normalize(answer) in ["sixseven", "six seven", "67", "6 7"]:
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
                os.startfile(resource_path("arhive_video_NO67.MP4"))
            except Exception:
                self.print_line("// ОШИБКА: Архив SXS-67 повреждён.")
            self.root.after(19000, self.root.destroy)
            return

        normalized_answer = self.normalize(answer)

        if normalized_answer in BANNED_WORDS:
            data = BANNED_WORDS[normalized_answer]

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

        if self.caesar_hint_ready and self.normalize(answer) in ["да", "открыть", "согласие", "архив", "ок"]:
            self.print_line(f"> {answer}")
            self.type_text(
                "\n// КПК: АРХИВ\n"
                "Открытие...\n"
            )

            try:
                os.startfile(resource_path("arhive_video_NO3826.MP4"))
            except Exception:
                self.print_line("// ОШИБКА: Файл архива повреждён.")

            self.caesar_hint_ready = False
            return

        self.print_line(f"> {answer}")

        if self.stage == 0:
            self.fragments = []
            if self.is_answer(answer, "start"):
                self.caesar_attempts = 0
                self.stage = 1
                self.type_text(
                    "\nДоступ подтверждён.\n"
                    "Добро пожаловать, snorix\n"
                    "Ошибка ключей безопасности.\n"
                    "База данных зашифрована от несанкционированного доступа.\n"
                    "Для восстановления доступа пройдите проверку на [данные повреждены].\n\n"
                    "ФРАГМЕНТ 1/3\n"
                    "Чем глубже ты уходишь, тем меньше света.\n"
                    "Но без этого выживший не проживёт и минуты.\n"
                    "Ответ:"
                )
            else:
                self.print_line("ОШИБКА:\n"
                                "Логин неверный.\n"
                                "Данные зашифрованы\n\n"
                                "В честь великого диктатора назвали какой-то салат...\n"
                                "и вы называете так обычного человека??\n\n"
                                "«В» здесь явно лишнее" )
                self.caesar_attempts += 1

                if self.caesar_attempts == 4:
                    self.caesar_hint_ready = True
                    self.type_text(
                        "\n// КПК: Обнаружено архивное видео.\n"
                        "Подтвердите согласие на просмотр.\n"
                    )

        elif self.stage == 1:
            if self.is_answer(answer, "oxygen"):
                self.fragments.append("AAAAA")
                self.stage = 2
                self.type_text(
                    "\nФРАГМЕНТ 1/3 ВОССТАНОВЛЕН: AAAAA\n\n"
                    "ФРАГМЕНТ 2/3\n"
                    "Маленький, быстрый, спасает от долгих заплывов.\n"
                    "Не подлодка, но без него путь становится мучением.\n"
                    "Ответ:"
                )
            else:
                self.print_line("ОШИБКА:\n"
                                "Данные не распознаны.")

        elif self.stage == 2:
            if self.is_answer(answer, "seaglide"):
                self.fragments.append("BBBBB")
                self.stage = 3
                self.type_text(
                    "\nФРАГМЕНТ 2/3 ВОССТАНОВЛЕН: BBBBB\n\n"
                    "ФРАГМЕНТ 3/3\n"
                    "[--] обладает длинным телом, немного превосходящим длину «Циклопа».\n"
                    "Он, как и некоторые другие хищники планеты [--], обладает двумя парами чёрных глаз.\n"
                    "На голове этого животного находится довольно большой костяной гребень, предназначенный,\n"
                    "скорее всего, для таранных ударов при битвах левиафанов.\n"
                    "Ответ:"
                )
            else:
                self.print_line("ОШИБКА:\n"
                                "Данные не распознаны.")

        elif self.stage == 3:
            if self.is_answer(answer, "base"):
                self.fragments.append("CCCCC")
                self.stage = 4
                self.type_text(
                    "\nФРАГМЕНТ 3/3 ВОССТАНОВЛЕН: CCCCC\n\n"
                    "ЧЕРТЁЖ ВОССТАНОВЛЕН.\n"
                    "Доступ к архиву открыт.\n\n"
                    f"КЛЮЧ ВХОДА В СИСТЕМУ КПК:\n{SUBNAUTICA_KEY}\n\n"
                    "ВНИМАНИЕ.\n"
                    "Обнаружен новый сигнал.\n"
                    "Источник неизвестен.\n"
                    "Сигнал исходит из источника на ранних этапах разработки.\n"
                    "Чтобы продолжить сканирование, введи название места назначения.\n"
                    "Ответ:"
                )
            else:
                self.print_line("ОШИБКА:\n"
                                "Данные не распознаны.")

        elif self.stage == 4:
            if self.is_answer(answer, "future"):
                self.stage = 5
                self.type_text(
                    "\nСКАНИРОВАНИЕ ЗАВЕРШЕНО.\n"
                    "Полный доступ восстановлен.\n\n"
                    f"Для получения доступа к закрытому каналу связи свяжитесь с ТСП:"
                    f"\n{SUBNAUTICA_2_KEY}\n"
                    f"Напишите ключ «экспедиция» для запуска автоматического ответа.\n\n"
                    "С днём рождения, выживший.\n"
                    "Глубина ждёт.\n"
                )
                self.entry.config(state="disabled")
                self.button.config(state="disabled")
            else:
                self.print_line("ОШИБКА:\n"
                                "Сигнал не распознан.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDAApp(root)
    root.mainloop()
