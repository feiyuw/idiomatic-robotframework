title: RobotFramework简介及其在Nokia Networks的应用
speaker: Zhang Yu
url: https://github.com/feiyuw/idiomatic-robotframework
transition: cards
files: /js/demo.js,/css/demo.css,/css/theme.moon.css

[slide]

# RobotFramework简介及其在Nokia Networks的应用
## 演讲者：Zhang Yu

![RobotFramework](/img/robotframework.png "RobotFramework")

[slide]

## RobotFramework是什么
----
* 一个开源的测试自动化框架 {:&.moveIn}
* 以类自然语言的方式来编写自动化case
* 基于Python实现, 支持Python和Jython
* 支持Linux, Windows和Mac
* 关键字驱动
* 简明友好的测试报告
* 可以使用Python/Java编写keyword进行扩展
* 可以使用其他语言通过remote接口来进行扩展

[slide]

## RobotFramework的诞生历程

* 2005年, Pekka在准备硕士论文的过程中实现了一个原型 {:&.moveIn}
* 2005年秋季, 在Nokia Networks, Pekka和其他Robot Dev团队的基于上述原型开始开发RobotFramework, 并于几个月之后付诸使用
* 2008年6月, RobotFramework 2.0版本发布, 并正式对外开源, RobotFramework进入快速发展阶段

[slide]

## 今天的RobotFramework

* 月均**60000**下载 {:&.moveIn}
* 超过**2000**用户在robotframework-users邮件列表中
* 包括中国在内的多个国家的许多公司正在采用这个框架
* 在Nokia Networks, 有不同产品线的超过**1000**名工程师在使用RobotFramework

[note]
The framework is based on studies and prototypes that I did for my
Master's Thesis back in 2005. I hadn't even yet finished the Thesis
when an old colleague called and told they needed a large scale
automation framework for a heterogeneous environment at Nokia
Networks. They liked the prototypes I had, and we started developing a
better framework based on it at Nokia autumn 2005. The framework was
taken into real use only few months later, and its usage has then
organically grow so that there are nowadays thousands of uses at
Nokia.

Our plan was to open source the framework from the very beginning. It
took some time to get lawyers to agree on that, but we finally got a
permission and Robot Framework 2.0 was publicly announced in June
2008. Since then the usage and the community has grown around the
world, and nowadays there are dozens of ready-made test libraries and
other tools developed by the community available in the ecosystem.
It's impossible to tell how many users there are worldwide, but based
on the number of members on the public robotframework-users mailing
list (about 2000) and current download counts (about 60000 per month),
I would estimate that the number is tens of thousands.

If there's any more information you need let me know! If you are
interested, the aforementioned Master's Thesis is available here:
http://eliga.fi/writings.html
[/note]

[slide]

## 支持的library

----
* Standard Library
    * BuiltIn
    * OperatingSystem
    * String
    * Remote
    * Collections
    * Telnet
    * ...
* External Library
    * Selenium2
    * SSH
    * Android
    * iOS
    * ...

[slide]

## Demo

[note]
使用demo目录下的应用来演示
[/note]

[slide]

## RobotFramework在Nokia Networks的应用

* X*10000 cases {:&.moveIn}
* X*1000 keywords
* 每天上万个case会被执行
* 每天生成超过100G的测试报告
* [示例Case](http://10.56.117.81/IPA_TRUNK/TestCase/DATest/DC/FMA/Alarm/B01927_FUT_012_TA_all_active_star_alarms_should_be_uploaded_to_OMS_successfully_by_total_type.html), [示例Log](http://10.56.117.81/archiver2/10_56_117_81/tep-ci2/Worker-il-BCN173-FPC51/Archive_1284.zip!/logs/robot_logs/10.68.156.78_log.html)
