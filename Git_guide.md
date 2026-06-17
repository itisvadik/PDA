Проверить состояние репозитория:

git status

Показывает:

Что изменено
Что удалено
Что будет добавлено
Добавить только один файл

Например КПК:

git add pda_gift_app.py

Или:

git add build.py
Добавить несколько конкретных файлов
git add pda_gift_app.py build.py README.md
Добавить всё изменённое

⚠️ Использовать осторожно:

git add .

или

git add --all
Создать коммит
git commit -m "КПК 2.7-PRE: обновлены фрагменты ключа"
Отправить изменения на GitHub
git push
Получить изменения с GitHub
git pull
Посмотреть историю коммитов

Кратко:

git log --oneline

Пример:

a8c41c2 КПК 2.7-PRE
d91fa23 Исправление ТСП-А
Проверить текущую ветку
git branch

Звёздочка показывает активную:

* main

или

* pda-2.7-pre
Создать новую ветку
git checkout -b pda-2.7-pre
Переключиться на существующую ветку
git checkout main



git merge PDA-2.7-PRE
git push --set-upstream origin PDA