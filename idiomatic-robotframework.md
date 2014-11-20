title: Idiomatic RobotFramework
speaker: Zhang Yu
url: https://github.com/feiyuw/idiomatic-robotframework
transition: cards
files: /css/theme.moon.css

[slide style="background-image:url('/img/robotframework.jpg')"]

# Idiomatic RobotFramework {:&.flexbox.vleft}
## From：Zhang Yu

[slide]

# PART 1  重新认识RobotFramework {:&.moveIn}
## 起初神创造天地。地是空虚混沌。渊面黑暗。神的灵运行在水面上。神说，要有光，就有了光。神看光是好的，就把光暗分开了。神称光为昼，称暗为夜。有晚上，有早晨，这是头一日。

[slide]

## 你对TA的认识有哪些?
----
* 测试数据 {:&.moveIn}
* 业务逻辑
* 结果验证
* TA也是软件开发的一种
[note]
### 测试 vs. 验证
### 讨论: 什么样的场景适合/不适合TA
* 经常变化的业务(如Web UI)
* 命令行接口
* FTP上传下载
* 应用程序的API
* 打印
[/note]

[slide]

## 你对RobotFramework的认识有哪些?
----
* 一个开源的测试自动化框架 {:&.moveIn}
* 以类自然语言的方式来编写自动化case
* 基于Python实现
* 支持Linux, Windows和Mac
* Keyword Driven
* 可以使用Python编写Keyword进行扩展
* 可以使用其他语言编写Keyword/Remote Keyword来进行扩展

[slide]

## 你知道执行pybot后RobotFramework都做了些什么吗?
----
* 实例化robot.run.RobotFramework {:&.moveIn}
* 命令行参数解析
* 实例化RobotSettings
* 设置LOGGER
* 生成TestSuite
* 执行TestSuite
* 写入log和report
* 判断测试结果
* 结束进程
[note]
* 写入log和report为optional步骤
* 如果有keyword产生的子进程无法结束, 则pybot无法结束
[/note]

[slide]

### 相关代码robot.run.RobotFramework
----
```python
class RobotFramework(Application):

    def __init__(self):
        Application.__init__(self, USAGE, arg_limits=(1,),
                             env_options='ROBOT_OPTIONS', logger=LOGGER)

    def main(self, datasources, **options):
        settings = RobotSettings(options)
        LOGGER.register_console_logger(**settings.console_logger_config)
        LOGGER.info('Settings:\n%s' % unicode(settings))
        suite = TestSuiteBuilder(settings['SuiteNames'],
                                 settings['WarnOnSkipped'],
                                 settings['RunEmptySuite']).build(*datasources)
        suite.configure(**settings.suite_config)
        result = suite.run(settings)
        LOGGER.info("Tests execution ended. Statistics:\n%s"
                    % result.suite.stat_message)
        if settings.log or settings.report or settings.xunit:
            writer = ResultWriter(settings.output if settings.log else result)
            writer.write_results(settings.get_rebot_settings())
        return result.return_code
```

[slide]

## 你有用过下面这些feature吗?
----
* 将通用的keyword和variable封装为Resource File {:&.moveIn}
* 对某些动态的变量或者复杂变量使用Variable File
* 在suite目录下通过\_\_init\_\_进行全局的suite setup和suite teardown
* 使用Listener在robot执行的时候做一些通用的工作(如Debug)
* 使用全局变量来动态控制case的执行环境等(pybot -v VAR:XXX)
* 使用其他pybot的命令行参数来对case进行过滤, 随机调整suite/case执行顺序等
* 向pybot进程发送kill -2来停止robot执行, 并生成log

[slide]

## 从suite开始
----
* suite还是test? {:&.moveIn}
    * 测试的范围是否跨多个feature或者功能点, 尽可能将同一个feature和功能点的测试放在一起 {:&.moveIn}
    * 是否有类似case存在, 存在则在现有suite中添加
* suite的结构化 vs. python中module, class和function
* resource文件, library文件放在哪?
    * case同级或者上级目录的resources目录中 {:&.moveIn}
    * 不应该存在对子目录resource或者library文件的调用
* resource, library文件的结构化
    * 只允许子目录继承父目录 {:&.moveIn}
    * 尽量避免同目录内的交叉引用

