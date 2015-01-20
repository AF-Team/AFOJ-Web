#encoding=utf-8
ACCESS_BACKEND = 1
ADD_PROBLEM = 2
ADD_CONTEST = 4
ADD_ANNOUNCE = 8
ADMIN = ACCESS_BACKEND + ADD_PROBLEM + ADD_CONTEST + ADD_ANNOUNCE
VERDICT_NAME=(
	(0,'V_ALL','各种状态'),
	(1,'V_Q','<span class="glyphicon glyphicon-refresh"></span> 队列中'),
	(2,'V_C','<span class="glyphicon glyphicon-refresh"></span> 编译'),
	(3,'V_CE','<span class="glyphicon glyphicon-remove"></span> 编译错误'),
	(4,'V_RUN,''<span class="glyphicon glyphicon-refresh"></span> 运行中'),
	(5,'V_AC','<span class="glyphicon glyphicon-ok"></span> 正确'),
	(6,'V_WA','<span class="glyphicon glyphicon-remove"></span> 错误'),
	(7,'V_RE',' <span class="glyphicon glyphicon-remove"></span> 运行错误'),
	(8,'V_TLE',' <span class="glyphicon glyphicon-remove"></span> 时间超限'),
	(9,'V_MLE',' <span class="glyphicon glyphicon-remove"></span>内存超限'),
	(10,'V_PE','<span class="glyphicon glyphicon-remove"></span> 格式错误'),
	(11,'V_OLE','<span class="glyphicon glyphicon-remove"></span> 输出超限'),
	(12,'V_RF',),
	(13,'V_OOC',),
	(14,'V_SE',),
	)
LANGUAGE=(
	(0,'C'),
	(1,'C++'),
	(2,'Java'),
	)

