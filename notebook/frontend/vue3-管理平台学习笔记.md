# 搭建模板

## 1. 项目初始化

### 1.1环境准备

+ node v20.18.0
+ pnpm 10.8.1

### 1.2初始化项目

本项目使用vite进行构建，vite官方中文文档参考：[cn.vitejs.dev/guide/](https://cn.vitejs.dev/guide/)

pnpm安装指令

```plain
npm i -g pnpm
```

项目初始化命令pnpm:

```plain
pnpm create vite
```

### 1.3 浏览器自动打开

`package.json`

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1685950295448-6bdd848e-22c4-4e68-9697-5e1d6a6b193f-678310.png)

### 1.4 配置**prettier**

有了eslint，为什么还要有prettier？eslint针对的是javascript，他是一个检测工具，包含js语法以及少部分格式问题，在eslint看来，语法对了就能保证代码正常运行，格式问题属于其次；

而prettier属于格式化工具，它看不惯格式不统一，所以它就把eslint没干好的事接着干，另外，prettier支持

包含js在内的多种语言。

总结起来，**eslint和prettier这俩兄弟一个保证js代码质量，一个保证代码美观。**

##### 安装依赖包

```plain
pnpm install -D eslint-plugin-prettier prettier eslint-config-prettier
```

##### prettierrc.json 添加规则

```plain
{
  "singleQuote": true,
  "semi": false,
  "bracketSpacing": true,
  "htmlWhitespaceSensitivity": "ignore",
  "endOfLine": "auto",
  "trailingComma": "all",
  "tabWidth": 2
}
```

##### .prettierignore忽略文件

```plain
/dist/*
/html/*
.local
/node_modules/**
**/*.svg
**/*.sh
/public/*
```



## 2.  项目集成

### 2.1集成element-plus

这里UI组件库采用的element-plus

官网地址:https://element-plus.gitee.io/zh-CN/

```plain
pnpm install element-plus @element-plus/icons-vue
```



**入口文件main.ts全局安装element-plus,element-plus默认支持语言英语设置为中文**

```ts
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'

import zhCn from "element-plus/es/locale/lang/zh-cn";
app.use(ElementPlus, {
    locale: zhCn
})
```



**Element Plus全局组件类型声明**

```json
// tsconfig.json 
{"compilerOptions": {
    "baseUrl": "./", // 解析非相对模块的基地址，默认是当前目录
    "paths": { //路径映射，相对于baseUrl
      "@/*": [
        "src/*"
      ]
    },
    "types": [
      "element-plus/global"
    ]
  }
 }
```



**补充** 自动导入组件和api

```plain
pnpm i -D unplugin-vue-components unplugin-auto-import
```

然后在`vite.config.ts` 中配置

```ts
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';

export default defineConfig({
  plugins: [
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
});

```

### 2.2 src别名的配置

在开发项目的时候文件与文件关系可能很复杂，因此我们需要给src文件夹配置一个别名！！！

```plain
// vite.config.ts
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
	'@': path.resolve(__dirname, 'src'),
      '~': path.resolve(__dirname, 'src/assets')
		}
    }
})
```

**TypeScript 编译配置**

```plain
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": "./", // 解析非相对模块的基地址，默认是当前目录
    "paths": { //路径映射，相对于baseUrl
      "@/*": ["src/*"] 
    }
  }
}
```

### 2.3环境变量的配置

**项目开发过程中，至少会经历开发环境、测试环境和生产环境(即正式环境)三个阶段。不同阶段请求的状态(如接口地址等)不尽相同，若手动切换接口地址是相当繁琐且易出错的。于是环境变量配置的需求就应运而生，我们只需做简单的配置，把环境状态切换的工作交给代码。**

开发环境（development） 顾名思义，开发使用的环境，每位开发人员在自己的dev分支上干活，开发到一定程度，同事会合并代码，进行联调。

测试环境（testing） 测试同事干活的环境啦，一般会由测试同事自己来部署，然后在此环境进行测试

生产环境（production） 生产环境是指正式提供对外服务的，一般会关掉错误报告，打开错误日志。(正式提供给客户使用的环境。)

注意:一般情况下，一个环境对应一台服务器,也有的公司开发与测试环境是一台服务器！！！

项目根目录分别添加 开发、生产和测试环境的文件!

```plain
.env.development
.env.production
.env.test
```

文件内容

```plain
# 变量必须以 VITE_ 为前缀才能暴露给外部读取
NODE_ENV = 'development'
VITE_APP_TITLE = '运营平台'
VITE_APP_BASE_API = '/dev-api'
```

```plain
NODE_ENV = 'production'
VITE_APP_TITLE = '运营平台'
VITE_APP_BASE_API = '/prod-api'
```

```plain
# 变量必须以 VITE_ 为前缀才能暴露给外部读取
NODE_ENV = 'test'
VITE_APP_TITLE = '运营平台'
VITE_APP_BASE_API = '/test-api'
```

配置运行命令：package.json

```plain
"scripts": {
    "dev": "vite --open",
    "build:test": "vue-tsc && vite build --mode test",
    "build:pro": "vue-tsc && vite build --mode production",
    "preview": "vite preview"
  },
```

通过import.meta.env获取环境变量

### 2.4 SVG图标配置

在开发项目的时候经常会用到svg矢量图,而且我们使用SVG以后，页面上加载的不再是图片资源,

这对页面性能来说是个很大的提升，而且我们SVG文件比img要小的很多，放在项目中几乎不占用资源。

**安装SVG依赖插件**

```plain
pnpm install vite-plugin-svg-icons -D
```

**在****vite.config.ts****中配置插件**

```plain
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import path from 'path'
export default () => {
  return {
    plugins: [
      createSvgIconsPlugin({
        // Specify the icon folder to be cached
        iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
        // Specify symbolId format
        symbolId: 'icon-[dir]-[name]',
      }),
    ],
  }
}
```

**入口文件导入**

```plain
import 'virtual:svg-icons-register'
```

**在src/components目录下创建一个SvgIcon组件:代表如下**

```plain
<template>
  <div>
    <svg :style="{ width: width, height: height }">
      <use :xlink:href="prefix + name" :fill="color"></use>
    </svg>
  </div>
</template>

<script setup lang="ts">
defineProps({
  //xlink:href属性值的前缀
  prefix: {
    type: String,
    default: '#icon-'
  },
  //svg矢量图的名字
  name: String,
  //svg图标的颜色
  color: {
    type: String,
    default: ""
  },
  //svg宽度
  width: {
    type: String,
    default: '16px'
  },
  //svg高度
  height: {
    type: String,
    default: '16px'
  }

})
</script>
<style scoped></style>
```

#### 注册全局组件

在src文件夹目录下创建一个index.ts文件：用于注册components文件夹内部全部全局组件！！！

```plain
import SvgIcon from './SvgIcon/index.vue';
import type { App, Component } from 'vue';
const components: { [name: string]: Component } = { SvgIcon };
export default {
    install(app: App) {
        Object.keys(components).forEach((key: string) => {
            app.component(key, components[key]);
        })
    }
}
```

在入口文件引入src/index.ts文件,通过app.use方法安装自定义插件

```plain
import gloablComponent from './components/index';
app.use(gloablComponent);
```

### 2.5 集成sass

先安装sass sass-loader,在组件内可以使用scss语法，需要加上lang="scss"

```plain
<style scoped lang="scss"></style>
```

接下来我们为项目添加一些全局的样式

在src/styles目录下创建一个index.scss文件，当然项目中需要用到清除默认样式，因此在index.scss引入reset.scss

```plain
@import reset.scss
```

在入口文件引入

```plain
import '@/styles'
```

但是你会发现在src/styles/index.scss全局样式文件中没有办法使用变量.因此需要给项目中引入全局变量.

在style/variable.scss创建一个variable.scss文件！

在vite.config.ts文件配置如下:

```plain
export default defineConfig((config) => {
    css: {
      preprocessorOptions: {
        scss: {
          javascriptEnabled: true,
          additionalData: `@import "@/styles/variable.scss";`,
        },
      },
    },
    }
}
```

配置完毕你会发现scss提供这些全局变量可以在组件样式中使用了！！！

### 2.6 mock数据

安装依赖:https://[www.npmjs.com/package/vite-plugin-mock](http://www.npmjs.com/package/vite-plugin-mock)

```plain
pnpm install -D vite-plugin-mock mockjs
```

在 vite.config.js 配置文件启用插件。

```plain
import { UserConfigExport, ConfigEnv } from 'vite'
import { viteMockServe } from 'vite-plugin-mock'
import vue from '@vitejs/plugin-vue'
export default ({ command })=> {
  return {
    plugins: [
      vue(),
      viteMockServe({
        localEnabled: command === 'serve',
      }),
    ],
  }
}
```

在根目录创建mock文件夹:去创建我们需要mock数据与接口！！！

在mock文件夹内部创建一个user.ts文件

```plain
//用户信息数据
function createUserList() {
    return [
        {
            userId: 1,
            avatar:
                'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            username: 'admin',
            password: '111111',
            desc: '平台管理员',
            roles: ['平台管理员'],
            buttons: ['cuser.detail'],
            routes: ['home'],
            token: 'Admin Token',
        },
        {
            userId: 2,
            avatar:
                'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            username: 'system',
            password: '111111',
            desc: '系统管理员',
            roles: ['系统管理员'],
            buttons: ['cuser.detail', 'cuser.user'],
            routes: ['home'],
            token: 'System Token',
        },
    ]
}

export default [
    // 用户登录接口
    {
        url: '/api/user/login',//请求地址
        method: 'post',//请求方式
        response: ({ body }) => {
            //获取请求体携带过来的用户名与密码
            const { username, password } = body;
            //调用获取用户信息函数,用于判断是否有此用户
            const checkUser = createUserList().find(
                (item) => item.username === username && item.password === password,
            )
            //没有用户返回失败信息
            if (!checkUser) {
                return { code: 201, data: { message: '账号或者密码不正确' } }
            }
            //如果有返回成功信息
            const { token } = checkUser
            return { code: 200, data: { token } }
        },
    },
    // 获取用户信息
    {
        url: '/api/user/info',
        method: 'get',
        response: (request) => {
            //获取请求头携带token
            const token = request.headers.token;
            //查看用户信息是否包含有次token用户
            const checkUser = createUserList().find((item) => item.token === token)
            //没有返回失败的信息
            if (!checkUser) {
                return { code: 201, data: { message: '获取用户信息失败' } }
            }
            //如果有返回成功信息
            return { code: 200, data: {checkUser} }
        },
    },
]
```

**安装axios**

```plain
pnpm install axios
```

测试代码：

```vue
<script setup lang="ts">
import axios from "axios";

axios({
    url: "/api/user/login",
    method: "post",
    data: {
        username: "admin",
        password: "111111",
    },
})
    .then((res) => {
        console.log(res.data);
    })
    .catch((err) => {
        console.log(err);
    });
</script>
```

### 2.7 axios二次封装

在开发项目的时候避免不了与后端进行交互,因此我们需要使用axios插件实现发送网络请求。在开发项目的时候

我们经常会把axios进行二次封装。

目的:

1:使用请求拦截器，可以在请求拦截器中处理一些业务(开始进度条、请求头携带公共参数)

2:使用响应拦截器，可以在响应拦截器中处理一些业务(进度条结束、简化服务器返回的数据、处理http网络错误)

在根目录下创建utils/request.ts

```plain
import axios from "axios";
import { ElMessage } from "element-plus";
//创建axios实例
let request = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 5000
})
//请求拦截器
request.interceptors.request.use(config => {
// config.header.token="123"  //可以加请求头
    return config;
});
//响应拦截器
request.interceptors.response.use((response) => {
    return response.data;
}, (error) => {
    //处理网络错误
    let msg = '';
    let status = error.response.status;
    switch (status) {
        case 401:
            msg = "token过期";
            break;
        case 403:
            msg = '无权访问';
            break;
        case 404:
            msg = "请求地址错误";
            break;
        case 500:
            msg = "服务器出现问题";
            break;
        default:
            msg = "无网络";

    }
    ElMessage({
        type: 'error',
        message: msg
    })
    return Promise.reject(error);
});
export default request;
```

### 

### 2.8 API接口统一管理

在开发项目的时候,接口可能很多需要统一管理。在src目录下去创建api文件夹去统一管理项目的接口；

比如:下面方式

```plain
//统一管理咱们项目用户相关的接口

import request from "@/utils/request";

interface loginFormData {
    username: string;
    password: string;
}
interface loginResponseData {
    code: number;
    data: string;
    message: string;
}
//项目用户相关的请求地址

enum API {
    LOGIN_URL = "/api/user/login",

    USERINFO_URL = "/api/user/info",

}
//登录接口
export const reqLogin = (data: loginFormData) =>
    request.post<any, loginResponseData>(API.LOGIN_URL, data);
//获取用户信息

export const reqUserInfo = () =>
    request.get<any, userInfoReponseData>(API.USERINFO_URL);



```

# 项目主体

## 1.路由配置

### 1.1路由组件的雏形

`src\views\home\index.vue`（以home组件为例）

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686059593185-b1f1ecb6-0789-4c0d-8cac-9340db0ad9ea-326791.png)

### 1.2路由配置

#### 1.2.1路由index文件

`src\router\index.ts`

```typescript
//通过vue-router插件实现模板路由配置
import { createRouter, createWebHashHistory } from 'vue-router'
import { constantRoute } from './router'
//创建路由器
const router = createRouter({
  //路由模式hash
  history: createWebHashHistory(),
  routes: constantRoute,
  //滚动行为
  scrollBehavior() {
    return {
      left: 0,
      top: 0,
    }
  },
})
export default router

```

#### 1.2.2路由配置

`src\router\router.ts`

```typescript
//对外暴露配置路由(常量路由)
export const constantRoute = [
  {
    //登录路由
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    name: 'login', //命名路由
  },
  {
    //登录成功以后展示数据的路由
    path: '/',
    component: () => import('@/views/home/index.vue'),
    name: 'layout',
  },
  {
    path: '/404',
    component: () => import('@/views/404/index.vue'),
    name: '404',
  },
  {
    //重定向
    path: '/:pathMatch(.*)*',
    redirect: '/404',
    name: 'Any',
  },
]

```

### 1.3路由出口

`src\App.vue`

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686059779295-e44a4f8d-8229-4d4b-bc2e-491c3c087169-004957.png)

## 2.登录模块

### 2.1 登录路由静态组件

`src\views\login\index.vue`

```vue
<template>
  <div class="login_container">
    <el-row>
      <el-col :span="12" :xs="0"></el-col>
      <el-col :span="12" :xs="24">
        <el-form class="login_form">
          <h1>Hello</h1>
          <h2>欢迎来到管理平台</h2>
          <el-form-item>
            <el-input
              :prefix-icon="User"
              v-model="loginForm.username"
              ></el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              type="password"
              :prefix-icon="Lock"
              v-model="loginForm.password"
              show-password
              ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button class="login_btn" type="primary" size="default">
              登录
            </el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
  import { User, Lock } from '@element-plus/icons-vue'
  import { reactive } from 'vue'
  //收集账号与密码数据
  let loginForm = reactive({ username: 'admin', password: '111111' })
</script>

<style lang="scss" scoped>
  .login_container {
    width: 100%;
    height: 100vh;
    background: url('@/assets/images/background.jpg') no-repeat;
    background-size: cover;
    .login_form {
      position: relative;
      width: 80%;
      top: 30vh;
      background: url('@/assets/images/login_form.png') no-repeat;
      background-size: cover;
      padding: 40px;
      h1 {
        color: white;
        font-size: 40px;
      }
      h2 {
        color: white;
        font-size: 20px;
        margin: 20px 0px;
      }
      .login_btn {
        width: 100%;
      }
    }
  }
</style>

```

注意：el-col是24份的，在此左右分为了12份。我们在右边放置我们的结构。`:xs="0"`是为了响应式。`el-form`下的element-plus元素都用`el-form-item`包裹起来。

### 2.2 登陆业务实现

#### 2.2.1 登录按钮绑定回调

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686109159913-c7acf59a-a335-420a-85a0-5f09a2d79f37-025950.png)

#### 2.2.2 仓库store初始化

1. **大仓库**（笔记只写一次）

安装pinia：`pnpm i pinia`

`src\store\index.ts`

```vue
//仓库大仓库
import { createPinia } from 'pinia'
//创建大仓库
const pinia = createPinia()
//对外暴露：入口文件需要安装仓库
export default pinia

```

2. **用户相关的小仓库**

`src\store\modules\user.ts`

```vue
//创建用户相关的小仓库
import { defineStore } from 'pinia'
//创建用户小仓库
const useUserStore = defineStore('User', {
  //小仓库存储数据地方
  state: () => {},
  //处理异步|逻辑地方
  actions: {},
  getters: {},
})
//对外暴露小仓库
export default useUserStore

```

#### 2.2.3 按钮回调

```vue
import useUserStore from "@/store/modules/user";
import { useRouter } from "vue-router";
//引入路由
const $router = useRouter();
let  useStore = useUserStore();

//登录按钮的回调
const login = async () => {

  try {
    //也可以书写.then语法
    await useStore.userLogin(loginForm)
    //编程式导航跳转到展示数据的首页
    $router.push('/')

    ElNotification({
      type: 'success',
      message: '登录成功！',
    })

  } catch (error) {

    ElNotification({
      type: 'error',
      message: (error as Error).message,
    })
  }
}
```

#### 2.2.4 用户仓库

```vue
//创建用户相关的小仓库
import { defineStore } from 'pinia'
import { reqLogin } from '@/api/user'
import type { loginForm } from '@/api/user/type'
//创建用户小仓库
const useUserStore = defineStore('User', {
  state: () => {
    return {
      token: localStorage.getItem('TOKEN'),
    }
  },
  //处理异步|逻辑地方
  actions: {
    async userLogin(data: loginForm) {
      const result: any = await reqLogin(data)
      if (result.code == 200) {
        this.token = result.data.token
        localStorage.setItem('TOKEN', result.data.token)
        return 'ok'
      } else {
        return Promise.reject(new Error(result.data.message))
      }
    },
  },
  getters: {},
})

export default useUserStore

```

