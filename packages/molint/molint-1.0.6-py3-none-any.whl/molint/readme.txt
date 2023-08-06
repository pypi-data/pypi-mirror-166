1、molint安装
pip install molint

2、查看帮助信息
molint -h

usage: python code scan [-h] [code_path] [lint_rule] [dis]
positional arguments:
  code_path   代码路径
  lint_rule   过滤目录
  dis         过滤条件

code_path:需要扫描的项目根目录，可不填，不填时为当前目录
lint_rule:忽略一些文件夹（注意输入文件夹的目录，不要输入文件夹的路径），多个用逗号隔开，如test1,test2，可不填
dis:忽略一些错误信息，多个用逗号隔开，如C0114,C0115，可不填

3、使用

molint  扫描当前目录

molint D:\aa  扫描D:\aa目录

molint D:\aa test1,test2  扫描D:\aa目录,忽略test1,test2文件夹

molint D:\aa test1,test2 C0304,C0114 扫描D:\aa目录,忽略test1,test2文件夹,忽略C0304,C0114错误

molint D:\aa ' C0304,C0114  若只想忽略一些错误，不想忽略文件夹，使用'来占位lint_rule