- [fastapi](#fastapi)
  - [1. 快速demo](#1-快速demo)
  - [2. 路由请求](#2-路由请求)
    - [2.1路径参数](#21路径参数)
      - [2.1.1基本用法](#211基本用法)
      - [2.1.2预定义enum](#212预定义enum)
      - [2.1.3含有path的路由](#213含有path的路由)
    - [2.2查询参数](#22查询参数)
    - [2.3请求体](#23请求体)
      - [多个请求体参数](#多个请求体参数)
  - [3. 数据模型和验证](#3-数据模型和验证)
    - [3.1`Query`](#31query)
      - [基本形式](#基本形式)
      - [主要参数](#主要参数)
      - [Annotated写法](#annotated写法)
      - [查询参数列表](#查询参数列表)
      - [别名参数](#别名参数)
      - [自定义验证](#自定义验证)
      - [查询参数模型](#查询参数模型)
    - [3.2`Path`](#32path)
    - [3.3`Body`](#33body)
      - [单一值](#单一值)
      - [嵌入单个请求体参数](#嵌入单个请求体参数)
    - [3.4`Cookie`](#34cookie)
    - [3.5`Header`](#35header)
    - [3.6 `Form`](#36-form)
      - [表单转json](#表单转json)
      - [表单模型](#表单模型)
    - [3.7`File`](#37file)
      - [多文件上传](#多文件上传)
  - [4. 依赖注入](#4-依赖注入)
  - [5. 身份验证](#5-身份验证)
  - [6. 请求和响应](#6-请求和响应)
    - [6.1 Request](#61-request)
    - [6.2 Response](#62-response)
- [实战重点笔记](#实战重点笔记)
  - [1. 项目构建](#1-项目构建)
    - [1.1项目结构](#11项目结构)
    - [1.2 app实例化](#12-app实例化)
    - [1.3 自定义异常处理](#13-自定义异常处理)
    - [1.4 中间件](#14-中间件)
    - [1.5 视图路由](#15-视图路由)
  - [2. redis](#2-redis)
  - [3. 认证方式](#3-认证方式)
    - [3.1 session\_id](#31-session_id)
      - [3.1.1工作流程](#311工作流程)
      - [3.1.2 特点](#312-特点)
      - [3.1.3 参考实现](#313-参考实现)
    - [3.2 JWT（JSON Web Token）：无状态认证](#32-jwtjson-web-token无状态认证)
      - [3.2.1 工作流程](#321-工作流程)
      - [3.2.2 特点](#322-特点)
      - [3.2.3 参考实现](#323-参考实现)
  - [4. SQLModel](#4-sqlmodel)
  - [5. RBAC权限](#5-rbac权限)

# fastapi

## 1. 快速demo

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
（6）运行开发服务器

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

## 2. 路由请求

### 2.1路径参数

#### 2.1.1基本用法

```python
@app.get("/user/{user_id}") 
def get_user(user_id:int): 
    return {"user_id": user_id}
```

路径参数 `user_id` 的值将作为参数 `user_id` 传递给你的函数,比如使用`http://127.0.0.1:8000/user/123`,`user_id`就会自动赋值成`123`

**注意**：fastapi会对类型做检查，如果输入`/user/ab`,则会报错，因为`ab`不是`int`类型

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

#### 2.1.2预定义enum

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

#### 2.1.3含有path的路由

你可能需要参数包含 `/home/johndoe/myfile.txt`，带有一个前导斜杠（`/`）。

在这种情况下，参数的名称是 `file_path`，最后一部分 `:path` 告诉它该参数应该匹配任何*路径*。

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

此时URL 将是：`/files//home/johndoe/myfile.txt`，在 `files` 和 `home` 之间有一个双斜杠（`//`）。

### 2.2查询参数

查询参数是 URL 中 `?` 之后，用 `&` 字符分隔的键值对集合

比如`http://127.0.0.1:8000/items/?skip=0&limit=10`

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, skip: int,limit: int | None = None):
    return {"item_id": item_id, "skip": skip}
```

**FastAPI** 足够智能，能识别出路径参数 `item_id` 是路径参数而 `skip` 是查询参数

当非路径参数声明默认值时，它不是必需要传递的，比如这里的`limit`。

### 2.3请求体

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

## 3. 数据模型和验证

### 3.1`Query`

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

### 3.2`Path`

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

### 3.3`Body`

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

### 3.4`Cookie`

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

### 3.5`Header`

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

### 3.6 `Form`

HTML 表单（`<form></form>`）向服务器发送数据的方式通常使用一种“特殊”编码，它与 JSON 不同。表单数据通常使用“媒体类型”`application/x-www-form-urlencoded`,当表单包含文件时，它会被编码为 `multipart/form-data`。

FastAPI 默认会把 POST body 当成 JSON 来解析,此时，不能直接使用pydantic模型去接收，你定义参数为 userinfo: UserCreate（Pydantic 模型）时，FastAPI 以为前端发的是 JSON，而你发的是表单 → 格式不匹配

此时可以使用`Form`组件来接受

```python
from typing import Annotated
from fastapi import Form


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
```

#### 表单转json

如果一定想用pydantic模型，可以定义转换函数和依赖注入，这种适用于想自己控制细节的，可扩展

```python
class UserCreate(SQLModel):

    username: str = Field(index=True, max_length=20, description="用户名")
    password: str = Field(max_length=255, description="密码")


    @classmethod
    def as_form( 
            cls,
            username: str = Form(...),
            password: str = Form(...)
        ):
            return cls(username=username, password=password)

    
```

然后路由函数为

```python
# 用 Depends 注入
@app.post("/login/")
async def result_page(
     req: Request,
     userinfo: UserCreate = Depends(UserCreate.as_form),
 ):
 ...
```

#### 表单模型

推荐使用`Annotated`让Form适配pydantic模型，更加现代的写法，但定制空间较小

```python
from typing import Annotated

from fastapi import Form
from pydantic import BaseModel

class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

### 3.7`File`

可以使用 `File` 来定义客户端上传的文件

```python
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

使用 `UploadFile` 相比 `bytes` 有以下几个优点

- 你无需在参数的默认值中使用 `File()`。
- 它使用 "缓冲" 文件，文件在内存中存储，直到达到最大大小限制，超过此限制后将存储在磁盘上。
- 这意味着它能很好地处理大文件，如图像、视频、大型二进制文件等，而不会消耗所有内存。
- 你可以从上传的文件中获取元数据。
- 它具有 [文件类](https://docs.pythonlang.cn/3/glossary.html#term-file-like-object) `async` 接口。
- 它暴露了一个实际的 Python [`SpooledTemporaryFile`](https://docs.pythonlang.cn/3/library/tempfile.html#tempfile.SpooledTemporaryFile) 对象，你可以直接将其传递给其他期望文件类对象的库。

#### 多文件上传

```python
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
```

## 4. 依赖注入

## 5. 身份验证

## 6. 请求和响应

### 6.1 Request

fastapi基于starlette写的，可以直接使用starlette的[request](https://www.starlette.io/requests/#request)，如果想获得请求头、请求体等原始信息，可以直接访问`request.headers`、`request.body()`等属性。

```python
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
```

### 6.2 Response

fastapi同样基于starlette的[response](https://www.starlette.io/responses/#response)

如果想给响应添加cookie或者自定义响应头，可以直接使用`Response`对象

```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    
    response.headers["X-Cat-Dog"] = "alone in the world"

    return {"message": "Come to the dark side, we have cookies"}
```

如果想完全控制响应，可以使用`Response`的子类，比如`JSONResponse`、`HTMLResponse`等

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/headers/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
```

# 实战重点笔记

## 1. 项目构建

### 1.1项目结构

![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250912093431669.png)

其中curd、models、schemas是数据库相关的，api放路由，static放静态页面，views放静态页面相关的视图路由

### 1.2 app实例化

FastAPI 应用有两个重要的阶段：

1. **启动（Startup）**
    应用刚启动时，通常需要做一些初始化操作，比如：
   - 连接数据库
   - 启动后台任务
   - 加载配置文件或模型
2. **关闭（Shutdown）**
    应用关闭时，需要做一些清理工作，比如：
   - 断开数据库连接
   - 停止后台任务
   - 释放资源

`lifespan` 这个 async context manager 就是把这两个阶段**打包成一个上下文**，在 `yield` 之前执行启动逻辑，在 `yield` 之后执行停止逻辑。

![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250912093937561.png)

### 1.3 自定义异常处理

在实例化后，可以给app添加自定义的异常处理机制，来统一拦截应用中的不同类型异常，并返回更清晰、标准化的响应

![img](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250912094635113.png)

```python
async def http_error_handler(_: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "data": exc.detail
    }, status_code=exc.status_code, headers=exc.headers)
```

优点：

1. **统一响应格式**，让所有错误返回类似格式，便于前端解析。

2. **记录和追踪**，你可以在 handler 里记录日志，方便排查问题。

3. **屏蔽敏感信息**，避免将内部错误直接暴露给用户。

4. **灵活扩展业务逻辑**，对于业务级异常，可以实现统一兜底逻辑，比如自动回滚或报警。

### 1.4 中间件

中间件（Middleware）就像一条“拦截管道”，所有请求和响应都必须经过它们。

中间件的常见用途

1. **认证与鉴权**:检查请求头里的 Token，决定是否允许继续访问。
2. **请求日志记录**:记录请求路径、耗时、响应状态码。
3. **全局错误处理**:捕获所有未处理异常，统一返回格式。
4. **Session 管理**:通过 Cookie 保持用户状态，比如 `SessionMiddleware`。
5. **性能监控**:统计请求耗时，打点埋点。

这里我们加入三个组件

```python
# 自己写的组件
class Middleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # pragma: no cover
            await self.app(scope, receive, send)
            return
        start_time = time.time()
        req = Request(scope, receive, send)
        if not req.session.get("session"):
            req.session.setdefault("session", random_str())

        async def send_wrapper(message: Message) -> None:
            process_time = time.time() - start_time
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", str(process_time))
            await send(message)
        await self.app(scope, receive, send_wrapper)
```

```python
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from core.middleware import Middleware  # 完全自定义

app.add_middleware(Middleware)  # 放在最前面添加 → 最内层执行（在 Session 之后）
app.add_middleware(
    SessionMiddleware,
    secret_key="session",
    session_cookie="f_id",
    # max_age=4,
    # same_site="lax",
    # https_only=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
```

**注意**：添加的时候要注意顺序，上面的代码书写顺序是“Middleware，SessionMiddleware，CORSMiddleware”，

执行顺序如下：

```scss
请求进入
↓
CORSMiddleware (前处理)
↓
SessionMiddleware (前处理)
↓
Middleware (前处理)
↓
业务路由函数
↓
Middleware (后处理)
↓
SessionMiddleware (后处理)
↓
CORSMiddlewaree (后处理)
↓
响应返回

```

由于Middleware依赖于SessionMiddleware 生成的request.session，所以在书写时，Middleware一定要放前面

### 1.5 视图路由

首先要给app增加配置

```python
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app.mount('/static', StaticFiles(directory=settings.STATIC_DIR), name="static")
app.state.views = Jinja2Templates(directory=settings.TEMPLATE_DIR)
```

**`app.mount`作用：挂载静态文件目录**

- `app.mount`
   相当于在 FastAPI 应用中“挂载”一个子应用，这里挂载的是 `StaticFiles`，用于托管静态文件，让浏览器可以直接访问 CSS/JS 等资源。
- `"/static"`
   这是 URL 前缀。访问路径中如果以 `/static` 开头，就会进入这个静态文件处理逻辑。
   例如：浏览器请求 `http://localhost:8000/static/style.css`，FastAPI 会去 `settings.STATIC_DIR` 目录下寻找 `style.css` 文件,相反如果想访问**不在**`static`的文件，就会被拒绝。
- `StaticFiles(directory=settings.STATIC_DIR)`
   指定静态文件存放的物理路径，`settings.STATIC_DIR` 通常是一个类似 `./static` 或绝对路径。
- `name="static"`
   给这个挂载的子应用取一个名字。主要用于 **URL 反向解析**，在模板中使用 `url_for('static', path='xxx')` 来生成静态资源 URL。

**`app.state.views`作用：配置模板引擎，用于渲染 HTML 页面**

- `Jinja2Templates`
   这是 FastAPI 提供的一个模板渲染工具，底层用的是 **Jinja2** 模板引擎（Flask 也用它）。

- `directory=settings.TEMPLATE_DIR`
   指定模板文件（HTML）的存放目录。通常你会把模板文件放在 `templates` 文件夹中。

- `app.state.views`
   `app.state` 是 FastAPI 内置的一个“全局存储”，你可以把一些全局变量放在这里。
   把 `Jinja2Templates` 实例挂在 `app.state.views`，之后在路由中可以直接访问，比如：

  ```python
  @app.get("/")
  async def home(request: Request):
      return app.state.views.TemplateResponse("index.html", {"request": request, "title": "首页"})
  ```

## 2. redis

定义初始化和关闭redis的函数，并把这个过程放在Startup和Shutdown的lifespan中。

```python
import redis.asyncio as redis
from core.config import settings

redis_client: redis.Redis | None = None


async def close_redis():
    global redis_client
    print("close redis")
    if redis_client:
        await redis_client.close()


def get_redis():
    return redis_client


async def init_redis(max_connections: int = 20):
    global redis_client
    print("load redis")
    redis_client = await redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=max_connections,
    )

```

使用redis的方式多种多样，可以使用依赖注入

```python
@redis_router.post("/redis/set", response_class=HTMLResponse)
async def redis_set(req: Request, redis: redis.Redis = Depends(get_redis)):
    data = await req.json()
    key = data.get("key")
    value = data.get("value")
    await redis.set(key, value)
    return "ok"
```

也可以使用装饰器或者中间件,在参数到达路由函数就进行判断，之后不走函数直接返回，比如

```python
def cacheable(ttl: int = 3600, key_prefix: str = "cache"):
    """
    Redis 缓存装饰器
    :param ttl: 缓存过期时间（秒）
    :param key_prefix: 缓存 key 前缀
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"

            cached = await redis_client.get(key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            if result is not None:
                await redis_client.set(key, json.dumps(result, default=str), ex=ttl)

            return result
        return wrapper
    return decorator
```

## 3. 认证方式

### 3.1 session_id

#### 3.1.1工作流程

1. 用户登录时，服务器验证用户名和密码。
2. 服务器生成一个**随机的 session_id**（比如 `abc123xyz`），并在服务器内存或数据库里保存这段 session 相关的数据，比如：
   - 用户 ID
   - 登录时间
   - 权限信息
3. 服务器将这个 session_id 返回给客户端，通常存放在浏览器的 **cookie** 里。
4. 后续请求中，浏览器自动携带这个 session_id，服务器通过查找内存或数据库，确认用户身份。

#### 3.1.2 特点

- **状态存储在服务器**，每个活跃用户都占用服务器内存或数据库。
- session_id 本身没有实际信息，只是一个指针或索引。
- 如果服务器挂了，或者 session 数据被清理，用户就需要重新登录。
- **横向扩展难**：如果你有多台服务器，需要通过共享数据库或 Redis 同步 session 数据。

#### 3.1.3 参考实现

1. 参考[中间件](#14-中间件)的`Middleware`写法，就是以`SessionMiddleware`为基础，往`request.session`里面写入了`session_id`,`SessionMiddleware`会使用`Set-Cookie`把相关数据放入前端的`cookie`中，
2. 后端则以`session_id`为key，用户信息为value存储和读取相关信息。

### 3.2 JWT（JSON Web Token）：无状态认证

#### 3.2.1 工作流程

1. 用户登录时，服务器验证用户名和密码。

2. 服务器生成一个 **JWT Token**，这个 Token 内含用户信息，并**用服务器私钥签名**，保证不能被篡改。
    典型 JWT 长这样：

   ```
   xxxxx.yyyyy.zzzzz
   ```

   - `xxxxx`：Header（算法、类型）
   - `yyyyy`：Payload（用户 ID、过期时间、权限等）
   - `zzzzz`：Signature（签名，用来验证 Token 未被篡改）

3. 服务器把 JWT 返回给客户端，客户端存储在 cookie 或 localStorage。

4. 后续请求中，客户端带上这个 JWT，服务器只需验证签名，无需查数据库，就能确认身份。

#### 3.2.2 特点

- **服务器无需存储状态**，只需持有签名密钥。
- 横向扩展更容易，任何服务器节点都能直接验证 Token。
- Token 内含用户信息，太大可能影响传输效率。
- **安全风险**：Token 泄漏后，除非密钥轮换或 Token 过期，攻击者就能直接伪装成用户。

#### 3.2.3 参考实现

1. 后端把用户信息编码`jwt_token`然后传给前端，传给前端的形式不限，主要取决于前端如何存放

    ```python
    @login_router.post("/login", summary="用户登陆接口", response_class=JSONResponse)
    async def account_login(post: AccountLogin, session: SessionDep):

        get_user: User = await curd.user.get_user(session,username=post.username)
        if not get_user:
            return fail(msg=f"用户{post.username}密码验证失败!")
        if not check_password(post.password, get_user.password):
            return fail(msg=f"用户{post.username}密码验证失败!")
        if not get_user.user_status:
            return fail(msg=f"用户{post.username}已被管理员禁用!")
        jwt_data = {
            "user_id": get_user.id,
            "user_type": get_user.user_type
        }
        jwt_token = create_access_token(data=jwt_data)

        return JSONResponse({
            "code": 200,
            "message": "登陆成功😄",
            "data": {"token": "Bearer "+jwt_token}
        }, status_code=200, headers={"Set-Cookie": "X-token=Bearer "+jwt_token})
    ```

2. 后端可以自动获取jwt_token

    ```python
    from fastapi.security.oauth2 import OAuth2PasswordBearer

    OAuth2 = OAuth2PasswordBearer(tokenUrl="", auto_error=False)

    async def check_permissions(
        req: Request, security_scopes: SecurityScopes, session: SessionDep, token=Depends(OAuth2),
    ): ...

    ```

    `token=Depends(OAuth2)`注入的过程等价于下面，相当于试图从请求头的`Authorization`获取token

    ```python
    from fastapi.security.oauth2 import get_authorization_scheme_param

    authorization: str = req.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

    token = param
    ```

    如果能获取token，则还需要解码

    ```python
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

    if payload:
        user_id = payload.get("user_id", None)
        user_type = payload.get("user_type", None)
    ```

3. 前端以下面代码为例，用户在登陆成功后会拿到`token`,此时如果用户想使用`/v1/user/add`,则需要在请求头中放入`{ "Authorization": token }`以来验证login的操作和add的操作来自同一个人

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>注册页面</title>
</head>

<body>
    <form id="loginForm">
        <label>
            用户名:
            <input type="text" placeholder="请输入用户名" name="username">
        </label>
        <label>
            密码:
            <input type="password" placeholder="请设置密码" name="password">
        </label>
        <button type="submit">登录</button>
    </form>
    <form id="regForm">
        <label>
            用户名:
            <input type="text" placeholder="请输入用户名" name="username">
        </label>
        <label>
            密码:
            <input type="password" placeholder="请设置密码" name="password">
        </label>
        <button type="submit">add</button>
    </form>
    <script>
        let token;
        document.getElementById("loginForm").addEventListener("submit", function (e) {
            e.preventDefault();

            const data = {
                username: e.target.username.value,
                password: e.target.password.value
            };

            fetch("/v1/user/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            }).then(res => res.json())
                .then(data => {
                    if (data.code === 200) {
                        token = data.data.token;
                        console.log("Login successful", token);

                    } else {
                        console.log("Login failed");
                        alert(data.message);
                    }
                });
        });
        document.getElementById("regForm").addEventListener("submit", function (e) {
            e.preventDefault();

            const data = {
                username: e.target.username.value,
                password: e.target.password.value,
                user_type: false
            };


            fetch("/v1/user/add", {
                method: "POST",
                credentials: 'include',
                headers: { "Content-Type": "application/json", "Authorization": token },
                body: JSON.stringify(data)
            }).then(res => res.json())
                .then(data => {
                    if (data.code === 200) {

                        console.log("add successful");

                    } else {
                        console.log("add failed");
                        alert(data.message);
                    }
                });
        });
    </script>
</body>
</html>
```

## 4. SQLModel

## 5. RBAC权限