#### 2.2.5 小结

1. Element-plus中**ElNotification用法（弹窗）：**

引入：`import { ElNotification } from 'element-plus'`

使用：

```vue
//登录失败的提示信息
    ElNotification({
      type: 'error',
      message: (error as Error).message,
    })
```

2. Element-plus中**el-button**的**loading属性。**
3. $router的使用：也需要**引入函数**和**创建实例**
4. 在actions中使用state的token数据:**this.token**



### 2.3模板封装登陆业务

#### 2.3.1 result返回类型封装

```typescript
interface dataType {
  token?: string
  message?: string
}

//登录接口返回的数据类型
export interface loginResponseData {
  code: number
  data: dataType
}
```

#### 2.3.2 State仓库类型封装

```typescript
//定义小仓库数据state类型
export interface UserState {
  token: string | null
}

```

#### 2.3.3 本地存储封装

将本地存储的方法封装到一起

```typescript
//封装本地存储存储数据与读取数据方法
export const SET_TOKEN = (token: string) => {
  localStorage.setItem('TOKEN', token)
}

export const GET_TOKEN = () => {
  return localStorage.getItem('TOKEN')
}

```

### 2.4 登录时间的判断

1. 封装函数

```typescript
//封装函数：获取当前时间段
export const getTime = () => {
  let message = ''
  //通过内置构造函数Date
  const hour = new Date().getHours()
  if (hour <= 9) {
    message = '早上'
  } else if (hour <= 14) {
    message = '上午'
  } else if (hour <= 18) {
    message = '下午'
  } else {
    message = '晚上'
  }
  return message
}

```

2. 使用（引入后）

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686122767173-77bfa222-5a60-41ab-9240-29a1f69a2a0e-634087.png)

3. 效果

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686122788767-d980a39e-c5c2-4d05-bd40-c6ec9473ad79-409623.png)

### 2.5 表单校验规则

#### 2.5.1 表单校验

1. 表单绑定项

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686127043860-132dd02f-5b6e-4837-9558-285a2837dee3-808684.png)

**:model：**绑定的数据

```typescript
//收集账号与密码数据
let loginForm = reactive({ username: 'admin', password: '111111' })
```

**:rules**：对应要使用的规则

```typescript
//定义表单校验需要的配置对象
const rules = {}
```

**ref="loginForms"**：获取表单元素

```typescript
//获取表单元素
let loginForms = ref()
```

2. 表单元素绑定项

<font style="color:rgb(255, 49, 51);">Form 组件提供了表单验证的功能，只需为 rules 属性传入约定的验证规则，并将 form-Item 的 prop 属性设置为需要验证的特殊键值即可</font>

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686127373932-7d3aec5f-e8a5-4052-a6e7-6f02964a18be-024835.png)

3. **使用规则rules**

```typescript
//定义表单校验需要的配置对象
const rules = {
  username: [
    //规则对象属性:
    {
      required: true, // required,代表这个字段务必要校验的
      min: 5, //min:文本长度至少多少位
      max: 10, // max:文本长度最多多少位
      message: '长度应为6-10位', // message:错误的提示信息
      trigger: 'blur', //trigger:触发校验表单的时机 change->文本发生变化触发校验, blur:失去焦点的时候触发校验规则
    }, 
    
  ],
  password: [
   {
      required: true,
      min: 6,
      max: 10,
      message: '长度应为6-15位',
      trigger: 'change',
    }, 
  ],
}
```

4. 校验规则通过后运行

```typescript
const login = async () => {
  //保证全部表单项校验通过
  await loginForms.value.validate()
	。。。。。。
}
```

#### 2.5.2自定义表单校验

1. **修改使用规则rules**

使用自己编写的函数作为规则校验。

```typescript
//定义表单校验需要的配置对象
const rules = {
  username: [
    { trigger: 'change', validator: validatorUserName },
  ],
  password: [
    { trigger: 'change', validator: validatorPassword },
  ],
}
```

2. **自定义校验规则函数**

```typescript
//自定义校验规则函数
const validatorUserName = (rule: any, value: any, callback: any) => {
  //rule：校验规则对象
  //value:表单元素文本内容
  //callback:符合条件，callback放行通过，不符合：注入错误提示信息
  if (value.length >= 5) {
    callback()
  } else {
    callback(new Error('账号长度至少5位'))
  }
}

const validatorPassword = (rule: any, value: any, callback: any) => {
  if (value.length >= 6) {
    callback()
  } else {
    callback(new Error('密码长度至少6位'))
  }
}
```

## 3. Layout模块（主界面）

### 3.1 组件的静态页面

#### 3.1.1 组件的静态页面

注意：我们将主界面单独放一个文件夹（顶替原来的home路由组件）。注意修改一下路由配置

```typescript
<template>
  <div class="layout_container">
    <!-- 左侧菜单 -->
    <div class="layout_slider"></div>
    <!-- 顶部导航 -->
    <div class="layout_tabbar"></div>
    <!-- 内容展示区域 -->
    <div class="layout_main">
      <p style="height: 1000000px"></p>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.layout_container {
  width: 100%;
  height: 100vh;
  .layout_slider {
    width: $base-menu-width;
    height: 100vh;
    background: $base-menu-background;
  }
  .layout_tabbar {
    position: fixed;
    width: calc(100% - $base-menu-width);
    height: $base-tabbar-height;
    background: cyan;
    top: 0;
    left: $base-menu-width;
  }
  .layout_main {
    position: absolute;
    width: calc(100% - $base-menu-width);
    height: calc(100vh - $base-tabbar-height);
    background-color: yellowgreen;
    left: $base-menu-width;
    top: $base-tabbar-height;
    padding: 20px;
    overflow: auto;
  }
}
</style>

```

#### 3.1.2定义部分全局变量&滚动条

**scss全局变量**

```typescript
//左侧菜单宽度
$base-menu-width :260px;
//左侧菜单背景颜色
$base-menu-background: #001529;

//顶部导航的高度
$base-tabbar-height:50px;
```

**滚动条**

```css
//滚动条外观设置

::-webkit-scrollbar{
  width: 10px;
}

::-webkit-scrollbar-track{
  background: $base-menu-background;
}

::-webkit-scrollbar-thumb{
  width: 10px;
  background-color: yellowgreen;
  border-radius: 10px;
}
```

### 3.2 Logo子组件的搭建

页面左上角的这部分，我们将它做成子组件，并且封装方便维护以及修改。

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/9e4e2e2dba3af879c63584d5496f578f.png)

#### 3.2.1 Logo子组件

在这里我们引用了封装好的**setting**

```vue
<template>
  <div class="logo" v-if="setting.logoHidden">
    <img :src="setting.logo" alt="" />
    <p>{{ setting.title }}</p>
  </div>
</template>

<script setup lang="ts">
  //引入设置标题与logo配置文件
  import setting from '@/setting'
</script>

<style lang="scss" scoped>
  .logo {
    width: 100%;
    height: $base-menu-logo-height;
    color: white;
    display: flex;
    align-items: center;
    padding: 20px;
    img {
      width: 40px;
      height: 40px;
    }
    p {
      font-size: $base-logo-title-fontSize;
      margin-left: 10px;
    }
  }
</style>

```

#### 3.2.2 封装setting

为了方便我们以后对logo以及标题的修改。

```typescript
//用于项目logo|标题配置
export default {
  title: 'vue-admin', //项目的标题
  logo: '/public/logo.png', //项目logo设置
  logoHidden: false, //logo组件是否隐藏
}

```

#### 3.2.3 使用

在layout组件中引入并使用

### 3.3 左侧菜单组件

#### 3.3.1静态页面（未封装）

主要使用到了element-plus的**menu组件。**附带使用了滚动组件

```html
<!-- 左侧菜单 -->
<div class="layout_slider">
  <Logo></Logo>
  <!-- 展示菜单 -->
  <!-- 滚动组件 -->
  <el-scrollbar class="scrollbar">
    <!-- 菜单组件 -->
    <el-menu background-color="#001529" text-color="white">
      <el-menu-item index="1">首页</el-menu-item>
      <el-menu-item index="2">数据大屏</el-menu-item>
      <!-- 折叠菜单 -->
      <el-sub-menu index="3">
        <template #title>
          <span>权限管理</span>
        </template>
        <el-menu-item index="3-1">用户管理</el-menu-item>
        <el-menu-item index="3-2">角色管理</el-menu-item>
        <el-menu-item index="3-3">菜单管理</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </el-scrollbar>
</div>
```

#### 3.3.2 递归组件生成动态菜单

在这一部分，我们要**根据路由**生成左侧的菜单栏

1. 将**父组件**中写好的子组件结构提取出去

```html
      <!-- 展示菜单 -->
      <!-- 滚动组件 -->
      <el-scrollbar class="scrollbar">
        <!-- 菜单组件 -->
        <el-menu background-color="#001529" text-color="white">
          <!-- 更具路由动态生成菜单 -->
          <Menu></Menu>
        </el-menu>
      </el-scrollbar>
```

2. 动态菜单**子组件：src\layout\menu\index.vue**
3. **处理路由**

> 因为我们要根据路由以及其子路由作为我们菜单的一级|二级标题。因此我们要获取路由信息。

给路由中加入了路由元信息meta：它包含了2个属性：title以及hidden

```typescript
{
  //登录路由
  path: '/login',
    component: () => import('@/views/login/index.vue'),
    name: 'login', //命名路由
    meta: {
    	title: '登录', //菜单标题
      hidden: true, //路由的标题在菜单中是否隐藏
      },
      },
```

4. 仓库引入路由并对路由信息类型声明（vue-router有对应函数）

```typescript
//引入路由（常量路由）
import { constantRoute } from '@/router/routes'
。。。。。
//小仓库存储数据地方
state: (): UserState => {
  return {
    token: GET_TOKEN(), //用户唯一标识token
    menuRoutes: constantRoute, //仓库存储生成菜单需要数组（路由）
}

```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686191956140-28ec5710-ef14-41f9-90b9-ed286b3acb0b-233050.png)

5. 父组件拿到仓库路由信息并传递给子组件

```typescript
<script setup lang="ts">
。。。。。。
//引入菜单组件
import Menu from './menu/index.vue'
//获取用户相关的小仓库
import useUserStore from '@/store/modules/user'
let userStore = useUserStore()
</script>
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686191898567-791e2795-0607-4b97-a2e9-721017912d79-579956.png)

6. 子组件prps接收并且处理结构

```typescript
<template>
  <template v-for="(item, index) in menuList" :key="item.path">
    <!-- 没有子路由 -->
    <template v-if="!item.children">
      <el-menu-item v-if="!item.meta.hidden" :index="item.path">
        <template #title>
          <span>标</span>
          <span>{{ item.meta.title }}</span>
        </template>
      </el-menu-item>
    </template>
    <!-- 有且只有一个子路由 -->
    <template v-if="item.children && item.children.length == 1">
      <el-menu-item
        index="item.children[0].path"
        v-if="!item.children[0].meta.hidden"
      >
        <template #title>
          <span>标</span>
          <span>{{ item.children[0].meta.title }}</span>
        </template>
      </el-menu-item>
    </template>
    <!-- 有子路由且个数大于一个 -->
    <el-sub-menu
      :index="item.path"
      v-if="item.children && item.children.length >= 2"
    >
      <template #title>
        <span>{{ item.meta.title }}</span>
      </template>
      <Menu :menuList="item.children"></Menu>
    </el-sub-menu>
  </template>
</template>

<script setup lang="ts">
//获取父组件传递过来的全部路由数组
defineProps(['menuList'])
</script>
<script lang="ts">
export default {
  name: 'Menu',
}
</script>
<style lang="scss" scoped></style>

```

注意：

1：因为每一个项我们要判断俩次（是否要隐藏，以及子组件个数），所以在el-menu-item外面又套了一层模板

2：当子路由个数大于等于一个时，并且或许子路由还有后代路由时。这里我们使用了递归组件。递归组件需要命名（另外使用一个script标签，vue2格式）。

#### 3.3.3 菜单图标

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686193507312-cb774e31-030d-4bfa-a544-91393e62682c-209657.png)

1. 注册图标组件

因为我们要根据路由配置对应的图标，也要为了后续方便更改。因此我们将所有的图标注册为全局组件。（使用之前将分页器以及矢量图注册全局组件的**自定义插件**）（所有图标全局注册的方法element-plus文档中已给出）

```typescript
。。。。。。
//引入element-plus提供全部图标组件
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
。。。。。。

//对外暴露插件对象
export default {
  //必须叫做install方法
  //会接收我们的app
 。。。。。。
  //将element-plus提供全部图标注册为全局组件 
    for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
      app.component(key, component)
    }
  },
}

```

2. 给路由元信息添加属性：**icon**

以laytou和其子组件为例**：**首先在element-puls找到你要使用的图标的名字。将它添加到**路由元信息的icon属性**上

```typescript
  {
    //登录成功以后展示数据的路由
    path: '/',
    component: () => import('@/layout/index.vue'),
    name: 'layout',
    meta: {
      title: 'layout',
      hidden: false,
      icon: 'Avatar',
    },
    children: [
      {
        path: '/home',
        component: () => import('@/views/home/index.vue'),
        meta: {
          title: '首页',
          hidden: false,
          icon: 'HomeFilled',
        },
      },
    ],
  },
```

3. 菜单组件使用

以只有一个子路由的组件为例：

```html
<!-- 有且只有一个子路由 -->
<template v-if="item.children && item.children.length == 1">
  <el-menu-item
    index="item.children[0].path"
    v-if="!item.children[0].meta.hidden"
    >
    <template #title>
      <el-icon>
        <component :is="item.children[0].meta.icon"></component>
      </el-icon>
      <span>{{ item.children[0].meta.title }}</span>
    </template>
  </el-menu-item>
</template>
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686194065863-596ad954-ee23-4a18-a474-ffd1463ee22a-211560.png)



#### 3.3.4 项目全部路由配置

1. 全部路由配置(以权限管理为例）

```typescript
{
  path: '/acl',
    component: () => import('@/layout/index.vue'),
    name: 'Acl',
    meta: {
    hidden: false,
      title: '权限管理',
      icon: 'Lock',
      },
  children: [
    {
      path: '/acl/user',
      component: () => import('@/views/acl/user/index.vue'),
      name: 'User',
      meta: {
        hidden: false,
        title: '用户管理',
        icon: 'User',
      },
    },
    {
      path: '/acl/role',
      component: () => import('@/views/acl/role/index.vue'),
      name: 'Role',
      meta: {
        hidden: false,
        title: '角色管理',
        icon: 'UserFilled',
      },
    },
    {
      path: '/acl/permission',
      component: () => import('@/views/acl/permission/index.vue'),
      name: 'Permission',
      meta: {
        hidden: false,
        title: '菜单管理',
        icon: 'Monitor',
      },
    },
  ],
    },
```

2. 添加路由跳转函数

第三种情况我们使用组件递归，所以只需要给前面的2个添加函数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686208640889-f07be40f-c24b-4da2-8670-491198582793-886048.png)

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686208624808-082f190b-97d3-4c2f-b235-b1f7e1f3d9ff-036398.png)

```typescript
<script setup lang="ts">
。。。。。。
//获取路由器对象
let $router = useRouter()
const goRoute = (vc: any) => {
  //路由跳转
  $router.push(vc.index)
}
</script>
```

3. **layout组件**

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/1686208781007-19ff2e08-34e8-4831-88d3-59f57fc2bcc7-802193.png)

#### 3.3.5 动画 && 自动展示

1. 将router-link封装成单独的文件并且添加一些动画

```vue
<template>
  <!-- 路由组件出口的位置 -->
  <router-view v-slot="{ Component }">
    <transition name="fade">
      <!-- 渲染layout一级路由的子路由 -->
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
  .fade-enter-from {
    opacity: 0;
  }
  .fade-enter-active {
    transition: all 0.3s;
  }
  .fade-enter-to {
    opacity: 1;
  }
</style>

```

2. 自动展示

当页面刷新时，菜单会自动收起。我们使用element-plus的**default-active **处理。$router.path为当前路由。

`src\layout\index.vue`

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/f26f11f90c574709c5f8cd6f8ce6d309.png)

### 3.4 顶部tabbar组件

#### 3.4.1静态页面

element-plus：**breadcrumb el-button el-dropdown**

```vue
<template>
  <div class="tabbar">
    <div class="tabbar_left">
      <!-- 顶部左侧的图标 -->
      <el-icon style="margin-right: 10px">
        <Expand></Expand>
      </el-icon>
      <!-- 左侧的面包屑 -->
      <el-breadcrumb separator-icon="ArrowRight">
        <el-breadcrumb-item>权限挂历</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="tabbar_right">
      <el-button size="small" icon="Refresh" circle></el-button>
      <el-button size="small" icon="FullScreen" circle></el-button>
      <el-button size="small" icon="Setting" circle></el-button>
      <img
        src="/public/logo.jpg"
        style="width: 24px; height: 24px; margin: 0px 10px"
      />
      <!-- 下拉菜单 -->
      <el-dropdown>
        <span class="el-dropdown-link">
          admin
          <el-icon class="el-icon--right">
            <arrow-down />
          </el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>退出登陆</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.tabbar {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  background-image: linear-gradient(
    to right,
    rgb(236, 229, 229),
    rgb(151, 136, 136),
    rgb(240, 234, 234)
  );
  .tabbar_left {
    display: flex;
    align-items: center;
    margin-left: 20px;
  }
  .tabbar_right {
    display: flex;
    align-items: center;
  }
}
</style>

```

**组件拆分：**

```vue
<template>
  <!-- 顶部左侧的图标 -->
  <el-icon style="margin-right: 10px">
    <Expand></Expand>
  </el-icon>
  <!-- 左侧的面包屑 -->
  <el-breadcrumb separator-icon="ArrowRight">
    <el-breadcrumb-item>权限挂历</el-breadcrumb-item>
    <el-breadcrumb-item>用户管理</el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped></style>

```