[slide]

### suite的默认执行顺序
----
* ![suite执行顺序](/img/suite.png "suite执行顺序")
* 相关代码
```python
# robot.parsing.populators.FromDirectoryPopulator
def _list_dir(self, path):
    # os.listdir returns Unicode entries when path is Unicode
    names = os.listdir(unic(path))
    for name in sorted(names, key=unicode.lower):
        # unic needed to handle nfc/nfd normalization on OSX
        yield unic(name), unic(os.path.join(path, name))
```

[slide]

### suite的随机执行顺序
----
* "--randomize"参数可以将suite/case的执行顺序进行随机调整
```python
class Randomizer(SuiteVisitor):

    def __init__(self, randomize_suites=True, randomize_tests=True, seed=None):
        # ......
        args = (seed,) if seed is not None else ()
        self._shuffle = Random(*args).shuffle

    def start_suite(self, suite):
        # ......
        if self.randomize_suites:
            self._shuffle(suite.suites)
        if self.randomize_tests:
            self._shuffle(suite.tests)
        # ......
```
[note]
效果类似于:
```
In [1]: from random import Random
In [2]: x = Random().shuffle
In [3]: l = range(4)
In [4]: l
Out[4]: [0, 1, 2, 3]
In [5]: x(l)
In [6]: l
Out[6]: [3, 0, 1, 2]
```
[/note]

[slide]

## 使用\_\_init\_\_文件
----
* Documentation {:&.moveIn}
* Meta Data
* Force Tags
* Suite Setup和Suite Teardown
* 目录级别的Tags
* 所有case的默认Test Setup, Test Teardown和Test Timeout

[slide]

## 让测试分组
----
* Q: 有如下Web应用的TA场景, 怎么组织suite和case? {:&.moveIn}
    * 用户以root/password登陆, 可以跳转到success.html {:&.moveIn}
    * 用户以root/invalid登陆, 可以跳转到invalid.html
    * 用户都可以通过link "/download"下载数据
    * 用户登陆成功后, 可以通过link "/upload"上传数据
    * 用户可以通过ftp协议的"/download" link下载数据
    * 用户可以通过rsync协议的"/download" link下载数据
    * 用户可以向其他已登陆用户发送消息
* 以Feature而不是人/组织来组织suite
* 通过Tags来区分人和组织
[note]
![Web TA](/img/webta.png "Web TA")
### 课后思考
* 哪些场景适合用Keyword Driven?
* 哪些场景适合用Data Driven?
* 哪些场景适合用Behaviour Driven?
[/note]

[slide]

## suite组织上的常见问题
----
* 没有\_\_init\_\_文件 {:&.moveIn}
* 一个txt|html文件仅包含一个case
* 一个txt|html文件包含超过10个case
* setup和teardown的步骤都在case中
* 根据team或者部门来组织suite目录结构

[slide]

## 使用Variable File让变量更聪明
----
* Variable File的优势 {:&.moveIn}
    * 获取动态数据 {:&.moveIn}
    * 获取复杂的数据结构
    * 利用Python进行逻辑判断
* 代码示例
```python
def get_variables(host):
    try:
        # ......
        return {"PACKAGE_VERSION_LONG" : long,
                "PACKAGE_VERSION" : short,
                "SYSTEM_PLATFORM" : system,
                "TEST_ENV" : test_env}
    except :
        return {"PACKAGE_VERSION_LONG" : "NA",
                "PACKAGE_VERSION" : "NA",
                "SYSTEM_PLATFORM" : "NA",
                "TEST_ENV" : "NA"}
    finally:
        # ......
```

[slide]

## 使用listener扩展RobotFramework
----
* 什么时候用listener {:&.moveIn}
    * 测试之外的需求, 如统计, 调试等 {:&.moveIn}
    * 统一要求的测试需求, 如文件清理, CI环境恢复等
    * 临时的测试需求
