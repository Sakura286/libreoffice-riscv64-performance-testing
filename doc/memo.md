
# 一些笔记

## macros security level 问题

起因：

使用 UITest 打开带有宏（macros）的文档会提示需要我手动更改 macros security setting，这样是无法自动化的，需要解决方案

检索“enable macros libreoffice”，出来的结果是在图形化界面手动 tools -> options -> Security -> Security -> Macro Security -> low。手动更改这个设置后对于 UITest 无效。

继续检索“enable macros libreoffice cli”，出来的结果大都是通过 headless（无图形界面）模式进行启动，并未直接解决问题

使用 root 权限运行 libreoffice，发现 macros security “恢复”成了默认状态，可以确定一点：libreoffice 在用户模式下与管理员模式下分别使用了不同的配置，进而可以推断，使用 UITest 的时候与用户模式也用了不同的配置

既然我们在图形界面修改过了 macros security 的设置，那么用户模式下的配置文件应该会留下痕迹。进入 ~/.config/libreoffice/4 ，检索该文件夹，发现了`MacroSecurityLevel`这样的变量，检索“set MacroSecurityLevel in cli libreoffice”，终于出现了有些相关的内容

然而没有涉及到 UITest 及 CLI 的内容，所以先自己想办法

既然运行脚本会生成 /tmp/libreoffice/4/user 文件夹，那么就可以在脚本里不删除它，手动在 registrymodifications.xcu 里添加如下一行

```xml
<item oor:path="/org.openoffice.Office.Common/Security/Scripting"><prop oor:name="MacroSecurityLevel" oor:op="fuse"><value>0</value></prop></item>
```