```vue
<template>
  <el-button size="small" icon="Refresh" circle></el-button>
  <el-button size="small" icon="FullScreen" circle></el-button>
  <el-button size="small" icon="Setting" circle></el-button>
  <img
    src="/public/logo.jpg"
    style="width: 24px; height: 24px; margin: 0px 10px"
  />
  <!-- 下拉菜单 -->
  <el-dropdown>
    <span class="el-dropdown-link">
      admin
      <el-icon class="el-icon--right">
        <arrow-down />
      </el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>退出登陆</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped></style>

```

#### 3.4.2 菜单折叠

1. 折叠变量

> 定义一个折叠变量来判断现在的状态是否折叠。因为这个变量同时给breadcrumb组件以及父组件layout使用，因此将这个变量定义在pinia中

```vue
//小仓库：layout组件相关配置仓库
import { defineStore } from 'pinia'

let useLayOutSettingStore = defineStore('SettingStore', {
  state: () => {
    return {
      fold: false, //用户控制菜单折叠还是收起的控制
    }
  },
})

export default useLayOutSettingStore

```

2. 面包屑组件点击图标切换状态

```vue
<template>
  <!-- 顶部左侧的图标 -->
  <el-icon style="margin-right: 10px" @click="changeIcon">
    <component :is="LayOutSettingStore.fold ? 'Fold' : 'Expand'"></component>
  </el-icon>
  。。。。。。。
</template>

<script setup lang="ts">
import useLayOutSettingStore from '@/store/modules/setting'
//获取layout配置相关的仓库
let LayOutSettingStore = useLayOutSettingStore()

//点击图标的切换
const changeIcon = () => {
  //图标进行切换
  LayOutSettingStore.fold = !LayOutSettingStore.fold
}
</script>
。。。。。。

```

3. layout组件根据fold状态来修改个子组件的样式（以左侧菜单为例）

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/ed13d9b2fc032a13a1d6df7819a9b42f.png)

绑定动态样式修改scss

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/6c7a8f0b78efc67e45a514a7c90f0850.png)

其他组件也需要进行变动

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/703c3cbd8a3ac924f571fd44db5440b1.png)

4. 左侧菜单使用element-plus**折叠collapse**属性

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420123805.png)

**效果图：**

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420123820.png)

注意：折叠文字的时候会把图标也折叠起来。在menu组件中吧图标放到template外面就可以。

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420123834.png)



#### 3.4.3 顶部面包屑动态展示

1. 引入$route

注意$router和$route是不一样的

```vue
<script setup lang="ts">
import { useRoute } from 'vue-router'
//获取路由对象
let $route = useRoute()
//点击图标的切换

</script>
```

2. 结构展示

注意：使用了$route.matched函数，此函数能得到当前路由的信息

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420123847.png)

3. 首页修改

访问首页时，因为它是二级路由，会遍历出layout面包屑，处理：删除layout路由的title。再加上一个判断

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420124003.png)

4. 面包屑点击跳转

注意：将路由中的一级路由**权限管理**以及**商品管理**重定向到第一个孩子，这样点击跳转的时候会定向到第一个孩子。

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420124021.png)



#### 3.4.4 刷新业务的实现

1. 使用pinia定义一个变量作为标记

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420124032.png)

2. 点击刷新按钮，修改标记

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420124046.png)

```vue
<script setup lang="ts">
//使用layout的小仓库
import useLayOutSettingStore from '@/store/modules/setting'
let layoutSettingStore = useLayOutSettingStore()
//刷新按钮点击的回调
const updateRefresh = () => {
  layoutSettingStore.refresh = !layoutSettingStore.refresh
}
</script>
```

3. main组件检测标记销毁&重加载组件（**nextTick**）

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420124218.png)

```vue
<script setup lang="ts">
import { watch, ref, nextTick } from 'vue'
//使用layout的小仓库
import useLayOutSettingStore from '@/store/modules/setting'
let layOutSettingStore = useLayOutSettingStore()
//控制当前组件是否销毁重建
let flag = ref(true)
//监听仓库内部的数据是否发生变化，如果发生变化，说明用户点击过刷新按钮
watch(
  () => layOutSettingStore.refresh,
  () => {
    //点击刷新按钮：路由组件销毁
    flag.value = false
    nextTick(() => {
      flag.value = true
    })
  },
)
</script>
```

#### 3.4.5 全屏模式的实现

1. 给全屏按钮绑定函数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250420124231.png)

2. 实现全屏效果（利用docment根节点的方法）

```vue
//全屏按钮点击的回调
const fullScreen = () => {
  //DOM对象的一个属性：可以用来判断当前是不是全屏的模式【全屏：true，不是全屏：false】
  let full = document.fullscreenElement
  //切换成全屏
  if (!full) {
    //文档根节点的方法requestFullscreen实现全屏
    document.documentElement.requestFullscreen()
  } else {
    //退出全屏
    document.exitFullscreen()
  }
```

## 4.部分功能处理完善

### 4.1 登录获取用户信息（TOKEN）

> 登录之后页面（home）上来就要获取用户信息。并且将它使用到页面中

1. home组件挂载获取用户信息

```vue
<script setup lang="ts">
//引入组合是API生命周期函数
import { onMounted } from 'vue'
import useUserStore from '@/store/modules/user'
let userStore = useUserStore()
onMounted(() => {
  userStore.userInfo()
})
</script>
```

2. 小仓库中定义用户信息以及type声明

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422121502.png)

```vue
import type { RouteRecordRaw } from 'vue-router'
//定义小仓库数据state类型
export interface UserState {
  token: string | null
  menuRoutes: RouteRecordRaw[]
  username: string
  avatar: string
}

```

3. **请求头添加TOKEN**

```vue
//引入用户相关的仓库
import useUserStore from '@/store/modules/user'
    。。。。。。
//请求拦截器
request.interceptors.request.use((config) => {
  //获取用户相关的小仓库，获取token，登录成功以后携带个i服务器
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.token = userStore.token
  }
  //config配置对象，headers请求头，经常给服务器端携带公共参数
  //返回配置对象
  return config
})
```

4. 小仓库发请求并且拿到用户信息

```vue
    //获取用户信息方法
    async userInfo() {
      //获取用户信息进行存储
      let result = await reqUserInfo()
      if (result.code == 200) {
        this.username = result.data.checkUser.username
        this.avatar = result.data.checkUser.avatar
      }
    },
```

5. 更新tabbar的信息（记得先引入并创建实例）

`src\layout\tabbar\setting\index.vue`

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422121538.png)

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422121551.png)



### 4.2 退出功能

1. 退出登录绑定函数，调用仓库函数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422121603.png)

```vue
//退出登陆点击的回调
const logout = () => {
  //第一件事：需要项服务器发请求【退出登录接口】（我们这里没有）
  //第二件事：仓库当中和关于用户的相关的数据清空
  userStore.userLogout()
  //第三件事：跳转到登陆页面
}
```

2. pinia仓库

```vue
    //退出登录
    userLogout() {
      //当前没有mock接口（不做）：服务器数据token失效
      //本地数据清空
      this.token = ''
      this.username = ''
      this.avatar = ''
      REMOVE_TOKEN()
    },
```

3. 退出登录，路由跳转

注意:携带的query参数方便下次登陆时直接跳转到当时推出的界面

个人觉得这个功能没什么作用。但是可以学习方法

```vue
//退出登陆点击的回调
const logout = () => {
  //第一件事：需要项服务器发请求【退出登录接口】（我们这里没有）
  //第二件事：仓库当中和关于用户的相关的数据清空
  userStore.userLogout()
  //第三件事：跳转到登陆页面
  $router.push({ path: '/login', query: { redirect: $route.path } })
}
```

4. 登录按钮进行判断

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422121627.png)

### 4.3 路由守卫

`src\permisstion.ts`（新建文件）

main.ts引入

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422121640.png)

#### 4.3.1 进度条

1. 安装

` pnpm i nprogress`

2. 引入并使用

```vue
//路由鉴权：鉴权：项目当中路由能不能被访问的权限
import router from '@/router'
import nprogress from 'nprogress'
//引入进度条样式
import 'nprogress/nprogress.css'
//全局前置守卫
router.beforeEach((to: any, from: any, next: any) => {
  //访问某一个路由之前的守卫
  nprogress.start()
  next()
})

//全局后置守卫
router.afterEach((to: any, from: any) => {
  // to and from are both route objects.
  nprogress.done()
})

//第一个问题：任意路由切换实现进度条业务 ----nprogress

```

#### 4.3.2 路由鉴权

```vue
//路由鉴权：鉴权：项目当中路由能不能被访问的权限
import router from '@/router'
import setting from './setting'
import nprogress from 'nprogress'
//引入进度条样式
import 'nprogress/nprogress.css'
//进度条的加载圆圈不要
nprogress.configure({ showSpinner: false })
//获取用户相关的小仓库内部token数据，去判断用户是否登陆成功
import useUserStore from './store/modules/user'
//为什么要引pinia
import pinia from './store'
const userStore = useUserStore(pinia)

//全局前置守卫
router.beforeEach(async (to: any, from: any, next: any) => {
  //网页的名字
  document.title = `${setting.title}-${to.meta.title}`
  //访问某一个路由之前的守卫
  nprogress.start()
  //获取token，去判断用户登录、还是未登录
  const token = userStore.token
  //获取用户名字
  let username = userStore.username
  //用户登录判断
  if (token) {
    //登陆成功，访问login。指向首页
    if (to.path == '/login') {
      next('/home')
    } else {
      //登陆成功访问其余的，放行
      //有用户信息
      if (username) {
        //放行
        next()
      } else {
        //如果没有用户信息，在收尾这里发请求获取到了用户信息再放行
        try {
          //获取用户信息
          await userStore.userInfo()
          next()
        } catch (error) {
          //token过期|用户手动处理token
          //退出登陆->用户相关的数据清空
          userStore.userLogout()
          next({ path: '/login', query: { redirect: to.path } })
        }
      }
    }
  } else {
    //用户未登录
    if (to.path == '/login') {
      next()
    } else {
      next({ path: '/login', query: { redirect: to.path } })
    }
  }
  next()
})

//全局后置守卫
router.afterEach((to: any, from: any) => {
  // to and from are both route objects.
  nprogress.done()
})

//第一个问题：任意路由切换实现进度条业务 ----nprogress
//第二个问题：路由鉴权
//全部路由组件 ：登录|404|任意路由|首页|数据大屏|权限管理（三个子路由）|商品管理（4个子路由）

//用户未登录 ：可以访问login 其余都不行
//登陆成功：不可以访问login 其余都可以

```

**路由鉴权几个注意点**：

1. 获取用户小仓库为什么要导入pinia？

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422121703.png)

答案：pinia 本质上是通过 `app.use(pinia)`*把这个上下文注入到了 Vue 的“依赖注入系统”中，所以你在组件里能直接用 `useUserStore()`。但在 `route.ts` 这种 **脱离组件上下文** 的文件中，`useUserStore()` 默认无法拿到上下文

2. 全局路由守卫将获取用户信息的请求放在了跳转之前。实现了刷新后用户信息丢失的功能。



### 4.4 真实接口替代mock接口

1. 修改服务器域名

将.env.development，.env.production  .env.test，三个环境文件下的服务器域名写为：

![1686307539467-b5f7ec90-a237-4e69-9f8c-0bdd98739ce9.png](vue3-管理平台学习笔记.assets/1686307539467-b5f7ec90-a237-4e69-9f8c-0bdd98739ce9-114129.png)

2. 代理跨域

```vue
import { loadEnv } from 'vite'
。。。。。。
export default defineConfig(({ command, mode }) => {
  //获取各种环境下的对应的变量
  let env = loadEnv(mode, process.cwd())
  return {
    。。。。。。。
    //代理跨域
    server: {
      proxy: {
        [env.VITE_APP_BASE_API]: {
          //获取数据服务器地址的设置
          target: env.VITE_SERVE,
          //需要代理跨域
          changeOrigin: true,
          //路径重写
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  }
})

```

3. 修改api

在这里退出登录有了自己的api

```vue
//统一管理项目用户相关的接口
import request from '@/utils/request'

//项目用户相关的请求地址
enum API {
  LOGIN_URL = '/admin/acl/index/login',
  USERINFO_URL = '/admin/acl/index/info',
  LOGOUT_URL = '/admin/acl/index/logout',
}
//对外暴露请求函数
//登录接口方法
export const reqLogin = (data: any) => {
  return request.post<any, any>(API.LOGIN_URL, data)
}

//获取用户信息接口方法
export const reqUserInfo = () => {
  return request.get<any, any>(API.USERINFO_URL)
}

//退出登录
export const reqLogout = () => {
  return request.post<any, any>(API.LOGOUT_URL)
}

```

4. 小仓库（user）

替换原有的请求接口函数，以及修改退出登录函数。以及之前引入的类型显示我们展示都设置为any

```vue
//创建用户相关的小仓库
import { defineStore } from 'pinia'
//引入接口
import { reqLogin, reqUserInfo, reqLogout } from '@/api/user'
import type { UserState } from './types/type'
//引入操作本地存储的工具方法
import { SET_TOKEN, GET_TOKEN, REMOVE_TOKEN } from '@/utils/token'
//引入路由（常量路由）
import { constantRoute } from '@/router/routes'

//创建用户小仓库
const useUserStore = defineStore('User', {
  //小仓库存储数据地方
  state: (): UserState => {
    return {
      token: GET_TOKEN(), //用户唯一标识token
      menuRoutes: constantRoute, //仓库存储生成菜单需要数组（路由）
      username: '',
      avatar: '',
    }
  },
  //处理异步|逻辑地方
  actions: {
    //用户登录的方法
    async userLogin(data: any) {
      //登录请求
      const result: any = await reqLogin(data)

      if (result.code == 200) {
        //pinia仓库存储token
        //由于pinia|vuex存储数据其实利用js对象
        this.token = result.data as string
        //本地存储持久化存储一份
        SET_TOKEN(result.data as string)
        //保证当前async函数返回一个成功的promise函数
        return 'ok'
      } else {
        return Promise.reject(new Error(result.data))
      }
    },
    //获取用户信息方法
    async userInfo() {
      //获取用户信息进行存储
      const result = await reqUserInfo()
      console.log(result)

      if (result.code == 200) {
        this.username = result.data.name
        this.avatar = result.data.avatar
        return 'ok'
      } else {
        return Promise.reject(new Error(result.message))
      }
    },
    //退出登录
    async userLogout() {
      const result = await reqLogout()
      if (result.code == 200) {
        //本地数据清空
        this.token = ''
        this.username = ''
        this.avatar = ''
        REMOVE_TOKEN()
        return 'ok'
      } else {
        return Promise.reject(new Error(result.message))
      }
    },
  },
  getters: {},
})
//对外暴露小仓库
export default useUserStore

```



5. **退出登录**按钮的点击函数修改

退出成功后再跳转

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122157.png)

6. 路由跳转判断条件修改

`src\permisstion.ts`

也是退出成功后再跳转

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122209.png)

### 4.5 接口类型定义

```vue
//登录接口需要携带参数类型
export interface loginFormData {
  username: string
  password: string
}

//定义全部接口返回数据都有的数据类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
//定义登录接口返回数据类型
export interface loginResponseData extends ResponseData {
  data: string
}

//定义获取用户信息返回的数据类型
export interface userInfoResponseData extends ResponseData {
  data: {
    routes: string[]
    button: string[]
    roles: string[]
    name: string
    avatar: string
  }
}

```

注意：在src\store\modules\user.ts以及src\api\user\index.ts文件中对发请求时的参数以及返回的数据添加类型定义

## 5.品牌管理模块

### 5.1 静态组件

使用element-plus。

```vue
<template>
  <el-card class="box-card">
    <!-- 卡片顶部添加品牌按钮 -->
    <el-button type="primary" size="default" icon="Plus">添加品牌</el-button>
    <!-- 表格组件，用于展示已有的数据 -->
    <!-- 
      table
      ---border:是否有纵向的边框
      table-column
      ---lable：某一个列表
      ---width：设置这一列的宽度
      ---align：设置这一列对齐方式
     -->
    <el-table style="margin: 10px 0px" border>
      <el-table-column
        label="序号"
        width="80px"
        align="center"
      ></el-table-column>
      <el-table-column label="品牌名称"></el-table-column>
      <el-table-column label="品牌LOGO"></el-table-column>
      <el-table-column label="品牌操作"></el-table-column>
    </el-table>
    <!-- 分页器组件 -->
    <!-- 
      pagination
      ---v-model:current-page：设置当前分页器页码
      ---v-model:page-size:设置每一也展示数据条数
      ---page-sizes：每页显示个数选择器的选项设置
      ---background:背景颜色
      ---layout：分页器6个子组件布局的调整 "->"把后面的子组件顶到右侧
     -->
    <el-pagination
      v-model:current-page="pageNo"
      v-model:page-size="limit"
      :page-sizes="[3, 5, 7, 9]"
      :background="true"
      layout=" prev, pager, next, jumper,->,total, sizes,"
      :total="400"
    />
  </el-card>
</template>

<script setup lang="ts">
//引入组合式API函数
import { ref } from 'vue'
//当前页码
let pageNo = ref<number>(1)
//每一页展示的数据
let limit = ref<number>(3)
</script>

<style lang="scss" scoped></style>

```

### 5.2 数据模块

#### 5.2.1 API

1. api函数

```vue
//书写品牌管理模块接口
import request from '@/utils/request'
//品牌管理模块接口地址
enum API {
  //获取已有品牌接口
  TRADEMARK_URL = '/admin/product/baseTrademark/',
}
//获取一样偶品牌的接口方法
//page:获取第几页 ---默认第一页
//limit:获取几个已有品牌的数据
export const reqHasTrademark = (page: number, limit: number) =>
  request.get<any, any>(API.TRADEMARK_URL + `${page}/${limit}`)

```

2. 获取数据

我们获取数据没有放在pinia中，二是放在组件中挂载时获取数据