* 避免滥用listener
* [一个复杂的示例](http://becrtt01.china.nsn-net.net/platformci/coci-runner/tree/master/src/ipaci/rdb)

[slide style="background-image:url('/img/anotherway.jpg')"]

# PART 2: 换一种方式写TA

[slide style="background-image:url('/img/datadriven.jpg')"]

## 你写过Data Driven的case吗?

[slide style="background-image:url('/img/behaviourdriven.jpg')"]

## 你写过Behavior Driven的case吗?

[slide style="background-image:url('/img/designpattern.png')"]

# TA也有设计模式

[slide]

## Keyword Driven模式
----
* 每一个业务点相对固定 {:&.moveIn}
* 业务点之间可以互相组合
* 验证点随组合不同而不同
* [示例](/examples/kw-driven.robot)

[slide]

## 什么时候用Data Driven模式?
----
* 测试基于数据和反馈, 如登陆 {:&.moveIn}
* 测试步骤相同
* 数据组合较多
* [示例1](/examples/data-driven.robot)
* [示例2](/examples/data-driven-arguments.robot)
[note]
* 所有的示例基于robotframework 2.8.6版本
[/note]

[slide]

## 什么时候用Behaviour Driven模式?
----
* 测试用例就是文档 {:&.moveIn}
* 测试用例的设计是以user case来驱动的
* [示例](/examples/bdd.robot)

[slide style="background-image:url('/img/bullet.jpg')"]

# PART 3: 充实我们的弹药库

[slide]

## 你写过keyword吗?
----
* 一个典型的keyword {:&.moveIn}
```python
def create_list(*items):
    """Returns a list containing given items.

    The returned list can be assigned both to `${scalar}` and `@{list}`
    variables.

    Examples:
    | @{list} =   | Create List | a    | b    | c    |
    | ${scalar} = | Create List | a    | b    | c    |
    | ${ints} =   | Create List | ${1} | ${2} | ${3} |
    """
    return list(items)
```
[note]
* 名字
* 参数
* 返回值
* 文档
[/note]

[slide]

## 你的keyword是什么样的?
----
* 开发语言是什么? {:&.moveIn}
* 有依赖吗?
* 有被依赖吗?
* 支持Linux吗?
* 支持Windows吗?

[slide]

## keyword设计的一些准则
----
* 一个keyword是一个原子操作 {:&.moveIn}
* keyword的参数应该是一个简单数据类型, 多数情况下应该是String
* 不同级别的keyword需要分离
* 抛出错误, 而不是捕获它
* 调用其他的keyword, 应该只需要知道它的名字
* 一个keyword的重构(如移动, 添加optional的参数), 不应该影响其他keyword和case
* 单元测试是必须的, 鼓励TDD
* keyword的设计也需要遵循其他Python编码的规范

[slide]

## keyword编写中的一些常见问题
----
* 为了适应不同的场景, 添加很多的可选参数, [示例](/examples/unit_state.py) {:&.moveIn}
* 同一个参数支持多种数据类型, 导致冗长的参数判断逻辑, [示例](/examples/tm500.py)
* 复杂的参数类型, 通常情况下参数应该是字符串
* 以C/Java的风格写Python
* 其它与clean code相违背的问题
    * boolean参数 {:&.moveIn}
    * defensive programming, 典型情形: 对参数进行类型检查
    * setter函数有返回值
    * getter函数中有对业务的修改操作

[note]
```python
# 重构前
Key_List = []
Value_List = []
for target in Need_to_Modify:
     if len(target)==0:
        para_len=para_len+1
        continue
     tmp = target.split(':')
     Key_List.append(tmp[0].upper())
     Value_List.append(tmp[1].upper())
# 重构后
para_dict = dict(map(lambda x: x.upper().split(':', 1), Need_to_Modify))
```
练习: 对第二个例子进行重构
[/note]

[slide]

## 不可或缺地单元测试
----
* 什么时候写单元测试? {:&.moveIn}
* 验证什么?
* 你的单元测试安全吗?
* 单元测试的效率
* [示例函数](/examples/utils.py), [示例UT](/examples/test_utils.py)

[slide]

## keyword也需要持续集成
----
* 版本控制 {:&.moveIn}
* 代码审查
* 单元测试
* 持续发布
* 协同开发

[slide style="background-image:url('/img/nextstep.jpg')"]

* ## Case/keyword的Review {:&.moveIn}
* ## Refactoring
* ## Open Source

[slide]

# 下一期预告
----
* 基于RobotFramework的Web UI测试的开源解决方案
