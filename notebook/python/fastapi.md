# fastapi

## 快速demo

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000,reload=True)
```

（1）导入 FastAPI。  
（2）创建一个 app 实例。  
（3）编写一个路径操作装饰器（如 @app.get(“/”)）。  
（4）编写一个路径操作函数（如上面的 def root(): …）  
（5）定义返回值  
（6）运行开发服务器（如 uvicorn main:app --reload）

fastapi有**交互式 的API 文档**，跳转到 [http://127.0.0.1:8000/docs](https://link.zhihu.com/?target=http%3A//127.0.0.1%3A8000/docs)。你将会看到**自动生成**的交互式 API 文档。

测试demo

```python
from fastapi.testclient import TestClient
from app import app  # 你的 FastAPI app 对象

client = TestClient(app)

# 模拟 GET
response = client.get("/items/", params={"id": "123"})
print(response.json())


# 模拟 POST
response = client.post("/users/", json={"username": "charlie", "password": "xyz"})
print(response.json())

```

## 路由请求

### 路径参数

#### 基本用法

```python
@app.get("/user/{user_id}") 
def get_user(user_id:int): 
    return {"user_id": user_id}
```

路径参数 `user_id` 的值将作为参数 `user_id` 传递给你的函数,比如使用`http://127.0.0.1:8000/user/123`,`user_id`就会自动赋值成`123`

**注意**：fastapi会对类型做检查，如果输入`/user/a`b,则会报错，因为`ab`不是`int`类型

```python
    {
        "detail": [
            {
                "type": "int_parsing",
                "loc": [
                    "path",
                    "user_id"
                ],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "ab"
            }
        ]
    }
```

如果存在两个路由,则按照代码书写顺序从上到下进行匹配，前者会把后者进行覆盖。

```python
@app.get("/user/me")
@app.get("/user/{user_id}")
```

#### 预定义enum

如果希望有效*路径参数*值是预定义的，可以使用`Enum`。

```python
from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return 1
    if model_name.value == "lenet":
        return 2
    return 3
```

#### 含有path的路由

你可能需要参数包含 `/home/johndoe/myfile.txt`，带有一个前导斜杠（`/`）。

在这种情况下，参数的名称是 `file_path`，最后一部分 `:path` 告诉它该参数应该匹配任何*路径*。

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

此时URL 将是：`/files//home/johndoe/myfile.txt`，在 `files` 和 `home` 之间有一个双斜杠（`//`）。

### 查询参数

查询参数是 URL 中 `?` 之后，用 `&` 字符分隔的键值对集合

比如`http://127.0.0.1:8000/items/?skip=0&limit=10`

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, skip: int,limit: int | None = None):
    return {"item_id": item_id, "skip": skip}
```

**FastAPI** 足够智能，能识别出路径参数 `item_id` 是路径参数而 `skip` 是查询参数

当非路径参数声明默认值时，它不是必需要传递的，比如这里的`limit`。

### 请求体

要声明**请求体**，可以使用 [Pydantic](https://docs.pydantic.org.cn/)模型

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict(),"q": q}
    return result
```

仅仅通过这个 Python 类型声明，**FastAPI** 将会

1. 将请求体读取为 JSON。

2. 转换相应的类型（如果需要）。
3. 验证数据。如果数据无效，它将返回一个清晰的错误，精确指出错误数据的位置和内容。

4. 将接收到的数据提供给参数`item`

5. 由于你在函数中将其声明为 `Item` 类型，你将获得所有属性及其类型的所有编辑器支持（补全等）。

函数参数将被识别为如下：

- 如果参数也在**路径**中声明，它将被用作路径参数。
- 如果参数是单一类型（如 `int`、`float`、`str`、`bool` 等），它将被解释为**查询**参数。
- 如果参数声明为 Pydantic 模型的类型，它将被解释为**请求体**。

#### 多个请求体参数

**FastAPI** 会注意到函数中有多个请求体参数，比如

```python
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

则可以这样拆分

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
```

如果请求体中还有单一值，可以参考`Body`参数

## 数据模型和验证

### `Query`

`Query` 是一个**声明参数约束和元数据的特殊函数**，它既是语法糖，又是一个提示给 FastAPI 的机制，让框架知道“这个参数应该来自查询字符串（query string）”。可以把它看作是 **参数描述器**，用来定义：

1. **默认值**
2. **校验规则**（比如长度、数值范围、正则等）
3. **元信息**（例如文档描述、示例值）