```vue
<script setup lang="ts">
import { reqHasTrademark } from '@/api/product/trademark'
//引入组合式API函数
import { ref, onMounted } from 'vue'
//当前页码
let pageNo = ref<number>(1)
//每一页展示的数据
let limit = ref<number>(3)
//存储已有品牌数据总数
let total = ref<number>(0)
//存储已有品牌的数据
let trademarkArr = ref<any>([])
//获取已有品牌的接口封装为一个函数:在任何情况下向获取数据,调用次函数即可
const getHasTrademark = async (pager = 1) => {
  //当前页码
  pageNo.value = pager
  let result = await reqHasTrademark(pageNo.value, limit.value)
  console.log(result)
  if (result.code == 200) {
    //存储已有品牌总个数
    total.value = result.data.total
    trademarkArr.value = result.data.records
    console.log(trademarkArr)
    
  }
}
//组件挂载完毕钩子---发一次请求,获取第一页、一页三个已有品牌数据
onMounted(() => {
  getHasTrademark()
})
</script>
```

#### 5.2.2 数据展示

在数据展示模块，我们使用了element-plus的**el-table，**下面组要讲解属性和注意点。

1. data属性：显示的数据

比如我们这里绑定的trademarkArr是个三个对象的数组，就会多出来3行。![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122422.png)

2. el-table-column的type属性：<font style="color:rgb(255, 49, 51);">对应列的类型。 如果设置了selection则显示多选框； 如果设置了 index 则显示该行的索引（从 1 开始计算）； 如果设置了 expand 则显示为一个可展开的按钮</font>

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122434.png)

3. el-table-column的prop属性：<font style="color:rgb(255, 49, 51);">字段名称 对应列内容的字段名， 也可以使用 property属性</font>

注意：因为我们之前已经绑定了数据，所以在这里直接使用数据的属性tmName

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122448.png)

4. el-table-column的插槽

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122458.png)

为什么要使用插槽呢？因为prop属性虽然能够展示数据，但是他默认是div，如果我们的图片使用prop展示的话，会展示图片的路径。因此如果想展示图片或者按钮，我们就要使用插槽

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122553.png)

注意：row就是我们的trademarkArr的每一个数据（对象）

### 5.3 品牌类型定义

API中的以及组件中。 

```vue
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}

//已有的品牌的ts数据类型
export interface TradeMark {
  id?: number
  tmName: string
  logoUrl: string
}

//包含全部品牌数据的ts类型
export type Records = TradeMark[]

//获取的已有全部品牌的数据ts类型
export interface TradeMarkResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    size: number
    current: number
    searchCount: boolean
    pages: number
  }
}

```

### 5.4 分页展示数据

> 此部分主要是俩个功能，第一个是当点击分页器页数时能跳转到对应的页数。第二个是每页展示的数据条数能正确显示

#### 5.4.1 跳转页数函数

这里我们绑定的点击回调直接用的是之前写好的发送请求的回调。可以看出，发送请求的回调函数是有默认的参数：1.

**注意**：因为current-change方法时element-plus封装好的，它会给父组件传递并注入一个参数（点击的页码），所以相当于把这个参数传递给了getHasTrademark函数，因此能够跳转到正确的页码数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122626.png)

```typescript
//获取已有品牌的接口封装为一个函数:在任何情况下向获取数据,调用次函数即可
const getHasTrademark = async (pager = 1) => {
  //当前页码
  pageNo.value = pager
  let result: TradeMarkResponseData = await reqHasTrademark(
    pageNo.value,
    limit.value,
  )
  if (result.code == 200) {
    //存储已有品牌总个数
    total.value = result.data.total
    trademarkArr.value = result.data.records
  }
}
```

#### 5.4.2 每页展示数据条数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122642.png)

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122742.png)

```typescript
//当下拉菜单发生变化的时候触发此方法
//这个自定义事件,分页器组件会将下拉菜单选中数据返回
const sizeChange = () => {
  //当前每一页的数据量发生变化的时候，当前页码归1
  getHasTrademark()
  console.log(123)
}
```

同样的这个函数也会返回一个参数。但是我们不需要使用这个参数，因此才另外写一个回调函数。

### 5.5 dialog对话框静态搭建

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122800.png)

1. 对话框的标题&&显示隐藏

v-model:属性用户控制对话框的显示与隐藏的 true显示 false隐藏

title:设置对话框左上角标题

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122815.png)

2. 表单项

```typescript
    <el-form style="width: 80%">
      <el-form-item label="品牌名称" label-width="100px" prop="tmName">
        <el-input
          placeholder="请您输入品牌名称"
          v-model="trademarkParams.tmName"
        ></el-input>
      </el-form-item>
      <el-form-item label="品牌LOGO" label-width="100px" prop="logoUrl">
        <!-- upload组件属性:action图片上传路径书写/api,代理服务器不发送这次post请求  -->
        <el-upload
          class="avatar-uploader"
          action="/api/admin/product/fileUpload"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <img
            v-if="trademarkParams.logoUrl"
            :src="trademarkParams.logoUrl"
            class="avatar"
          />
          <el-icon v-else class="avatar-uploader-icon">
            <Plus />
          </el-icon>
        </el-upload>
      </el-form-item>
    </el-form>
```

3. 确定与取消按钮

```vue
<template #footer>
  <el-button type="primary" size="default" @click="cancel">取消</el-button>
  <el-button type="primary" size="default" @click="confirm">确定</el-button>
</template>
```

### 5.5 新增品牌数据

#### 5.4.1 API（新增与修改品牌）

因为这2个接口的携带的数据差不多，我们将其写为一个方法

```vue
//书写品牌管理模块接口
import request from '@/utils/request'
import type { TradeMarkResponseData, TradeMark } from './type'
//品牌管理模块接口地址
enum API {
  。。。。。。
  //添加品牌
  ADDTRADEMARK_URL = '/admin/product/baseTrademark/save',
  //修改已有品牌
  UPDATETRADEMARK_URL = '/admin/product/baseTrademark/update',
}
。。。。。。
//添加与修改已有品牌接口方法
export const reqAddOrUpdateTrademark = (data: TradeMark) => {
  //修改已有品牌的数据
  if (data.id) {
    return request.put<any, any>(API.UPDATETRADEMARK_URL, data)
  } else {
    //新增品牌
    return request.post<any, any>(API.ADDTRADEMARK_URL, data)
  }
}

```

#### 5.4.2 收集新增品牌数据

1. 定义数据

```vue
import type {
。。。。。。。
TradeMark,
} from '@/api/product/trademark/type'
//定义收集新增品牌数据
let trademarkParams = reactive<TradeMark>({
  tmName: '',
  logoUrl: '',
})
```

2. 收集品牌名称

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122835.png)

3. upload组件的属性介绍

```vue
<el-upload
          class="avatar-uploader"
          action="/api/admin/product/fileUpload"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <img
            v-if="trademarkParams.logoUrl"
            :src="trademarkParams.logoUrl"
            class="avatar"
          />
          <el-icon v-else class="avatar-uploader-icon">
            <Plus />
          </el-icon>
        </el-upload>
```

**class**：带的一些样式，需复制到style中

**action**：图片上传路径需要书写/api,否则代理服务器不发送这次post请求

**:show-file-list**：是否展示已经上传的文件

**:before-upload：上传图片之前的钩子函数**

```vue
//上传图片组件->上传图片之前触发的钩子函数
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  //钩子是在图片上传成功之前触发,上传文件之前可以约束文件类型与大小
  //要求:上传文件格式png|jpg|gif 4M
  if (
    rawFile.type == 'image/png' ||
    rawFile.type == 'image/jpeg' ||
    rawFile.type == 'image/gif'
  ) {
    if (rawFile.size / 1024 / 1024 < 4) {
      return true
    } else {
      ElMessage({
        type: 'error',
        message: '上传文件大小小于4M',
      })
      return false
    }
  } else {
    ElMessage({
      type: 'error',
      message: '上传文件格式务必PNG|JPG|GIF',
    })
    return false
  }
}
```

**:on-success**：**图片上传成功钩子（收集了上传图片的地址）**

在这里，你将本地的图片上传到之前el-upload组件的action=`"/api/admin/product/fileUpload"`这个地址上，然后**on-success钩子**会将上传后图片的地址返回

```vue
//图片上传成功钩子
const handleAvatarSuccess: UploadProps['onSuccess'] = (
  response,
  uploadFile,
) => {
  //response:即为当前这次上传图片post请求服务器返回的数据
  //收集上传图片的地址,添加一个新的品牌的时候带给服务器
  trademarkParams.logoUrl = response.data
  //图片上传成功,清除掉对应图片校验结果
  formRef.value.clearValidate('logoUrl')
}
```

4. 上传图片后，用图片代替加号

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122853.png)

#### 5.4.3 添加品牌

1. 点击确定按钮回调

```typescript
const confirm = async () => {
  //在你发请求之前,要对于整个表单进行校验
  //调用这个方法进行全部表单相校验,如果校验全部通过，在执行后面的语法
  // await formRef.value.validate()
  let result: any = await reqAddOrUpdateTrademark(trademarkParams)
  //添加|修改已有品牌
  if (result.code == 200) {
    //关闭对话框
    dialogFormVisible.value = false
    //弹出提示信息
    ElMessage({
      type: 'success',
      message: trademarkParams.id ? '修改品牌成功' : '添加品牌成功',
    })
    //再次发请求获取已有全部的品牌数据
    getHasTrademark(trademarkParams.id ? pageNo.value : 1)
  } else {
    //添加品牌失败
    ElMessage({
      type: 'error',
      message: trademarkParams.id ? '修改品牌失败' : '添加品牌失败',
    })
    //关闭对话框
    dialogFormVisible.value = false
  }
}
```

2. 每次点击添加品牌的时候先情况之前的数据

```typescript
//添加品牌按钮的回调
const addTrademark = () => {
  //对话框显示
  dialogFormVisible.value = true
  //清空收集数据
  trademarkParams.tmName = ''
  trademarkParams.logoUrl = ''
}
```

### 5.6 修改品牌数据

1. 绑定点击函数

其中的**row**就是当前的数据

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122907.png)

2. 回调函数

```typescript
//修改已有品牌的按钮的回调
//row:row即为当前已有的品牌
const updateTrademark = (row: TradeMark) => {
  //对话框显示
  dialogFormVisible.value = true
  //ES6语法合并对象
  Object.assign(trademarkParams, row)
}
```

3. 对确认按钮回调修改

```typescript
const confirm = async () => {
  。。。。。。。
  if (result.code == 200) {
   。。。
    //弹出提示信息
    ElMessage({
      。。。。
      message: trademarkParams.id ? '修改品牌成功' : '添加品牌成功',
    })
    //再次发请求获取已有全部的品牌数据
    getHasTrademark(trademarkParams.id ? pageNo.value : 1)
  } else {
    //添加品牌失败
    ElMessage({
      。。。。
      message: trademarkParams.id ? '修改品牌失败' : '添加品牌失败',
    })
    。。。。
  }
}
```

4. 设置对话框标题

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122920.png)

5. 小问题

当我们修改操作之后再点击添加品牌，对话框的title依旧是修改品牌。怎么是因为对话框的title是根据trademarkParams.id来的，我们之前添加品牌按钮操作没有对id进行清除。修改为如下就可

```typescript
//添加品牌按钮的回调
const addTrademark = () => {
  //对话框显示
  dialogFormVisible.value = true
  //清空收集数据
  trademarkParams.id = 0
  trademarkParams.tmName = ''
  trademarkParams.logoUrl = ''
}
```

### 5.7 品牌管理模块表单校验

#### 5.7.1 表单校验（自定义规则校验，可以简略堪称三步走）

1. 绑定参数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122934.png)

:model：校验的数据

:rules：校验规则

ref="formRef"：表单实例

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422122950.png)

prop：表单元素校验的数据，可以直接使用表单绑定的数据。

2. **Rules**

```typescript
//表单校验规则对象
const rules = {
  tmName: [
    //required:这个字段务必校验,表单项前面出来五角星
    //trigger:代表触发校验规则时机[blur、change]
    { required: true, trigger: 'blur', validator: validatorTmName },
  ],
  logoUrl: [{ required: true, validator: validatorLogoUrl }],
}
```

3. **Rules中写的方法**

```typescript
//品牌自定义校验规则方法
const validatorTmName = (rule: any, value: any, callBack: any) => {
  //是当表单元素触发blur时候,会触发此方法
  //自定义校验规则
  if (value.trim().length >= 2) {
    callBack()
  } else {
    //校验未通过返回的错误的提示信息
    callBack(new Error('品牌名称位数大于等于两位'))
  }
}
//品牌LOGO图片的自定义校验规则方法
const validatorLogoUrl = (rule: any, value: any, callBack: any) => {
  //如果图片上传
  if (value) {
    callBack()
  } else {
    callBack(new Error('LOGO图片务必上传'))
  }
}
```

#### 5.7.2 存在的一些问题

1. 图片校验时机

因为img是图片，不好判断。因此使用表单的**validate**属性，全部校验，放在确认按钮的回调函数中

```typescript
const confirm = async () => {
  //在你发请求之前,要对于整个表单进行校验
  //调用这个方法进行全部表单相校验,如果校验全部通过，在执行后面的语法
  await formRef.value.validate()
 。。。。。。
}
```

2. 清除校验信息

当图片没有上传点击确认后会出来校验的提示信息，我们上传图片后校验信息应该消失。使用表单的**clearValidate属性**

```typescript
//图片上传成功钩子
const handleAvatarSuccess: UploadProps['onSuccess'] = (
  。。。。。。
) => {
  。。。。。。。
  //图片上传成功,清除掉对应图片校验结果
  formRef.value.clearValidate('logoUrl')
}
```

3. 清除校验信息2

当我们未填写信息去点击确认按钮时，会弹出2个校验信息。当我们关闭后再打开，校验信息还在。因为，我们需要在添加品牌按钮时清除校验信息。但是因为点击添加品牌，表单还没有加载，所以我们需要换个写法。

```typescript
//添加品牌按钮的回调
const addTrademark = () => {
  //对话框显示
  dialogFormVisible.value = true
  //清空收集数据
  trademarkParams.id = 0
  trademarkParams.tmName = ''
  trademarkParams.logoUrl = ''
  //第一种写法:ts的问号语法
  formRef.value?.clearValidate('tmName')
  formRef.value?.clearValidate('logoUrl')
  /* nextTick(() => {
    formRef.value.clearValidate('tmName')
    formRef.value.clearValidate('logoUrl')
  }) */
}
```

同理**修改按钮**

```typescript
//修改已有品牌的按钮的回调
//row:row即为当前已有的品牌
const updateTrademark = (row: TradeMark) => {
  //清空校验规则错误提示信息
  nextTick(() => {
    formRef.value.clearValidate('tmName')
    formRef.value.clearValidate('logoUrl')
  })
 。。。。。。
}
```

### 5.8删除业务

删除业务要做的事情不多，包括API以及发请求。不过有些点要注意

1. API 

```typescript
//书写品牌管理模块接口
import request from '@/utils/request'
import type { TradeMarkResponseData, TradeMark } from './type'
//品牌管理模块接口地址
enum API {
  。。。。。。。
  //删除已有品牌
  DELETE_URL = '/admin/product/baseTrademark/remove/',
}
。。。。。。

//删除某一个已有品牌的数据
export const reqDeleteTrademark = (id: number) =>
  request.delete<any, any>(API.DELETE_URL + id)

```

2. 绑定函数

这里使用了一个气泡组件，@confirm绑定的就是回调函数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250422123019.png)

3. 回调函数

```typescript
//气泡确认框确定按钮的回调
const removeTradeMark = async (id: number) => {
  //点击确定按钮删除已有品牌请求
  let result = await reqDeleteTrademark(id)
  if (result.code == 200) {
    //删除成功提示信息
    ElMessage({
      type: 'success',
      message: '删除品牌成功',
    })
    //再次获取已有的品牌数据
    getHasTrademark(
      trademarkArr.value.length > 1 ? pageNo.value : pageNo.value - 1,
    )
  } else {
    ElMessage({
      type: 'error',
      message: '删除品牌失败',
    })
  }
}
```



## 6 属性管理模块

### 6.1 属性管理模块的静态组件

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729094811.png)

#### 6.1.1 三级分类全局组件（静态）

注意：要在`src\components\index.ts`下引入。

```typescript
<template>
  <el-card>
    <el-form inline>
      <el-form-item label="一级分类">
        <el-select>
          <el-option label="北京"></el-option>
          <el-option label="深圳"></el-option>
          <el-option label="广州"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="二级分类">
        <el-select>
          <el-option label="北京"></el-option>
          <el-option label="深圳"></el-option>
          <el-option label="广州"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="三级分类">
        <el-select>
          <el-option label="北京"></el-option>
          <el-option label="深圳"></el-option>
          <el-option label="广州"></el-option>
        </el-select>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts"></script>

<style lang="" scoped></style>

```

#### 6.1.2 添加属性模块（静态）

```typescript
<template>
  <!-- 三级分类全局组件-->
  <Category></Category>
  <el-card style="margin: 10px 0px">
    <el-button type="primary" size="default" icon="Plus">添加属性</el-button>
    <el-table border style="margin: 10px 0px">
      <el-table-column
        label="序号"
        type="index"
        align="center"
        width="80px"
      ></el-table-column>
      <el-table-column label="属性名称" width="120px"></el-table-column>
      <el-table-column label="属性值名称"></el-table-column>
      <el-table-column label="操作" width="120px"></el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped></style>

```

### 6.2 一级分类数据

> 一级分类的流程时：API->pinia->组件
>
> 为什么要使用pinia呢？因为在下面的添加属性那部分，父组件要用到三级分类组件的信息（id），所以将数据放在pinia中是最方便的。

#### 6.2.1 API

```typescript
//这里书写属性相关的API文件
import request from '@/utils/request'
//属性管理模块接口地址
enum API {
  //获取一级分类接口地址
  C1_URL = '/admin/product/getCategory1',
  //获取二级分类接口地址
  C2_URL = '/admin/product/getCategory2/',
  //获取三级分类接口地址
  C3_URL = '/admin/product/getCategory3/',
}

//获取一级分类的接口方法
export const reqC1 = () => request.get<any, any>(API.C1_URL)
//获取二级分类的接口方法
export const reqC2 = (category1Id: number | string) => {
  return request.get<any, any>(API.C2_URL + category1Id)
}
//获取三级分类的接口方法
export const reqC3 = (category2Id: number | string) => {
  return request.get<any, any>(API.C3_URL + category2Id)
}

```

