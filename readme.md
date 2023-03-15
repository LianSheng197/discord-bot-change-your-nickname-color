# Discord Bot - 更換暱稱顏色

**使用 `poetry` 套件管理器。**

- 沒有 `poetry`？
```
pip install poetry
```

- (可選) poetry 預設會把虛擬環境 virtualenv (以下簡稱 venv) 裝在使用者目錄底下。如果想要跟專案放一起的話，請加上這條指令
```
poetry config virtualenvs.in-project true
```

- 安裝本專案所需套件 (會自動建 venv)
```
poetry install
```

-  將 `config.sample.py` 複製成 `config.py`，然後填入你的 bot token 及指定伺服器 id 
```py
def get_token() -> str:
    return "<bot token>"

def get_guild_id() -> int:
    return <伺服器 id>
```

- 進入 venv
```
poetry shell
```

- 啓動 bot
```
python main.py
```
