# foyou-datclass

Python 数据类相关

## 设计一下

### 样例1

<details>

- 输入 - Result

```json
{
  "code": 400501,
  "message": "no found ad",
  "data": null
}
```

- 输出

```python
@dataclass
class Result(DatClass):
    code: int = None
    message: str = None
    data: str = None
```

</details>

### 样例2

<details>

- 输入 Message

```json
{
  "medalName": "求知",
  "sourceUrl": "https://ask.csdn.net/new",
  "getLevel": 1,
  "desc": "发布1个问题",
  "getImageUrl": "https://csdnimg.cn/c0535f9cefbd4cc0a4878be28bfc4590.png",
  "getTime": "2022-07-15",
  "ifShow": true,
  "medalType": 2,
  "medalId": 114,
  "getMedalTime": null,
  "status": null
}
```

- 输出

```python
@dataclass
class Message(DatClass):
    medal_name: str = None
    source_url = str = None
    get_level: int = None
    desc: str = None
    get_image_url: str = None
    get_time: str = None
    if_show: bool = None
    medal_type: int = None
    medal_id: int = None
    get_medal_time: str = None
    status: str = None
```

</details>

### 样例3

输入 Config

```json
{
  "code": -1,
  "subcode": -1,
  "data": {
    "hotkey": []
  }
}
```

输出

```python
@dataclass
class Config(DatClass):
    code: int = None
    subcode: int = None
    data: Dict = None
```