#### 6.2.2 pinia

```typescript
//商品分类全局组件的小仓库
import { defineStore } from 'pinia'
import { reqC1, } from '@/api/product/attr'
const useCategoryStore = defineStore('Category', {
  state: () => {
    return {
      //存储一级分类的数据
      c1Arr: [],
      //存储一级分类的ID
      c1Id: '',
      
    }
  },
  actions: {
    //获取一级分类的方法
    async getC1() {
      //发请求获取一级分类的数据
      const result = await reqC1()
      if (result.code == 200) {
        this.c1Arr = result.data
      }
    },
  },
  getters: {},
})

export default useCategoryStore

```

#### 6.2.3 Category组件

注意：**el-option**中的**:value**属性，它将绑定的值传递给**el-select**中的**v-model**绑定的值

```vue
<template>
  <el-card>
    <el-form inline>
      <el-form-item label="一级分类">
        <el-select v-model="categoryStore.c1Id">
          <!-- label:即为展示数据 value:即为select下拉菜单收集的数据 -->
          <el-option
            v-for="(c1, index) in categoryStore.c1Arr"
            :key="c1.id"
            :label="c1.name"
            :value="c1.id"
            ></el-option>
        </el-select>
      </el-form-item>
      。。。。。。
</template>

<script setup lang="ts">
  //引入组件挂载完毕方法
  import { onMounted } from 'vue'
  //引入分类相关的仓库
  import useCategoryStore from '@/store/modules/category'
  let categoryStore = useCategoryStore()
  //分类全局组件挂载完毕,通知仓库发请求获取一级分类的数据
  onMounted(() => {
    getC1()
  })
  //通知仓库获取一级分类的方法
  const getC1 = () => {
    //通知分类仓库发请求获取一级分类的数据
    categoryStore.getC1()
  }
</script>

<style lang="" scoped></style>

```

### 6.3 分类数据ts类型

#### 6.3.1 API下的type

```typescript
//分类相关的数据ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}

//分类ts类型
export interface CategoryObj {
  id: number | string
  name: string
  category1Id?: number
  category2Id?: number
}

//相应的分类接口返回数据的类型
export interface CategoryResponseData extends ResponseData {
  data: CategoryObj[]
}

```

**使用：仓库中的result，API中的接口返回的数据**

#### 6.3.2 组件下的type

```typescript
import type { CategoryObj } from '@/api/product/attr/type'
。。。。。
//定义分类仓库state对象的ts类型
export interface CategoryState {
  c1Id: string | number
  c1Arr: CategoryObj[]
  c2Arr: CategoryObj[]
  c2Id: string | number
  c3Arr: CategoryObj[]
  c3Id: string | number
}

```

使用：仓库中的state数据类型

### 6.4 完成分类组件业务

> 分类组件就是以及组件上来就拿到数据，通过用户选择后我们会拿到id，通过id发送请求之后二级分类就会拿到数据。以此类推三级组件。我们以二级分类为例。

#### 6.4.1 二级分类流程

1. 绑定函数

二级分类不是一上来就发生变化，而是要等一级分类确定好之后再发送请求获得数据。于是我们将这个发送请求的回调函数绑定在了一级分类的**change**属性上

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729095449.png)

2. 回调函数

```typescript
//此方法即为一级分类下拉菜单的change事件(选中值的时候会触发,保证一级分类ID有了)
const handler = () => {
  //通知仓库获取二级分类的数据
  categoryStore.getC2()
}
```

3. pinia

```typescript
//获取二级分类的数据
    async getC2() {
      //获取对应一级分类的下二级分类的数据
      const result: CategoryResponseData = await reqC2(this.c1Id)
      if (result.code == 200) {
        this.c2Arr = result.data
      }
    },
```

4. 组件数据展示

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729095534.png)

#### 6.4.2 小问题

> 当我们选择好三级菜单后，此时修改一级菜单。二、三级菜单应该清空
>
> 清空id之后就不会显示了。

```vue
//此方法即为一级分类下拉菜单的change事件(选中值的时候会触发,保证一级分类ID有了)
const handler = () => {
  //需要将二级、三级分类的数据清空
  categoryStore.c2Id = ''
  categoryStore.c3Arr = []
  categoryStore.c3Id = ''
  //通知仓库获取二级分类的数据
  categoryStore.getC2()
}
```

```vue
//此方法即为二级分类下拉菜单的change事件(选中值的时候会触发,保证二级分类ID有了)
const handler1 = () => {
  //清理三级分类的数据
  categoryStore.c3Id = ''
  categoryStore.getC3()
}
```

#### 6.4.3 添加属性按钮禁用

> 在我们没选择好三级菜单之前，添加属性按钮应该处于禁用状态

`src\views\product\attr\index.vue`（父组件）

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729095612.png)

6.5 已有属性与属性值展示

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729095634.png)

#### 6.5.1 返回type类型

```typescript
//属性值对象的ts类型
export interface AttrValue {
  id?: number
  valueName: string
  attrId?: number
  flag?: boolean
}

//存储每一个属性值的数组类型
export type AttrValueList = AttrValue[]
//属性对象
export interface Attr {
  id?: number
  attrName: string
  categoryId: number | string
  categoryLevel: number
  attrValueList: AttrValueList
}
//存储每一个属性对象的数组ts类型
export type AttrList = Attr[]
//属性接口返回的数据ts类型
export interface AttrResponseData extends ResponseData {
  data: Attr[]
}

```

#### 6.5.2 API发送请求

```typescript
//这里书写属性相关的API文件
import request from '@/utils/request'
import type { CategoryResponseData, AttrResponseData, Attr } from './type'
//属性管理模块接口地址
enum API {
  。。。。。。。
  //获取分类下已有的属性与属性值
  ATTR_URL = '/admin/product/attrInfoList/',
}
。。。。。。
//获取对应分类下已有的属性与属性值接口
export const reqAttr = (
  category1Id: string | number,
  category2Id: string | number,
  category3Id: string | number,
) => {
  return request.get<any, AttrResponseData>(
    API.ATTR_URL + `${category1Id}/${category2Id}/${category3Id}`,
  )
}

```

#### 6.5.3 组件获取返回数据并存储数据

注意：通过watch监听c3Id，来适时的获取数据。

```typescript
<script setup lang="ts">
//组合式API函数
import { watch, ref } from 'vue'
//引入获取已有属性与属性值接口
import { reqAttr } from '@/api/product/attr'
import type { AttrResponseData, Attr } from '@/api/product/attr/type'
//引入分类相关的仓库
import useCategoryStore from '@/store/modules/category'
let categoryStore = useCategoryStore()
//存储已有的属性与属性值
let attrArr = ref<Attr[]>([])
//监听仓库三级分类ID变化
watch(
  () => categoryStore.c3Id,
  () => {
    //获取分类的ID
    getAttr()
  },
)
//获取已有的属性与属性值方法
const getAttr = async () => {
  const { c1Id, c2Id, c3Id } = categoryStore
  //获取分类下的已有的属性与属性值
  let result: AttrResponseData = await reqAttr(c1Id, c2Id, c3Id)
  console.log(result)

  if (result.code == 200) {
    attrArr.value = result.data
  }
}
</script>
```

#### 6.5.4 将数据放入模板中

```typescript
<el-card style="margin: 10px 0px">
    <el-button
      type="primary"
      size="default"
      icon="Plus"
      :disabled="categoryStore.c3Id ? false : true"
    >
      添加属性
    </el-button>
    <el-table border style="margin: 10px 0px" :data="attrArr">
      <el-table-column
        label="序号"
        type="index"
        align="center"
        width="80px"
      ></el-table-column>
      <el-table-column
        label="属性名称"
        width="120px"
        prop="attrName"
      ></el-table-column>
      <el-table-column label="属性值名称">
        <!-- row：已有的属性对象 -->
        <template #="{ row, $index }">
          <el-tag
            style="margin: 5px"
            v-for="(item, index) in row.attrValueList"
            :key="item.id"
          >
            {{ item.valueName }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120px">
        <!-- row：已有的属性对象 -->
        <template #="{ row, $index }">
          <!-- 修改已有属性的按钮 -->
          <el-button type="primary" size="small" icon="Edit"></el-button>
          <el-button type="primary" size="small" icon="Delete"></el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
```

#### 6.5.5 小问题

当我们获取数据并展示以后，此时修改一级分类或者二级分类，由于watch的存在，同样会发送请求。但是此时没有c3Id，请求会失败。因此将watch改为如下

```vue
//监听仓库三级分类ID变化
watch(
  () => categoryStore.c3Id,
  () => {
    //清空上一次查询的属性与属性值
    attrArr.value = []
    //保证三级分类得有才能发请求
    if (!categoryStore.c3Id) return
    //获取分类的ID 
    getAttr()
  },
)
```

### 6.6 添加属性页面的静态展示

当点击**添加属性**后：

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729100445.png)

6.6.1 定义变量控制页面展示与隐藏

```vue
let scene = ref<number>(0);
```

6.6.2 表单

```vue
<div v-show="scene === 1">
            <el-form :inline="true">
                <el-form-item label="属性名称">
                    <el-input
                        placeholder="请你输入属性名称"
                    ></el-input>
                </el-form-item>
            </el-form>
            <el-button
                type="primary"
                size="default"
                icon="Plus"
            >
                添加属性值
            </el-button>
            <el-button
                size="default"
                @click="cancel"
                >取消</el-button
            >
            <el-table
                border
                style="margin: 10px 0"
                :data="attrParams.attrValueList"
            >
                <el-table-column
                    label="序号"
                    width="80px"
                    type="index"
                    align="center"
                ></el-table-column>
                <el-table-column label="属性值名称">
                    <template #="{ row, $index }">
                 
                    </template>
                </el-table-column>
                <el-table-column label="属性值操作">
                    <template #="{ row, $index }">
                    </template>
                </el-table-column>
            </el-table>
        </div>
```

### 6.7 添加属性&&修改属性的接口类型

#### 6.7.1 type

```ts
//属性值对象的ts类型
export interface AttrValue {
  id?: number
  valueName: string
  attrId?: number
  flag?: boolean
}


//存储每一个属性值的数组类型
export type AttrValueList = AttrValue[]
//属性对象
export interface Attr {
  id?: number
  attrName: string
  categoryId: number | string
  categoryLevel: number
  attrValueList: AttrValueList
}
```

#### 6.7.2 组件收集新增的属性的数据

```vue
//收集新增的属性的数据
let attrParams = reactive<Attr>({
  attrName: '', //新增的属性的名字
  attrValueList: [
    //新增的属性值数组
  ],
  categoryId: '', //三级分类的ID
  categoryLevel: 3, //代表的是三级分类
})
```

### 6.8 添加属性值

> 一个操作最重要的是理清楚思路。添加属性值的总体思路是：收集表单的数据（绑定对应的表单项等）->发送请求（按钮回调函数，携带的参数）->更新页面

#### 6.8.1 收集表单的数据（attrParams）

1. 属性名称（attrName）

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729101443.png)

2. 属性值数组（attrValueList）

我们给添加属性值按钮绑定一个回调，点击的时候会往attrParams.attrValueList中添加一个空数组。我们根据空数组的数量生成input框，再将input的值与数组中的值绑定。

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729101529.png)

```vue
//添加属性值按钮的回调
const addAttrValue = () => {
  //点击添加属性值按钮的时候,向数组添加一个属性值对象
  attrParams.attrValueList.push({
    valueName: '',
    flag: true, //控制每一个属性值编辑模式与切换模式的切换
  })
}
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729101609.png)

3. 三级分类的id（categoryId）

三级分类的id（c3Id）在页面1的添加属性按钮之前就有了，因此我们把它放到添加属性按钮的回调身上

注意：每一次点击的时候,先清空一下数据再收集数据。防止下次点击时会显示上次的数据

```vue
//添加属性按钮的回调
const addAttr = () => {
  //每一次点击的时候,先清空一下数据再收集数据
  Object.assign(attrParams, {
    attrName: '', //新增的属性的名字
    attrValueList: [
      //新增的属性值数组
    ],
    categoryId: categoryStore.c3Id, //三级分类的ID
    categoryLevel: 3, //代表的是三级分类
  })


  //切换为添加与修改属性的结构
  scene.value = 1
}
```

4. categoryLevel（固定的，无需收集）

#### 6.8.2 发送请求&&更新页面

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729101742.png)

```vue
//保存按钮的回调
const save = async () => {
  //发请求
  let result: any = await reqAddOrUpdateAttr(attrParams)
  //添加属性|修改已有的属性已经成功
  if (result.code == 200) {
    //切换场景
    scene.value = 0
    //提示信息
    ElMessage({
      type: 'success',
      message: attrParams.id ? '修改成功' : '添加成功',
    })
    //获取全部已有的属性与属性值（更新页面）
    getAttr()
  } else {
    ElMessage({
      type: 'error',
      message: attrParams.id ? '修改失败' : '添加失败',
    })
  }
}
```

### 6.9 属性值的编辑与查看模式

#### 6.9.1 模板的切换

在input下面添加了一个div，使用flag来决定哪个展示。

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729101835.png)

注意：flag放在哪？由于每一个属性值对象都需要一个flag属性，因此将flag的添加放在添加属性值的按钮的回调上。（注意修改属性值的type）

```vue
//添加属性值按钮的回调
const addAttrValue = () => {
  //点击添加属性值按钮的时候,向数组添加一个属性值对象
  attrParams.attrValueList.push({
    valueName: '',
    flag: true, //控制每一个属性值编辑模式与切换模式的切换
  })
  
}
```

`src\api\product\attr\type.ts`

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729101905.png)

#### 6.9.2 切换的回调

```typescript
//属性值表单元素失却焦点事件回调
const toLook = (row: AttrValue, $index: number) => {
  。。。。。。
  //相应的属性值对象flag:变为false,展示div
  row.flag = false
}


//属性值div点击事件
const toEdit = (row: AttrValue, $index: number) => {
  //相应的属性值对象flag:变为true,展示input
  row.flag = true
  。。。。。。
}
```

#### 6.9.3 处理非法属性值

```typescript
//属性值表单元素失却焦点事件回调
const toLook = (row: AttrValue, $index: number) => {
  //非法情况判断1
  if (row.valueName.trim() == '') {
    //删除调用对应属性值为空的元素
    attrParams.attrValueList.splice($index, 1)
    //提示信息
    ElMessage({
      type: 'error',
      message: '属性值不能为空',
    })
    return
  }
  //非法情况2
  let repeat = attrParams.attrValueList.find((item) => {
    //切记把当前失却焦点属性值对象从当前数组扣除判断
    if (item != row) {
      return item.valueName === row.valueName
    }
  })


  if (repeat) {
    //将重复的属性值从数组当中干掉
    attrParams.attrValueList.splice($index, 1)
    //提示信息
    ElMessage({
      type: 'error',
      message: '属性值不能重复',
    })
    return
  }
  //相应的属性值对象flag:变为false,展示div
  row.flag = false
}
```

### 6.10 表单聚焦&&删除按钮

> 表单聚焦可以直接调用input提供foces方法：<font style="color:rgb(48, 49, 51);">当选择器的输入框获得焦点时触发</font>

#### 6.10.1 存储组件实例

使用ref的函数形式，每有一个input就将其存入inputArr中

```typescript
//准备一个数组:将来存储对应的组件实例el-input
let inputArr = ref<any>([])
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102011.png)

#### 6.10.2 点击div转换成input框后的自动聚焦

注意：使用nextTick是因为点击后，组件需要加载，没办法第一时间拿到组件实例。所以使用nextTick会等到组件加载完毕后才调用，达到聚焦效果。

```typescript
//属性值div点击事件
const toEdit = (row: AttrValue, $index: number) => {
  //相应的属性值对象flag:变为true,展示input
  row.flag = true
  //nextTick:响应式数据发生变化,获取更新的DOM(组件实例)
  nextTick(() => {
    inputArr.value[$index].focus()
  })
}
```

#### 6.10.3 添加属性值自动聚焦

```typescript
//添加属性值按钮的回调
const addAttrValue = () => {
  //点击添加属性值按钮的时候,向数组添加一个属性值对象
  attrParams.attrValueList.push({
    valueName: '',
    flag: true, //控制每一个属性值编辑模式与切换模式的切换
  })
  //获取最后el-input组件聚焦
  nextTick(() => {
    inputArr.value[attrParams.attrValueList.length - 1].focus()
  })
}
```

#### 6.10.4 删除按钮

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102042.png)

### 6.11属性修改业务

#### 6.11.1属性修改业务

修改业务很简单：当我们点击修改按钮的时候，将修改的实例（row）传递给回调函数。回调函数：首先跳转到第二页面，第二页面是根据attrParams值生成的，我们跳转的时候将实例的值传递给attrParams

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102209.png)

```vue
//table表格修改已有属性按钮的回调
const updateAttr = (row: Attr) => {
  //切换为添加与修改属性的结构
  scene.value = 1
  //将已有的属性对象赋值给attrParams对象即为
  //ES6->Object.assign进行对象的合并
  Object.assign(attrParams, JSON.parse(JSON.stringify(row)))
}
```

### 6.12 删除按钮&&清空数据

#### 6.12.1删除按钮

1. API

```typescript
//这里书写属性相关的API文件
import request from '@/utils/request'
import type { CategoryResponseData, AttrResponseData, Attr } from './type'
//属性管理模块接口地址
enum API {
  。。。。。。
  //删除某一个已有的属性
  DELETEATTR_URL = '/admin/product/deleteAttr/',
}
。。。。。。

//删除某一个已有的属性业务
export const reqRemoveAttr = (attrId: number) =>
  request.delete<any, any>(API.DELETEATTR_URL + attrId)
```

2. 绑定点击函数&&气泡弹出框

   ![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102341.png)

3. 回调函数（功能实现&&刷新页面）

