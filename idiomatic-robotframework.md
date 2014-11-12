title: Idiomatic RobotFramework
speaker: Zhang Yu
url: https://github.com/feiyuw/idiomatic-rf
transition: cards
files: /css/theme.moon.css

[slide style="background-image:url('/img/robotframework.jpg')"]

# Idiomatic RobotFramework {:&.flexbox.vleft}
## From：Zhang Yu

[slide]

# PART 1  挑选合适的武器

![武器库](/img/weapon.jpg "武器库")

[slide style="background-image:url('/img/question.png')"]

## 你知道RobotFramework吗?

[slide]

## 你用RobotFramework多久了?
----
* 刚刚接触 {:&.moveIn}
* 写过一两个case
* 用过一段时间
* 很久了

[slide]

## 你知道执行pybot后RobotFramework都做了些什么吗?
----
* 实例化robot.run.RobotFramework {:&.moveIn}
* 实例化RobotSettings
* 设置LOGGER
* 生成TestSuite
* 执行TestSuite
* 写入log和report
* 判断测试结果
* 结束进程

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
* \_\_init\_\_.txt {:&.moveIn}
* Resource File
* Variable File
* Listener
* 全局变量
* 命令行参数
* 向pybot进程发送signal

[slide]

## 从suite开始
----
* suite是什么? {:&.moveIn}
* 执行顺序?
* suite的层级关系
* resource文件, library文件放在哪?

[slide]

## 使用__init__文件

[slide]

## 让测试分组

[slide]

## suite组织上的常见问题

[slide]

## 使用Variable File让变量更聪明
----
* Variable File的优势 {:&.moveIn}
* 让变量随环境改变

[slide]

## 使用listener扩展RobotFramework
----
* 什么时候用listener {:&.moveIn}
* 避免滥用listener

[slide]

# PART 2: 换一种方式写TA

[slide]

## 你写过Data Driven的case吗?

[slide]

## 你写过Behavior Driven的case吗?

[slide]

## TA也有设计模式

[slide]

# PART 3: 充实我们的弹药库

[slide]

## 你写过keyword吗?

[slide]

## 你的keyword是什么样的?
----
* 开发语言是什么? {:&.moveIn}
* 有依赖吗?
* 有被依赖吗?
* 支持Linux吗?
* 支持Windows吗?

[slide]

## keyword也需要持续集成
----
* 版本控制 {:&.moveIn}
* 代码审查
* 单元测试
* 持续发布
* 协同开发

[slide]

# 迈出下一步
----
* Case/keyword的Review {:&.moveIn}
* Refactoring
* Open Source

[slide]

# 下一期预告
----
* 基于RobotFramework的Web UI测试的开源解决方案