核心理念：它并不是运行时的业务逻辑对象，而是**声明式的配置**，FastAPI 解析后会交给 **Pydantic** 做数据验证，并在生成 OpenAPI 文档时展示出来。

#### 基本形式

```python
from fastapi import Query

@app.get("/items/")
async def read_items(q: str = Query(default="default", min_length=3, max_length=10)):
    return {"q": q}

```

当访问 `/items/?q=hello` 时：

- `q` 会自动从 URL 查询字符串中提取，比如 `?q=hello`
- FastAPI 会校验 `q` 是否符合 `min_length` 和 `max_length` 的规则
- 如果校验失败，自动返回 HTTP 422 错误和详细的 JSON 错误信息

这里的 `Query` 实际上返回的是一个 **特殊标记对象**，告诉 FastAPI：

> 这个参数应该从 query string 中取值，并应用这些规则。

#### 主要参数

| 参数                        | 作用                                                |
| --------------------------- | --------------------------------------------------- |
| `default`                   | 默认值；设为 `...` 表示必填                         |
| `alias`                     | 定义别名，比如 URL 用 `item-id`，代码中用 `item_id` |
| `title` / `description`     | 给自动生成的文档添加标题和描述                      |
| `min_length` / `max_length` | 字符串长度限制                                      |
| `ge` / `le` / `gt` / `lt`   | 数值范围限制                                        |
| `regex`                     | 正则表达式验证                                      |
| `deprecated`                | 标记参数已废弃，文档会有提示                        |
| `example` / `examples`      | 给文档生成示例                                      |

#### Annotated写法

```python
from typing import Annotated
from fastapi import Query

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    return {"q": q}
```

当在 `Annotated` 内部使用 `Query` 时，不能为使用 `default` 参数。下面是错误的

```python
q: Annotated[str, Query(default="rick")] = "morty"
```

#### 查询参数列表

使用类似url`https://:8000/items/?q=foo&q=bar`

```python
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items
```

此时响应是

```python
{  "q": [    "foo",    "bar"  ] }
```

#### 别名参数

如果希望使用这种url`http://127.0.0.1:8000/items/?item-query=foobaritems`,但是 `item-query` 不是一个有效的 Python 变量名。此时可以使用`alias`参数

```python
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    ...
```

#### 自定义验证

如果需要进行一些自定义验证，可以使用一个自定义验证器函数，该函数在正常验证之后应用（例如，在验证值是 `str` 之后）。

或者使用 [Pydantic 的 `AfterValidator`](https://docs.pydantic.org.cn/latest/concepts/validators/#field-after-validator)

```python
from typing import Annotated
from pydantic import AfterValidator

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    return {"id": id, "name": data[id]}
```

#### 查询参数模型

如果您有一组相关的**查询参数**，您可以创建一个 **Pydantic 模型**来声明它们。

```python
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    # model_config = {"extra": "forbid"} # 禁止出现额外的查询参数，如果查询参数有额外数据则发送错误响应
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

### `Path`

和Query的基本用法差不多，但这是用在路径参数上的

```python
from typing import Annotated
from fastapi import Path


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    return item_id
```

### `Body`

#### 单一值

如果请求体是这样的

```python
{
    "importance": 5
}
```

可以这样声明来获得`importance`

```python
@app.put("/items/{item_id}")
async def update_item(importance: Annotated[int, Body()]):
    return importance
```

#### 嵌入单个请求体参数

如果希望得到的请求体是

```python
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

而不是

```python
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

直接使用pytantic模型会把Item类解耦出来，所以得加上embed参数

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    ...
```

### `Cookie`

`Cookie` 是 `Path` 和 `Query` 的“姐妹”类。它也继承自相同的通用 `Param` 类

```python
from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

如果有多个参数，可以使用pydantic模型

```python
from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

### `Header`

```python
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

大多数标准请求头都由“连字符”字符分隔，也称为“减号”（`-`）。

但是像 `user-agent` 这样的变量在 Python 中是无效的。

因此，默认情况下，`Header` 会将参数名称中的下划线（`_`）字符转换为连字符（`-`），以提取和生成请求头文档。

此外，HTTP 请求头不区分大小写，因此你可以用标准的 Python 风格（也称为“snake_case”）声明它们。

所以，你可以在 Python 代码中像往常一样使用 `user_agent`，而不是需要将首字母大写为 `User_Agent` 或类似的形式。

如果出于某种原因你需要禁用下划线到连字符的自动转换，请将 `Header` 的参数 `convert_underscores` 设置为 `False`。

如果有多个参数，可以使用pydantic模型

```python
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```