```typescript
//删除某一个已有的属性方法回调
const deleteAttr = async (attrId: number) => {
  //发相应的删除已有的属性的请求
  let result: any = await reqRemoveAttr(attrId)
  //删除成功
  if (result.code == 200) {
    ElMessage({
      type: 'success',
      message: '删除成功',
    })
    //获取一次已有的属性与属性值
    getAttr()
  } else {
    ElMessage({
      type: 'error',
      message: '删除失败',
    })
  }
}
```

#### 6.12.2路由跳转前清空数据

```typescript
//路由组件销毁的时候，把仓库分类相关的数据清空
onBeforeUnmount(() => {
  //清空仓库的数据
  categoryStore.$reset()
})
```

## 9 用户管理模块

### 9.1 静态搭建

主要是el-form、el-pagination

```vue
<template>
  <el-card style="height: 80px">
    <el-form :inline="true" class="form">
      <el-form-item label="用户名:">
        <el-input placeholder="请你输入搜索用户名"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="default">搜索</el-button>
        <el-button type="primary" size="default" @click="reset">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
  <el-card style="margin: 10px 0px">
    <el-button type="primary" size="default">添加用户</el-button>
    <el-button type="primary" size="default">批量删除</el-button>
    <!-- table展示用户信息 -->
    <el-table style="margin: 10px 0px" border>
      <el-table-column type="selection" align="center"></el-table-column>
      <el-table-column label="#" align="center" type="index"></el-table-column>
      <el-table-column label="ID" align="center"></el-table-column>
      <el-table-column
        label="用户名字"
        align="center"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="用户名称"
        align="center"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="用户角色"
        align="center"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="创建时间"
        align="center"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="更新时间"
        align="center"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="操作"
        width="300px"
        align="center"
      ></el-table-column>
    </el-table>
    <!-- 分页器 -->
    <el-pagination
      v-model:current-page="pageNo"
      v-model:page-size="pageSize"
      :page-sizes="[5, 7, 9, 11]"
      :background="true"
      layout="prev, pager, next, jumper,->,sizes,total"
      :total="400"
    />
  </el-card>
</template>
```

### 9.2 用户管理基本信息展示

#### 9.2.1 API&&type

```typescript
//用户管理模块的接口
import request from '@/utils/request'
import type { UserResponseData } from './type'
//枚举地址
enum API {
  //获取全部已有用户账号信息
  ALLUSER_URL = '/admin/acl/user/',
}


//获取用户账号信息的接口
export const reqUserInfo = (page: number, limit: number) => {
  return request.get<any, UserResponseData>(
    API.ALLUSER_URL + `${page}/${limit}`,
  )
}
```

```typescript
//账号信息的ts类型
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
//代表一个账号信息的ts类型
export interface User {
  id?: number
  createTime?: string
  updateTime?: string
  username?: string
  password?: string
  name?: string
  phone?: null
  roleName?: string
}
//数组包含全部的用户信息
export type Records = User[]
//获取全部用户信息接口返回的数据ts类型
export interface UserResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    size: number
    current: number
    pages: number
  }
}
```

#### 9.2.2 发送请求（onMounted）

```vue
//用户总个数
let total = ref<number>(0)
//存储全部用户的数组
let userArr = ref<Records>([])
onMounted(() => {
  getHasUser()
})
//获取全部已有的用户信息
const getHasUser = async (pager = 1) => {
  //收集当前页码
  pageNo.value = pager
  let result: UserResponseData = await reqUserInfo(
    pageNo.value,
    pageSize.value,
    /* keyword.value, */
  )
  if (result.code == 200) {
    total.value = result.data.total
    userArr.value = result.data.records
  }
}
```

#### 9.2.3 模板展示数据

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102616.png)

9.2.4 分页器俩个函数回调

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102717.png)

```vue
//分页器下拉菜单的自定义事件的回调
const handler = () => {
  getHasUser()
}
```

9.3 添加与修改用户静态

```vue
<!-- 抽屉结构:完成添加新的用户账号|更新已有的账号信息 -->
<el-drawer v-model="drawer">
  <!-- 头部标题:将来文字内容应该动态的 -->
  <template #header>
    <h4>添加用户</h4>
  </template>
  <!-- 身体部分 -->
  <template #default>
    <el-form>
      <el-form-item label="用户姓名">
        <el-input placeholder="请您输入用户姓名"></el-input>
      </el-form-item>
      <el-form-item label="用户昵称">
        <el-input placeholder="请您输入用户昵称"></el-input>
      </el-form-item>
      <el-form-item label="用户密码">
        <el-input placeholder="请您输入用户密码"></el-input>
      </el-form-item>
    </el-form>
  </template>
  <template #footer>
    <div style="flex: auto">
      <el-button>取消</el-button>
      <el-button type="primary">确定</el-button>
    </div>
  </template>
</el-drawer>
```

#### 9.4.1 API&&TYPE

API：  
添加和修改的请求封装成一个。

```typescript
//添加一个新的用户账号
ADDUSER_URL = '/admin/acl/user/save',
//更新已有的用户账号
UPDATEUSER_URL = '/admin/acl/user/update',
//添加用户与更新已有用户的接口
export const reqAddOrUpdateUser = (data: User) => {
  //携带参数有ID更新
  if (data.id) {
    return request.put<any, any>(API.UPDATEUSER_URL, data)
  } else {
    return request.post<any, any>(API.ADDUSER_URL, data)
  }
}
```

type

```typescript
//代表一个账号信息的ts类型
export interface User {
  id?: number
  createTime?: string
  updateTime?: string
  username?: string
  password?: string
  name?: string
  phone?: null
  roleName?: string
}
```

#### 9.4.2 组件收集数据

```vue
//收集用户信息的响应式数据
let userParams = reactive<User>({
  username: '',
  name: '',
  password: '',
})
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102827.png)

#### 9.4.3 发起请求

```vue
//保存按钮的回调
const save = async () => {
  //保存按钮:添加新的用户|更新已有的用户账号信息
  let result: any = await reqAddOrUpdateUser(userParams)
  //添加或者更新成功
  if (result.code == 200) {
    //关闭抽屉
    drawer.value = false
    //提示消息
    ElMessage({
      type: 'success',
      message: userParams.id ? '更新成功' : '添加成功',
    })
    //获取最新的全部账号的信息
    getHasUser(userParams.id ? pageNo.value : 1)
  } else {
    //关闭抽屉
    drawer.value = false
    //提示消息
    ElMessage({
      type: 'error',
      message: userParams.id ? '更新失败' : '添加失败',
    })
  }
}
```

#### 9.4.4 添加用户按钮&&取消按钮

添加用户按钮：我们在点击添加用户按钮的时候，先把之前的用户数据清空

```vue
//添加用户按钮的回调
const addUser = () => {
  //抽屉显示出来
  drawer.value = true
  //清空数据
  Object.assign(userParams, {
    id: 0,
    username: '',
    name: '',
    password: '',
  })
  
}
```

取消按钮：

点击取消按钮之后：关闭抽屉

```vue
//取消按钮的回调
const cancel = () => {
  //关闭抽屉
  drawer.value = false
}
```

### 9.5 表单校验功能

#### 9.5.1 表单绑定校验信息

注意点：注意表单FORM与表格Table的区别。

主要还是收集与展示数据的区别。

表单绑定的:model="userParams"是数据，prop="username"是属性，绑定是为了对表单进行验证。

表格绑定的data是要显示的数据，item项的prop也是要展示的数据

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102921.png)

#### 9.5.2 校验规则

```vue
//校验用户名字回调函数
const validatorUsername = (rule: any, value: any, callBack: any) => {
  //用户名字|昵称,长度至少五位
  if (value.trim().length >= 5) {
    callBack()
  } else {
    callBack(new Error('用户名字至少五位'))
  }
}
//校验用户名字回调函数
const validatorName = (rule: any, value: any, callBack: any) => {
  //用户名字|昵称,长度至少五位
  if (value.trim().length >= 5) {
    callBack()
  } else {
    callBack(new Error('用户昵称至少五位'))
  }
}
const validatorPassword = (rule: any, value: any, callBack: any) => {
  //用户名字|昵称,长度至少五位
  if (value.trim().length >= 6) {
    callBack()
  } else {
    callBack(new Error('用户密码至少六位'))
  }
}
//表单校验的规则对象
const rules = {
  //用户名字
  username: [{ required: true, trigger: 'blur', validator: validatorUsername }],
  //用户昵称
  name: [{ required: true, trigger: 'blur', validator: validatorName }],
  //用户的密码
  password: [{ required: true, trigger: 'blur', validator: validatorPassword }],
}
```

#### 9.5.3 确保校验通过再发请求

先获取form组件的实例，在调用form组件的方法**validate()**

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729102944.png)

```vue
//获取form组件实例
let formRef = ref<any>()
```

```vue
//保存按钮的回调
const save = async () => {
  //点击保存按钮的时候,务必需要保证表单全部复合条件在去发请求
  await formRef.value.validate()
 。。。。。。
}
```

#### 9.5.4 再次校验前先清空上次的校验展示

使用nextTick是因为第一次的时候还没有formRef实例。

```typescript
//添加用户按钮的回调
const addUser = () => {
  。。。。。。
  //清除上一次的错误的提示信息
  nextTick(() => {
    formRef.value.clearValidate('username')
    formRef.value.clearValidate('name')
    formRef.value.clearValidate('password')
  })
}
```

### 9.6 更新账号业务

#### 9.6.1 抽屉结构变化分析

标题应该该为**更新用户**，没有输入密码。因为修改业务时我们需要用到用户id，因此再修改按钮存储账号信息赋值了用户的id。

我们根据这个id来决定我们的界面。

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729103103.png)

初始化用户id：

我们再修改的时候将row的值复制给userParams，因此在展示抽屉的时候就会变换

```vue
//更新已有的用户按钮的回调
//row:即为已有用户的账号信息
const updateUser = (row: User) => {
  //抽屉显示出来
  drawer.value = true
  //存储收集已有的账号信息
  Object.assign(userParams, row)
  //清除上一次的错误的提示信息
  nextTick(() => {
    formRef.value.clearValidate('username')
    formRef.value.clearValidate('name')
  })
}
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729103130.png)

#### 9.6.1 其余工作

1. 添加按钮回调

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729103206.png)

2. 清除上一次的错误的提示信息

```vue
//更新已有的用户按钮的回调
//row:即为已有用户的账号信息
const updateUser = (row: User) => {
  //抽屉显示出来
  drawer.value = true
  //存储收集已有的账号信息
  Object.assign(userParams, row)
  //清除上一次的错误的提示信息
  nextTick(() => {
    formRef.value.clearValidate('username')
    formRef.value.clearValidate('name')
  })
}
```

3.更改当前帐号之后，应该重新登陆

window身上的方法，刷新一次。

```vue
//保存按钮的回调
const save = async () => {
  。。。。。。。
  //添加或者更新成功
  。。。。。。。
    //获取最新的全部账号的信息
    getHasUser(userParams.id ? pageNo.value : 1)
    //浏览器自动刷新一次
    window.location.reload()
  } 。。。。。。。
}
```

### 9.7 分配角色静态搭建

```vue
          <el-form-item label="用户姓名">
            <el-input v-model="userParams.username" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="职位列表">
            <el-checkbox>
              全选
            </el-checkbox>
            <!-- 显示职位的的复选框 -->
            <el-checkbox-group>
              <el-checkbox
                v-for="(role, index) in 10"
                :key="index"
                :label="index"
              >
                {{ index }}
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729112933.png)

### 9.8 分配角色业务

#### 9.8.1 API&&TYPE  

```typescript
//获取全部职位以及包含当前用户的已有的职位
export const reqAllRole = (userId: number) => {
  return request.get<any, AllRoleResponseData>(API.ALLROLEURL + userId)
}
```

```typescript
//代表一个职位的ts类型
export interface RoleData {
  id?: number
  createTime?: string
  updateTime?: string
  roleName: string
  remark: null
}
//全部职位的列表
export type AllRole = RoleData[]
//获取全部职位的接口返回的数据ts类型
export interface AllRoleResponseData extends ResponseData {
  data: {
    assignRoles: AllRole
    allRolesList: AllRole
  }
}
```

#### 9.8.2获取&&存储数据

```vue
//收集顶部复选框全选数据
let checkAll = ref<boolean>(false)
//控制顶部全选复选框不确定的样式
let isIndeterminate = ref<boolean>(true)
//存储全部职位的数据
let allRole = ref<AllRole>([])
//当前用户已有的职位
let userRole = ref<AllRole>([])
//分配角色按钮的回调
const setRole = async (row: User) => {
  //存储已有的用户信息
  Object.assign(userParams, row)
  //获取全部的职位的数据与当前用户已有的职位的数据
  let result: AllRoleResponseData = await reqAllRole(userParams.id as number)
  if (result.code == 200) {
    //存储全部的职位
    allRole.value = result.data.allRolesList
    //存储当前用户已有的职位
    userRole.value = result.data.assignRoles
    //抽屉显示出来
    drawer1.value = true
  }
}
```

#### 9.8.3 展示数据

```vue
<!-- 抽屉结构:用户某一个已有的账号进行职位分配 -->
    <el-drawer v-model="drawer1">
      <template #header>
        <h4>分配角色(职位)</h4>
      </template>
      <template #default>
        <el-form>
          <el-form-item label="用户姓名">
            <el-input v-model="userParams.username" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="职位列表">
            <el-checkbox
              @change="handleCheckAllChange"
              v-model="checkAll"
              :indeterminate="isIndeterminate"
            >
              全选
            </el-checkbox>
            <!-- 显示职位的的复选框 -->
            <el-checkbox-group
              v-model="userRole"
              @change="handleCheckedCitiesChange"
            >
              <el-checkbox
                v-for="(role, index) in allRole"
                :key="index"
                :label="role"
              >
                {{ role.roleName }}
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </template>
    </el-drawer>
```

详细解释：

全选部分：

@change：全选框点击时的回调

v-model：绑定的数据，根据这个值决定是否全选

:indeterminate：不确定状态，既没有全选也没有全不选

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729143443.png)

复选框部分：  
`v-for="(role, index) in allRole"`：遍历allRole。

`:label="role"`：收集的数据（勾上的数据）

`v-model="userRole"`：绑定收集的数据，也就是收集的数据存储到userRole中。

@change：勾选变化时的回调

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729113047.png)

全选框勾选的回调：

实现原理：函数会将勾选与否注入到val中，如果是，就将全部数据（allRole）赋值给选中的数据（userRole），选中的数据通过v-model实现页面的同步变化。

```vue
//顶部的全部复选框的change事件
const handleCheckAllChange = (val: boolean) => {
  //val:true(全选)|false(没有全选)
  userRole.value = val ? allRole.value : []
  //不确定的样式(确定样式)
  isIndeterminate.value = false
}
```

复选框

```vue
//顶部全部的复选框的change事件
const handleCheckedCitiesChange = (value: string[]) => {
  //顶部复选框的勾选数据
  //代表:勾选上的项目个数与全部的职位个数相等，顶部的复选框勾选上
  checkAll.value = value.length === allRole.value.length
  //不确定的样式
  isIndeterminate.value = value.length !== allRole.value.length
}
```

#### 9.8.4 分配角色业务（给服务器发请求）

1. api&&type

```typescript
//分配职位
export const reqSetUserRole = (data: SetRoleData) => {
  return request.post<any, any>(API.SETROLE_URL, data)
}
```

```typescript
//给用户分配职位接口携带参数的ts类型
export interface SetRoleData {
  roleIdList: number[]
  userId: number
}
```

2. 组件发送请求

回调绑在确认按钮身上就可以了

```vue
//确定按钮的回调(分配职位)
const confirmClick = async () => {
  //收集参数
  let data: SetRoleData = {
    userId: userParams.id as number,
    roleIdList: userRole.value.map((item) => {
      return item.id as number
    }),
  }
  //分配用户的职位
  let result: any = await reqSetUserRole(data)
  if (result.code == 200) {
    //提示信息
    ElMessage({ type: 'success', message: '分配职务成功' })
    //关闭抽屉
    drawer1.value = false
    //获取更新完毕用户的信息,更新完毕留在当前页
    getHasUser(pageNo.value)
  }
}
```

### 9.8 删除&&批量删除业务

#### 9.8.1 API&TYPE

```typescript
//删除某一个账号
  DELETEUSER_URL = '/admin/acl/user/remove/',
  //批量删除的接口
  DELETEALLUSER_URL = '/admin/acl/user/batchRemove',
//删除某一个账号的信息
export const reqRemoveUser = (userId: number) => {
  return request.delete<any, any>(API.DELETEUSER_URL + userId)
}
//批量删除的接口
export const reqSelectUser = (idList: number[]) => {
  return request.delete(API.DELETEALLUSER_URL, { data: idList })
}
```

#### 9.8.2 删除业务

1. 绑定点击函数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729113114.png)

2. table收集选中的数据

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729113210.png)



```vue
//table复选框勾选的时候会触发的事件
const selectChange = (value: any) => {
  selectIdArr.value = value
}
```

3. 批量删除回调

```vue
//批量删除按钮的回调
const deleteSelectUser = async () => {
  //整理批量删除的参数
  let idsList: any = selectIdArr.value.map((item) => {
    return item.id
  })
  //批量删除的请求
  let result: any = await reqSelectUser(idsList)
  if (result.code == 200) {
    ElMessage({ type: 'success', message: '删除成功' })
    getHasUser(userArr.value.length > 1 ? pageNo.value : pageNo.value - 1)
  }
}
```

### 9.9 搜索与重置业务

#### 9.9.1 搜索业务

搜索业务与获取初始数据的请求是同一个，因此我们修改一下获取初始业务的请求。更具是否写道username来判断。

```typescript
//获取用户账号信息的接口
export const reqUserInfo = (page: number, limit: number, username: string) => {
  return request.get<any, UserResponseData>(
    API.ALLUSER_URL + `${page}/${limit}/?username=${username}`,
  )
}
```

收集数据：

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729113338.png)

发送请求

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729113400.png)

```vue
//搜索按钮的回调
const search = () => {
  //根据关键字获取相应的用户数据
  getHasUser()
  //清空关键字
  keyword.value = ''
}
```

#### 9.9.2重置业务 

重置业务是通过调用setting仓库实现的

```typescript
import useLayOutSettingStore from '@/store/modules/setting'
//获取模板setting仓库
let settingStore = useLayOutSettingStore()
//重置按钮
const reset = () => {
  settingStore.refresh = !settingStore.refresh
}
```

具体的功能实现是在之前写好的main组件里实现的，通过监听销毁重建组件。

```vue
<template>
  <!-- 路由组件出口的位置 -->
  <router-view v-slot="{ Component }">
    <transition name="fade">
      <!-- 渲染layout一级路由的子路由 -->
      <component :is="Component" v-if="flag" />
    </transition>
  </router-view>
