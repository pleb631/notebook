- [pydantic](#pydantic)
  - [1. BaseModel](#1-basemodel)
    - [1.1基本用法](#11基本用法)
    - [1.2 属性方法](#12-属性方法)
    - [1.3 嵌套模型](#13-嵌套模型)
    - [1.4 必填字段](#14-必填字段)
    - [1.5 动态默认值](#15-动态默认值)
  - [2. Field](#2-field)
    - [2.1 参数](#21-参数)
    - [2.2 computed\_field](#22-computed_field)
  - [3. 别名](#3-别名)
    - [3.1 alias](#31-alias)
    - [3.2 别名路径、别名选择](#32-别名路径别名选择)
    - [3.3 别名生成器](#33-别名生成器)
    - [3.4 别名优先级](#34-别名优先级)
    - [3.5 注意](#35-注意)
  - [4. 验证装饰器](#4-验证装饰器)

# pydantic

## 1. BaseModel

### 1.1基本用法

```pyhon
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = 'Jane Doe'
    
user = User(id='123')
```

在这个例子中， `user` 是 `User` 的一个实例。对象的初始化将执行所有的解析和验证。如果没有抛出 `ValidationError` ，你就知道生成的模型实例是有效的。

### 1.2 属性方法

```python
# 返回key的set
.model_fields_set: set[str] 


# 返回实例的复制
.model_copy(
    *,
    update: dict[str, Any] | None = None, # 可以在复制的过程中为新实例更新参数
    deep: bool = False # 深复制
) -> Self

# 返回实例的json字段
.model_dump(
    *,
    mode: Literal["json", "python"] | str = "python", 
    include: IncEx = None, # set,选择哪个参数要被dump
    exclude: IncEx = None, # set,选择哪个参数不被dump
    context: Any | None = None,
    by_alias: bool = False, # 是否使用别名
    exclude_unset: bool = False, # 是否排除未显式设置的字段(显示设置成默认值的不会被排除)。
    exclude_defaults: bool = False, # 是否排除是否设置成默认值的key
    exclude_none: bool = False, # 是否排除是否设置成None的key
    round_trip: bool = False,
    warnings: (
        bool | Literal["none", "warn", "error"]
    ) = True,
    serialize_as_any: bool = False
) -> dict[str, Any]

# 返回实例的json序列化
.model_dump_json(
    *,
    indent: int | None = None,
    include: IncEx = None,
    exclude: IncEx = None,
    context: Any | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    round_trip: bool = False,
    warnings: (
        bool | Literal["none", "warn", "error"]
    ) = True,
    serialize_as_any: bool = False
) -> str


# 返回可序列化的json字典
.model_json_schema(
    by_alias: bool = True,
    ref_template: str = DEFAULT_REF_TEMPLATE,
    schema_generator: type[
        GenerateJsonSchema
    ] = GenerateJsonSchema,
    mode: JsonSchemaMode = "validation",
) -> dict[str, Any]

```

### 1.3 嵌套模型

只要数据格式正确，就可以递归的创建

```python
from typing import List, Optional

from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'


class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]


m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
print(m)
"""
foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'), Bar(apple='x2', banana='y')]
"""
print(m.model_dump())
"""
{
    'foo': {'count': 4, 'size': None},
    'bars': [{'apple': 'x1', 'banana': 'y'}, {'apple': 'x2', 'banana': 'y'}],
}
"""
```

### 1.4 必填字段

要声明一个字段为必填字段，您可以使用注解或注解与 `Field` 规范结合使用。`Field` 函数主要用于为属性配置设置，如 `alias` 或 `description`

```python
from pydantic import BaseModel, Field


class Model(BaseModel):
    a: int
    b: int = ...
    c: int = Field(..., alias='C')
```

### 1.5 动态默认值

如果将可变对象用作函数或方法参数的默认值，则每次调用中都会重用同一个实例，如下，这种情况，会报错提醒

```python
class Model(BaseModel):
    item_counts: List[Dict[str, int]] = [{}]
```

正确方法是使用`default_factory`,这样每次调用时都会使用函数创建新的值。

```python
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Model(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    updated: datetime = Field(default_factory=datetime_now)


m1 = Model()
m2 = Model()
assert m1.uid != m2.uid
```

## 2. Field

[`Field`](https://pydantic.com.cn/api/fields/#pydantic.fields.Field)函数用于自定义和向模型字段添加元数据。

### 2.1 参数

| 参数                  | 类型              | 描述                                      |
| --------------------- | ----------------- | ----------------------------------------- |
| default               | Any               |                                           |
| default_factory       | Callable[[], Any] | None                                      |
| alias                 | str               |                                           |
| alias_priority        | int               |                                           |
| validation_alias      |                   |                                           |
| serialization_alias   | str               |                                           |
| description           | str               |                                           |
| exclude               | bool              | 是否不参与序列化                          |
| deprecated            | bool              |                                           |
| frozen                | bool              | 是否不允许更改                            |
| validate_default      | bool              | 是否验证默认值                            |
| strict                | bool              | 是否开启strict模式（不能自动格式转换）    |
| gt/ge/lt/le           |                   | 仅适用于数字的比较                        |
| multiple_of           | float             | 是否是xx的倍数                            |
| min_length/max_length | int               | 可迭代对象的长度                          |
| pattern               | str               | 正则表达式                                |
| allow_inf_nan         | bool              | 允许 `inf`、`-inf`、`nan`。仅适用于数字。 |
| max_digits            | int               | 字符串的最大位数                          |
| decimal_places        | int               | 数字允许的最大小数位数                    |

### 2.2 computed_field

可用于在序列化模型或数据类时包含 `property` 或 `cached_property` 属性。这对于从其他字段计算得出的字段或计算成本高的字段很有用

```python
from pydantic import BaseModel, computed_field


class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    # @deprecated("'volume' is deprecated")
    def volume(self) -> float:
        return self.width * self.height * self.depth


b = Box(width=1, height=2, depth=3)
print(b.model_dump())
#> {'width': 1.0, 'height': 2.0, 'depth': 3.0, 'volume': 6.0}
```

## 3. 别名

### 3.1 alias

有三种定义别名的方法：

- `Field(..., alias='foo')`
- `Field(..., validation_alias='foo')`
- `Field(..., serialization_alias='foo')`

`alias` 参数既用于验证，也用于序列化。如果希望分别为验证和序列化使用不同的别名，可以使用 `validation_alias` 和 `serialization_alias` 参数，它们将仅在各自的用例中应用。

### 3.2 别名路径、别名选择

为了方便在使用 `validation_alias` 时提供了两种特殊类型： `AliasPath` 和 `AliasChoices`

`AliasPath` 用于使用别名指定字段的路径。例如：

```python
from pydantic import BaseModel, Field, AliasPath


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasPath('names', 0))
    last_name: str = Field(validation_alias=AliasPath('names', 1))

user = User.model_validate({'names': ['John', 'Doe']})  # (1)!
print(user)
#> first_name='John' last_name='Doe'
```

在 `'first_name'` 字段中，我们使用别名 `'names'` 和索引 `0` 指定第一个名字的路径。在 `'last_name'` 字段中，我们使用别名 `'names'` 和索引 `1` 指定最后一个名字的路径。

`AliasChoices` 用于指定别名的选择。例如：

```python
from pydantic import BaseModel, Field, AliasChoices


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasChoices('first_name', 'fname'))
    last_name: str = Field(validation_alias=AliasChoices('last_name', 'lname'))

user = User.model_validate({'fname': 'John', 'lname': 'Doe'})  # (1)!
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'first_name': 'John', 'lname': 'Doe'})  # (2)!
print(user)
#> first_name='John' last_name='Doe'
```

1. 我们正在对这两个字段使用第二个别名选择。
2. 我们正在使用字段 `'first_name'` 的第一个别名选项和字段 `'last_name'` 的第二个别名选项。

也可以混合使用

```python
from pydantic import BaseModel, Field, AliasPath, AliasChoices


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasChoices('first_name', AliasPath('names', 0)))
    last_name: str = Field(validation_alias=AliasChoices('last_name', AliasPath('names', 1)))


user = User.model_validate({'first_name': 'John', 'last_name': 'Doe'})
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'names': ['John', 'Doe']})
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'names': ['John'], 'last_name': 'Doe'})
print(user)
#> first_name='John' last_name='Doe'
```

### 3.3 别名生成器

可以使用`ConfigDict`的 `alias_generator` 参数指定一个可调用对象，该对象将为模型中的所有字段生成别名

Pydantic 提供了三个内置的别名生成器，您可以直接使用：

- to_pascal
- to_camel
- to_snake

基本案例

```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Tree(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: field_name.upper()
        # alias_generator=to_camel
        populate_by_name=True 
    )

    age: int
    height: float
    kind: str


t = Tree.model_validate({'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'})
print(t.model_dump(by_alias=True))
#> {'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'}
```

### 3.4 别名优先级

可以在字段上设置 `alias_priority` 来更改此行为：

- `alias_priority=2` 别名不会被别名生成器覆盖。

- `alias_priority=1` 别名将被别名生成器覆盖。

- 未设置：

  - 别名已设置：别名不会被别名生成器覆盖。
  - 未设置别名：别名将被别名生成器覆盖。

### 3.5 注意

- 只传 alias → 不需要 `populate_by_name`。
- 使用alias生成器，会改变外部交互的字段名，想让原字段名也可用 → 必须 `populate_by_name=True`。

## 4. 验证装饰器

[`@validate_call`](https://pydantic.com.cn/api/validate_call/#pydantic.validate_call_decorator.validate_call)装饰器允许在调用函数之前，使用函数的注释来解析和验证传递给函数的参数。验证失败会报 `ValidationError`

```python
from pydantic import validate_call


@validate_call
def validate_foo(a: int, b: int):
        return b


foo = validate_foo(a=1, b=2)
print(foo)
#> 2
foo = validate_foo(a=1, b=[1,2,3]) # 报错
```