</template>
//监听仓库内部的数据是否发生变化，如果发生变化，说明用户点击过刷新按钮
watch(
  () => layOutSettingStore.refresh,
  () => {
    //点击刷新按钮：路由组件销毁
    flag.value = false
    nextTick(() => {
      flag.value = true
    })
  },
)
```

## 10 角色管理模块

### 10.1 角色管理模块静态搭建

还是熟悉的组件：el-card、el-table 、el-pagination、el-form

```vue
<template>
  <el-card>
    <el-form :inline="true" class="form">
      <el-form-item label="职位搜索">
        <el-input placeholder="请你输入搜索职位关键字"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="default">搜索</el-button>
        <el-button type="primary" size="default">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
  <el-card>
    <el-button type="primary" size="default" icon="Plus">添加职位</el-button>
    <el-table border style="margin: 10px 0px">
      <el-table-column type="index" align="center" label="#"></el-table-column>
      <el-table-column label="ID" align="center" prop="id"></el-table-column>
      <el-table-column
        label="职位名称"
        align="center"
        prop="roleName"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        label="创建时间"
        align="center"
        show-overflow-tooltip
        prop="createTime"
      ></el-table-column>
      <el-table-column
        label="更新时间"
        align="center"
        show-overflow-tooltip
        prop="updateTime"
      ></el-table-column>
      <el-table-column label="操作" width="280px" align="center">
        <!-- row:已有的职位对象 -->
        <template #="{ row, $index }">
          <el-button type="primary" size="small" icon="User">
            分配权限
          </el-button>
          <el-button type="primary" size="small" icon="Edit">编辑</el-button>
          <el-popconfirm :title="`你确定要删除${row.roleName}?`" width="260px">
            <template #reference>
              <el-button type="primary" size="small" icon="Delete">
                删除
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
  <el-pagination
    v-model:current-page="pageNo"
    v-model:page-size="pageSize"
    :page-sizes="[10, 20, 30, 40]"
    :background="true"
    layout="prev, pager, next, jumper,->,sizes,total"
    :total="400"
    @current-change="getHasRole"
    @size-change="sizeChange"
  />
</template>
```

### 10.2 角色管理数据展示

#### 10.2.1 API&&type

api:

```typescript
//角色管理模块的的接口
import request from '@/utils/request'
import type { RoleResponseData, RoleData, MenuResponseData } from './type'
//枚举地址
enum API {
  //获取全部的职位接口
  ALLROLE_URL = '/admin/acl/role/',
}
//获取全部的角色
export const reqAllRoleList = (
  page: number,
  limit: number,
  roleName: string,
) => {
  return request.get<any, RoleResponseData>(
    API.ALLROLE_URL + `${page}/${limit}/?roleName=${roleName}`,
  )
}
```

type:  


```typescript
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
//职位数据类型
export interface RoleData {
  id?: number
  createTime?: string
  updateTime?: string
  roleName: string
  remark?: null
}


//全部职位的数组的ts类型
export type Records = RoleData[]
//全部职位数据的相应的ts类型
export interface RoleResponseData extends ResponseData {
  data: {
    records: Records
    total: number
    size: number
    current: number
    orders: []
    optimizeCountSql: boolean
    hitCount: boolean
    countId: null
    maxLimit: null
    searchCount: boolean
    pages: number
  }
}
```

#### 10.2.2 组件获取数据

```vue
//当前页码
let pageNo = ref<number>(1)
//一页展示几条数据
let pageSize = ref<number>(10)
//搜索职位关键字
let keyword = ref<string>('')
//组件挂载完毕
onMounted(() => {
  //获取职位请求
  getHasRole()
})
//获取全部用户信息的方法|分页器当前页码发生变化的回调
const getHasRole = async (pager = 1) => {
  //修改当前页码
  pageNo.value = pager
  let result: RoleResponseData = await reqAllRoleList(
    pageNo.value,
    pageSize.value,
    keyword.value,
  )
  if (result.code == 200) {
    total.value = result.data.total
    allRole.value = result.data.records
  }
}
```

#### 10.2.3 表格数据

```vue
<el-table border style="margin: 10px 0px" :data="allRole">
        <el-table-column
          type="index"
          align="center"
          label="#"
        ></el-table-column>
        <el-table-column label="ID" align="center" prop="id"></el-table-column>
        <el-table-column
          label="职位名称"
          align="center"
          prop="roleName"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          label="创建时间"
          align="center"
          show-overflow-tooltip
          prop="createTime"
        ></el-table-column>
        <el-table-column
          label="更新时间"
          align="center"
          show-overflow-tooltip
          prop="updateTime"
        ></el-table-column>
        <el-table-column label="操作" width="280px" align="center">
          <!-- row:已有的职位对象 -->
          <template #="{ row, $index }">
            <el-button type="primary" size="small" icon="User">
              分配权限
            </el-button>
            <el-button type="primary" size="small" icon="Edit">编辑</el-button>
            <el-popconfirm
              :title="`你确定要删除${row.roleName}?`"
              width="260px"
            >
              <template #reference>
                <el-button type="primary" size="small" icon="Delete">
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
```

#### 10.2.4 分页器数据

同样的@current-change与@size-change函数回调。

```vue
<el-pagination
      v-model:current-page="pageNo"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 30, 40]"
      :background="true"
      layout="prev, pager, next, jumper,->,sizes,total"
      :total="total"
      @current-change="getHasRole"
      @size-change="sizeChange"
    />
```

```vue
//下拉菜单的回调
const sizeChange = () => {
  getHasRole()
}
```

#### 10.2.5 搜索按钮

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729141428.png)

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729141446.png)

```vue
//搜索按钮的回调
const search = () => {
  //再次发请求根据关键字
  getHasRole()
  keyword.value = ''
}
```

#### 10.2.6 重置按钮

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729141539.png)

```vue
import useLayOutSettingStore from '@/store/modules/setting'
let settingStore = useLayOutSettingStore()
//重置按钮的回调
const reset = () => {
  settingStore.refresh = !settingStore.refresh
}
```

### 10.3 添加&&修改职位

#### 10.3.1 静态

```vue
<!-- 添加职位与更新已有职位的结构:对话框 -->
    <el-dialog v-model="dialogVisite" title="添加职位">
      <el-form>
        <el-form-item label="职位名称">
          <el-input placeholder="请你输入职位名称"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" size="default" @click="dialogVisite = false">
          取消
        </el-button>
        <el-button type="primary" size="default">确定</el-button>
      </template>
    </el-dialog>
```

#### 10.3.2 API&&TYPE

```typescript
//新增岗位的接口地址
  ADDROLE_URL = '/admin/acl/role/save',
  //更新已有的职位
  UPDATEROLE_URL = '/admin/acl/role/update',
//添加职位与更新已有职位接口
export const reqAddOrUpdateRole = (data: RoleData) => {
  if (data.id) {
    return request.put<any, any>(API.UPDATEROLE_URL, data)
  } else {
    return request.post<any, any>(API.ADDROLE_URL, data)
  }
}
```

#### 10.3.3 添加&&修改按钮绑定点击函数

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729141718.png)

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729142602.png)

#### 10.3.4 添加&&修改按钮回调

```vue
//添加职位按钮的回调
const addRole = () => {
  //对话框显示出来
  dialogVisite.value = true
  //清空数据
  Object.assign(RoleParams, {
    roleName: '',
    id: 0,
  })
  //清空上一次表单校验错误结果
  nextTick(() => {
    form.value.clearValidate('roleName')
  })
}
//更新已有的职位按钮的回调
const updateRole = (row: RoleData) => {
  //显示出对话框
  dialogVisite.value = true
  //存储已有的职位----带有ID的
  Object.assign(RoleParams, row)
  //清空上一次表单校验错误结果
  nextTick(() => {
    form.value.clearValidate('roleName')
  })
}
```

#### 10.3.5 表单校验

:model：要校验的数据

:rules：校验的规则

ref：获取表单实例，方便后面调用validate函数来确保校验通过才放行

prop：绑定数据的属性

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729142633.png)

```vue
//自定义校验规则的回调
const validatorRoleName = (rule: any, value: any, callBack: any) => {
  if (value.trim().length >= 2) {
    callBack()
  } else {
    callBack(new Error('职位名称至少两位'))
  }
}
//职位校验规则
const rules = {
  roleName: [{ required: true, trigger: 'blur', validator: validatorRoleName }],
}
```

#### 10.3.6 保存按钮的回调
```vue
//确定按钮的回调
const save = async () => {
  //表单校验结果,结果通过在发请求、结果没有通过不应该在发生请求
  await form.value.validate()
  //添加职位|更新职位的请求
  let result: any = await reqAddOrUpdateRole(RoleParams)
  if (result.code == 200) {
    //提示文字
    ElMessage({
      type: 'success',
      message: RoleParams.id ? '更新成功' : '添加成功',
    })
    //对话框显示
    dialogVisite.value = false
    //再次获取全部的已有的职位
    getHasRole(RoleParams.id ? pageNo.value : 1)
  }
}
```

### 10.4 分配角色权限业务
#### 10.4.1 API&&type（获取全部菜单）
```typescript
//获取全部的菜单与按钮的数据
  ALLPERMISSTION = '/admin/acl/permission/toAssign/',
  //获取全部菜单与按钮权限数据
export const reqAllMenuList = (roleId: number) => {
  return request.get<any, MenuResponseData>(API.ALLPERMISSTION + roleId)
}
```

注意：type这里MenuData与MenuList互相调用，适合这种树状的数据结构

```typescript
//菜单与按钮数据的ts类型
export interface MenuData {
  id: number
  createTime: string
  updateTime: string
  pid: number
  name: string
  code: string
  toCode: string
  type: number
  status: null
  level: number
  children?: MenuList
  select: boolean
}
export type MenuList = MenuData[]
```

#### 10.4.2 获取数据
分配权限按钮：

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729142732.png)

获取&&存储数据

```vue
//准备一个数组:数组用于存储勾选的节点的ID(四级的)
let selectArr = ref<number[]>([])
//已有的职位的数据
const setPermisstion = async (row: RoleData) => {
  //抽屉显示出来
  drawer.value = true
  //收集当前要分类权限的职位的数据
  Object.assign(RoleParams, row)
  //根据职位获取权限的数据
  let result: MenuResponseData = await reqAllMenuList(RoleParams.id as number)
  if (result.code == 200) {
    menuArr.value = result.data
    // selectArr.value = filterSelectArr(menuArr.value, [])
  }
}
```

#### 10.4.3 展示数据

我们重点关注el-tree组件

data：展示的数据
show-checkbox：节点是否可被选择
node-key：每个树节点用来作为唯一标识的属性，整棵树应该是唯一的
default-expand-all：默认展开所有节点
default-checked-keys：默认勾选的节点的 key 的数组
props：属性： label：指定节点标签为节点对象的某个属性值 children:指定子树为节点对象的某个属性值

```vue
const defaultProps = {
  //子树为节点对象的children
  children: 'children',
  //节点标签为节点对象的name属性
  label: 'name',
}
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729142802.png)

#### 10.4.4 展示数据（已分配的权限）

获取已分配权限的id，这里我们只需要收集最后一层的id即可，因为组件会自动更具最后一层的选择情况决定上层的选择状况。

注意：获取最后一层id的函数filterSelectArr使用了递归。

```vue
//分配权限按钮的回调
//已有的职位的数据
const setPermisstion = async (row: RoleData) => {
  //抽屉显示出来
  drawer.value = true
  //收集当前要分类权限的职位的数据
  Object.assign(RoleParams, row)
  //根据职位获取权限的数据
  let result: MenuResponseData = await reqAllMenuList(RoleParams.id as number)
  if (result.code == 200) {
    menuArr.value = result.data
    selectArr.value = filterSelectArr(menuArr.value, [])
  }
}
const filterSelectArr = (allData: any, initArr: any) => {
  allData.forEach((item: any) => {
    if (item.select && item.level == 4) {
      initArr.push(item.id)
    }
    if (item.children && item.children.length > 0) {
      filterSelectArr(item.children, initArr)
    }
  })

  return initArr
} 
```

#### 10.4.5 API&&type（分配权限）

```typescript
//给相应的职位分配权限
SETPERMISTION_URL = '/admin/acl/permission/doAssign/?',
//给相应的职位下发权限
export const reqSetPermisstion = (roleId: number, permissionId: number[]) => {
  return request.post(
    API.SETPERMISTION_URL + `roleId=${roleId}&permissionId=${permissionId}`,
  )
}
```

#### 10.4.6 收集用户分配的权限（每个权限的id）&&发请求

我们这里收集主要用到了2个方法：getCheckedKeys、getHalfCheckedKeys。它们会返回已选择以及半选择用户的id数组

```vue
//抽屉确定按钮的回调
const handler = async () => {
  //职位的ID
  const roleId = RoleParams.id as number
  //选中节点的ID
  let arr = tree.value.getCheckedKeys()
  //半选的ID
  let arr1 = tree.value.getHalfCheckedKeys()
  let permissionId = arr.concat(arr1)
  //下发权限
  let result: any = await reqSetPermisstion(roleId, permissionId)
  if (result.code == 200) {
    //抽屉关闭
    drawer.value = false
    //提示信息
    ElMessage({ type: 'success', message: '分配权限成功' })
    //页面刷新
    window.location.reload()
  }
}
```

#### 10.4.7删除业务

API&&TYPE

```typescript
//删除已有的职位
export const reqRemoveRole = (roleId: number) => {
  return request.delete<any, any>(API.REMOVEROLE_URL + roleId)
}
```

删除的回调

```vue
//删除已有的职位
const removeRole = async (id: number) => {
  let result: any = await reqRemoveRole(id)
  if (result.code == 200) {
    //提示信息
    ElMessage({ type: 'success', message: '删除成功' })
    getHasRole(allRole.value.length > 1 ? pageNo.value : pageNo.value - 1)
  }
}
```

## 11 菜单管理模块

### 11.1 模块初始界面

#### 11.1.1 API&&type

API:

```typescript
import request from '@/utils/request'
import type { PermisstionResponseData, MenuParams } from './type'
//枚举地址
enum API {
  //获取全部菜单与按钮的标识数据
  ALLPERMISSTION_URL = '/admin/acl/permission',
}
//获取菜单数据
export const reqAllPermisstion = () => {
  return request.get<any, PermisstionResponseData>(API.ALLPERMISSTION_URL)
}

```

TYPE:

注意：type这里使用了嵌套

```typescript
//数据类型定义
export interface ResponseData {
  code: number
  message: string
  ok: boolean
}
//菜单数据与按钮数据的ts类型
export interface Permisstion {
  id?: number
  createTime: string
  updateTime: string
  pid: number
  name: string
  code: null
  toCode: null
  type: number
  status: null
  level: number
  children?: PermisstionList
  select: boolean
}
export type PermisstionList = Permisstion[]
//菜单接口返回的数据类型
export interface PermisstionResponseData extends ResponseData {
  data: PermisstionList
}
```

#### 11.1.2 组件获取初始数据

```vue
//存储菜单的数据
let PermisstionArr = ref<PermisstionList>([])
//组件挂载完毕
onMounted(() => {
  getHasPermisstion()
})
//获取菜单数据的方法
const getHasPermisstion = async () => {
  let result: PermisstionResponseData = await reqAllPermisstion()
  if (result.code == 200) {
    PermisstionArr.value = result.data
  }
}
```

#### 11.1.3 模板展示数据

```vue
<div>
    <el-table
      :data="PermisstionArr"
      style="width: 100%; margin-bottom: 20px"
      row-key="id"
      border
    >
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="权限值" prop="code"></el-table-column>
      <el-table-column label="修改时间" prop="updateTime"></el-table-column>
      <el-table-column label="操作">
        <!-- row:即为已有的菜单对象|按钮的对象的数据 -->
        <template #="{ row, $index }">
          <el-button
            type="primary"
            size="small"
            :disabled="row.level == 4 ? true : false"
          >
            {{ row.level == 3 ? '添加功能' : '添加菜单' }}
          </el-button>
          <el-button
            type="primary"
            size="small"
            :disabled="row.level == 1 ? true : false"
          >
            编辑
          </el-button>
          <el-button
            type="primary"
            size="small"
            :disabled="row.level == 1 ? true : false"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
```

### 11.2 更新与添加菜单功能

#### 11.2.1 API&&TYPE

API：

```typescript
//给某一级菜单新增一个子菜单
  ADDMENU_URL = '/admin/acl/permission/save',
  //更新某一个已有的菜单
  UPDATE_URL = '/admin/acl/permission/update',
    //添加与更新菜单的方法
export const reqAddOrUpdateMenu = (data: MenuParams) => {
  if (data.id) {
    return request.put<any, any>(API.UPDATE_URL, data)
  } else {
    return request.post<any, any>(API.ADDMENU_URL, data)
  }
}
```

#### 11.2.2 对话框静态

```vue
<!-- 对话框组件:添加或者更新已有的菜单的数据结构 -->
    <el-dialog
      v-model="dialogVisible"
    >
      <!-- 表单组件:收集新增与已有的菜单的数据 -->
      <el-form>
        <el-form-item label="名称">
          <el-input
            placeholder="请你输入菜单名称"
          ></el-input>
        </el-form-item>
        <el-form-item label="权限">
          <el-input
            placeholder="请你输入权限数值"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="save">确定</el-button>
        </span>
      </template>
    </el-dialog>
```

#### 11.2.3 收集数据

需要的参数一共是4个，其中code、name由v-model绑定的对话框收集。其余俩个通过点击按钮传递的参数收集。

```vue
//携带的参数
let menuData = reactive<MenuParams>({
  code: '',
  level: 0,
  name: '',
  pid: 0,
})
```

```typescript
//添加菜单按钮的回调
const addPermisstion = (row: Permisstion) => {
  //清空数据
  Object.assign(menuData, {
    id: 0,
    code: '',
    level: 0,
    name: '',
    pid: 0,
  })
  //对话框显示出来
  dialogVisible.value = true
  //收集新增的菜单的level数值
  menuData.level = row.level + 1
  //给谁新增子菜单
  menuData.pid = row.id as number
}
//编辑已有的菜单
const updatePermisstion = (row: Permisstion) => {
  dialogVisible.value = true
  //点击修改按钮:收集已有的菜单的数据进行更新
  Object.assign(menuData, row)
}
```

#### 11.2.4 发送请求

```vue
//确定按钮的回调
const save = async () => {
  //发请求:新增子菜单|更新某一个已有的菜单的数据
  let result: any = await reqAddOrUpdateMenu(menuData)
  if (result.code == 200) {
    //对话框隐藏
    dialogVisible.value = false
    //提示信息
    ElMessage({
      type: 'success',
      message: menuData.id ? '更新成功' : '添加成功',
    })
    //再次获取全部最新的菜单的数据
    getHasPermisstion()
  }
}
```

### 11.3 删除模块

#### 11.3.1 API

```typescript
//删除已有的菜单
 DELETEMENU_URL = '/admin/acl/permission/remove/',
//删除某一个已有的菜单
export const reqRemoveMenu = (id: number) => {
  return request.delete<any, any>(API.DELETEMENU_URL + id)
}
```

#### 11.3.2 删除点击函数

```vue
<el-popconfirm
            :title="`你确定要删除${row.name}?`"
            width="260px"
            @confirm="removeMenu(row.id)"
          >
            <template #reference>
              <el-button
                type="primary"
                size="small"
                :disabled="row.level == 1 ? true : false"
              >
                删除
              </el-button>
            </template>
          </el-popconfirm>
```

#### 11.3.3 删除的回调

```vue
//删除按钮回调
const removeMenu = async (id: number) => {
  let result = await reqRemoveMenu(id)
  if (result.code == 200) {
    ElMessage({ type: 'success', message: '删除成功' })
    getHasPermisstion()
  }
}
```

## 12 首页模块

首页模块比较简单，代码量也少。这里直接放上源代码

```vue
<template>
  <div>
    <el-card>
      <div class="box">
        <img :src="userStore.avatar" alt="" class="avatar" />
        <div class="bottom">
          <h3 class="title">{{ getTime() }}好呀{{ userStore.username }}</h3>
          <p class="subtitle">硅谷甄选运营平台</p>
        </div>
      </div>
    </el-card>
    <div class="bottoms">
      <svg-icon name="welcome" width="800px" height="400px"></svg-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getTime } from '@/utils/time'
//引入用户相关的仓库,获取当前用户的头像、昵称
import useUserStore from '@/store/modules/user'
//获取存储用户信息的仓库对象
let userStore = useUserStore()
</script>

<style lang="scss" scoped>
.box {
  display: flex;

  .avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
  }

  .bottom {
    margin-left: 20px;

    .title {
      font-size: 30px;
      font-weight: 900;
      margin-bottom: 30px;
    }

    .subtitle {
      font-style: italic;
      color: skyblue;
    }
  }
}
.bottoms {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}
</style>
```

## 13 setting按钮模块

### 13.1 暗黑模式设置

#### 13.1.1 暗黑模式静态

这里使用了el-switch组件，下面介绍一下属性

@change：点击切换时的回调

v-model：双向绑定的数据，用来控制开关的切换

class：默认的类

style：样式

active-ico、inactive-icon：开和关的图标

inline-prompt：可以把图标放在开关里面

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729142956.png)

13.1.2 暗黑模式![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729143022.png)

```vue
//暗黑模式需要的样式
import 'element-plus/theme-chalk/dark/css-vars.css'
```

#### 13.1.3 切换的回调

```vue
//收集开关的数据
let dark = ref<boolean>(false)
//switch开关的chang事件进行暗黑模式的切换
const changeDark = () => {
  //获取HTML根节点
  let html = document.documentElement
  //判断HTML标签是否有类名dark
  dark.value ? (html.className = 'dark') : (html.className = '')
}
```

### 13.2 主题颜色切换

<font style="color:rgb(48, 49, 51);">Element Plus 默认提供一套主题，也提供了相应的修改主题颜色的方法。我们要使用的时通过js来修改主题颜色</font>

#### <font style="color:rgb(48, 49, 51);">13.2.1 静态搭建</font>

使用了el-color-picker组件

@change:切换的回调

v-model：绑定的数据

show-alpha：是否支持透明度选择

predefine：预定义颜色（会在下面显示

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729143129.png)

#### 13.2.2 点击切换回调

```vue
//主题颜色的设置
const setColor = () => {
  //通知js修改根节点的样式对象的属性与属性值
  const html = document.documentElement
  html.style.setProperty('--el-color-primary', color.value)
}
```

#### 13.2.3 预定义颜色展示

<font style="color:rgb(48, 49, 51);">predefine：预定义颜色</font>

```vue
const predefineColors = ref([
  '#ff4500',
  '#ff8c00',
  '#ffd700',
  '#90ee90',
  '#00ced1',
  '#1e90ff',
  '#c71585',
  'rgba(255, 69, 0, 0.68)',
  'rgb(255, 120, 0)',
  'hsv(51, 100, 98)',
  'hsva(120, 40, 94, 0.5)',
  'hsl(181, 100%, 37%)',
  'hsla(209, 100%, 56%, 0.73)',
  '#c7158577',
])
```

## 15 菜单权限

### 15.1 路由的拆分

#### 15.1.1 路由分析

```markdown
菜单的权限:
超级管理员账号:admin atguigu123   拥有全部的菜单、按钮的权限
飞行员账号  硅谷333  111111       不包含权限管理模块、按钮的权限并非全部按钮
同一个项目：不同人(职位是不一样的,他能访问到的菜单、按钮的权限是不一样的)

一、目前整个项目一共多少个路由！！！
login(登录页面)、
404(404一级路由)、
任意路由、
首页(/home)、
数据大屏、
权限管理(三个子路由)
商品管理模块(四个子路由)

1.1开发菜单权限
---第一步:拆分路由
静态(常量)路由:大家都可以拥有的路由
login、首页、数据大屏、404

异步路由:不同的身份有的有这个路由、有的没有
权限管理(三个子路由)
商品管理模块(四个子路由)

任意路由:任意路由

1.2菜单权限开发思路
目前咱们的项目:任意用户访问大家能看见的、能操作的菜单与按钮都是一样的(大家注册的路由都是一样的)
```

#### 15.1.2 路由的拆分

```typescript
//对外暴露配置路由(常量路由)
export const constantRoute = [
  {
    //登录路由
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    name: 'login', //命名路由
    meta: {
      title: '登录', //菜单标题
      hidden: true, //路由的标题在菜单中是否隐藏
    },
  },
  {
    //登录成功以后展示数据的路由
    path: '/',
    component: () => import('@/layout/index.vue'),
    name: 'layout',
    meta: {
      hidden: false,
    },
    redirect: '/home',
    children: [
      {
        path: '/home',
        component: () => import('@/views/home/index.vue'),
        meta: {
          title: '首页',
          hidden: false,
          icon: 'HomeFilled',
        },
      },
    ],
  },
  {
    path: '/404',
    component: () => import('@/views/404/index.vue'),
    name: '404',
    meta: {
      title: '404',
      hidden: true,
    },
  },
  {
    path: '/screen',
    component: () => import('@/views/screen/index.vue'),
    name: 'Screen',
    meta: {
      hidden: false,
      title: '数据大屏',
      icon: 'Platform',
    },
  },
]

//异步路由
export const asnycRoute = [
  {
    path: '/acl',
    component: () => import('@/layout/index.vue'),
    name: 'Acl',
    meta: {
      hidden: false,
      title: '权限管理',
      icon: 'Lock',
    },
    redirect: '/acl/user',
    children: [
      {
        path: '/acl/user',
        component: () => import('@/views/acl/user/index.vue'),
        name: 'User',
        meta: {
          hidden: false,
          title: '用户管理',
          icon: 'User',
        },
      },
      {
        path: '/acl/role',
        component: () => import('@/views/acl/role/index.vue'),
        name: 'Role',
        meta: {
          hidden: false,
          title: '角色管理',
          icon: 'UserFilled',
        },
      },
      {
        path: '/acl/permission',
        component: () => import('@/views/acl/permission/index.vue'),
        name: 'Permission',
        meta: {
          hidden: false,
          title: '菜单管理',
          icon: 'Monitor',
        },
      },
    ],
  },
  {
    path: '/product',
    component: () => import('@/layout/index.vue'),
    name: 'Product',
    meta: {
      hidden: false,
      title: '商品管理',
      icon: 'Goods',
    },
    redirect: '/product/trademark',
    children: [
      {
        path: '/product/trademark',
        component: () => import('@/views/product/trademark/index.vue'),
        name: 'Trademark',
        meta: {
          hidden: false,
          title: '品牌管理',
          icon: 'ShoppingCartFull',
        },
      },
      {
        path: '/product/attr',
        component: () => import('@/views/product/attr/index.vue'),
        name: 'Attr',
        meta: {
          hidden: false,
          title: '属性管理',
          icon: 'CollectionTag',
        },
      },
      {
        path: '/product/spu',
        component: () => import('@/views/product/spu/index.vue'),
        name: 'Spu',
        meta: {
          hidden: false,
          title: 'SPU管理',
          icon: 'Calendar',
        },
      },
      {
        path: '/product/sku',
        component: () => import('@/views/product/sku/index.vue'),
        name: 'Sku',
        meta: {
          hidden: false,
          title: 'SKU管理',
          icon: 'Orange',
        },
      },
    ],
  },
]

//任意路由
//任意路由
export const anyRoute = {
  //任意路由
  path: '/:pathMatch(.*)*',
  redirect: '/404',
  name: 'Any',
  meta: {
    title: '任意路由',
    hidden: true,
    icon: 'DataLine',
  },
}
```

### 15.2 菜单权限的实现

#### 15.2.1 获取正确路由的方法

注意：这里使用了递归。其次，这里是浅拷贝，会改变原有的路由。因此还需要改进。

```typescript
//硅谷333: routes['Product','Trademark','Sku']
let guigu333 = ['Product', 'Trademark', 'Sku'];
function filterAsyncRoute(asnycRoute, routes) {
  return asnycRoute.filter(item => {
    if (routes.includes(item.name)) {
      if (item.children && item.children.length > 0) {
        item.children = filterAsyncRoute(item.children, routes)
      }
      return true
    }
  })
}
//硅谷333需要展示的异步路由
let guigu333Result = filterAsyncRoute(asnycRoute, guigu333);
console.log([...constRoute, ...guigu333Result, anyRoute], '硅谷333');
```

#### 15.2.2 获取路由

```typescript
。。。。。。

import router from '@/router'
//引入路由（常量路由）
import { constantRoute, asnycRoute, anyRoute } from '@/router/routes'
//用于过滤当前用户需要展示的异步路由
function filterAsyncRoute(asnycRoute: any, routes: any) {
  return asnycRoute.filter((item: any) => {
    if (routes.includes(item.name)) {
      if (item.children && item.children.length > 0) {
        //硅谷333账号:product\trademark\attr\sku
        item.children = filterAsyncRoute(item.children, routes)
      }
      return true
    }
  })
}
//创建用户小仓库
const useUserStore = defineStore('User', {
  //小仓库存储数据地方
  state: (): UserState => {
    return {
      。。。。。。。
      menuRoutes: constantRoute, //仓库存储生成菜单需要数组（路由）
      us。。。。。。
    }
  },
  //处理异步|逻辑地方
  actions: {
    。。。。。。。
    //获取用户信息方法
    async userInfo() {
      //获取用户信息进行存储
      const result: userInfoResponseData = await reqUserInfo()
      if (result.code == 200) {
        this.username = result.data.name
        this.avatar = result.data.avatar
        //计算当前用户需要展示的异步路由
        const userAsyncRoute = filterAsyncRoute(asnycRoute, result.data.routes)
        //菜单需要的数据整理完毕
        this.menuRoutes = [...constantRoute, ...userAsyncRoute, anyRoute]
        //目前路由器管理的只有常量路由:用户计算完毕异步路由、任意路由动态追加
        ;[...userAsyncRoute, anyRoute].forEach((route: any) => {
          router.addRoute(route)
        })
        return 'ok'
      } else {
        return Promise.reject(new Error(result.message))
      }
    },
    。。。。。。
})
//对外暴露小仓库
export default useUserStore
```

### 15.3 菜单权限的2个小问题

#### 15.3.1 深拷贝

之前获取需要的路由方法中使用的是浅拷贝，会改变原有的路由。因此我们这里引入深拷贝的方法

```typescript
//引入深拷贝方法
//@ts-expect-error
import cloneDeep from 'lodash/cloneDeep'
。。。。。。
 //获取用户信息方法
    async userInfo() {
      //获取用户信息进行存储
      const result: userInfoResponseData = await reqUserInfo()
      if (result.code == 200) {
        this.username = result.data.name
        this.avatar = result.data.avatar
        //计算当前用户需要展示的异步路由
        const userAsyncRoute = filterAsyncRoute(
          cloneDeep(asnycRoute),
          result.data.routes,
        )
        //菜单需要的数据整理完毕
        this.menuRoutes = [...constantRoute, ...userAsyncRoute, anyRoute]
        //目前路由器管理的只有常量路由:用户计算完毕异步路由、任意路由动态追加
        ;[...userAsyncRoute, anyRoute].forEach((route: any) => {
          router.addRoute(route)
        })
        return 'ok'
      } else {
        return Promise.reject(new Error(result.message))
      }
    },
```

#### 15.3.2 路由加载问题

这样配置路由后，如果你访问的是异步路由，会在刷新的时候出现空白页面。原因是异步路由是异步获取的，加载的时候还没有。因此我们可以在路由守卫文件中改写。这个的意思就是一直加载。

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729143229.png)



```typescript
//用户登录判断
  if (token) {
    //登陆成功，访问login。指向首页
    if (to.path == '/login') {
      next('/')
    } else {
      //登陆成功访问其余的，放行
      //有用户信息
      if (username) {
        //放行
        next()
      } else {
        //如果没有用户信息，在收尾这里发请求获取到了用户信息再放行
        try {
          //获取用户信息
          await userStore.userInfo()
          //万一刷新的时候是异步路由，有可能获取到用户信息但是异步路由没有加载完毕，出现空白效果
          next({ ...to })
        } catch (error) {
          //token过期|用户手动处理token
          //退出登陆->用户相关的数据清空

          await userStore.userLogout()
          next({ path: '/login', query: { redirect: to.path } })
        }
      }
    }
  } else {
    //用户未登录
    if (to.path == '/login') {
      next()
    } else {
      next({ path: '/login', query: { redirect: to.path } })
    }
  }
```

## 16 按钮权限

对于不同的用户，按钮的的显示与否

### 16.1 获取用户应有的按钮

记得修改对应的type

```typescript
//创建用户相关的小仓库
import { defineStore } from 'pinia'
//引入接口
import { reqLogin, reqUserInfo, reqLogout } from '@/api/user'
import type {
  loginFormData,
  loginResponseData,
  userInfoResponseData,
} from '@/api/user/type'
import type { UserState } from './types/type'

import router from '@/router'
。。。。。。
//创建用户小仓库
const useUserStore = defineStore('User', {
  //小仓库存储数据地方
  state: (): UserState => {
    return {
      token: GET_TOKEN(), //用户唯一标识token
      menuRoutes: constantRoute, //仓库存储生成菜单需要数组（路由）
      username: '',
      avatar: '',
      //存储当前用户是否包含某一个按钮
      buttons: [],
    }
  },
  //处理异步|逻辑地方
  actions: {
    。。。。。。
    //获取用户信息方法
    async userInfo() {
      //获取用户信息进行存储
      const result: userInfoResponseData = await reqUserInfo()
      if (result.code == 200) {
        this.username = result.data.name
        this.avatar = result.data.avatar
        this.buttons = result.data.buttons
        console.log(result)
        //计算当前用户需要展示的异步路由
        const userAsyncRoute = filterAsyncRoute(
          cloneDeep(asnycRoute),
          result.data.routes,
        )
        //菜单需要的数据整理完毕
        this.menuRoutes = [...constantRoute, ...userAsyncRoute, anyRoute]
        //目前路由器管理的只有常量路由:用户计算完毕异步路由、任意路由动态追加
        ;[...userAsyncRoute, anyRoute].forEach((route: any) => {
          router.addRoute(route)
        })
        return 'ok'
      } else {
        return Promise.reject(new Error(result.message))
      }
    },
  。。。。。。
})
//对外暴露小仓库
export default useUserStore
```

### 16.2 自定义指令指令

这个需要你在每个按钮元素中使用v-has="<font style="color:rgb(200, 0, 0);">btn.User.XXXX</font>"去判断。比v-if方便。不需要在组件内部引入仓库

```typescript
import pinia from '@/store'
import useUserStore from '@/store/modules/user'
const userStore = useUserStore(pinia)
export const isHasButton = (app: any) => {
  //获取对应的用户仓库
  //全局自定义指令:实现按钮的权限
  app.directive('has', {
    //代表使用这个全局自定义指令的DOM|组件挂载完毕的时候会执行一次
    mounted(el: any, options: any) {
      //自定义指令右侧的数值:如果在用户信息buttons数组当中没有
      //从DOM树上干掉
      //el就是dom元素
      //options:传入进来的值
      if (!userStore.buttons.includes(options.value)) {
        el.parentNode.removeChild(el)
      }
    },
  })
}
```

![](https://raw.githubusercontent.com/pleb631/ImgManager/main/img/20250729143259.png)
