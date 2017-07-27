<h1><center>Actor as Sranular, A Symmetric Micro-services Architecture</center></h1>


**<center>Ryan J.K</center>**
**<center>ryankung(at)ieee.org</center>**

## TR；DR:

为什么Actor是解决微服务的最好方法：

1. 微服务问题本质上是一个分布式的问题：

	1. 分布式问题的的定义出自于Lamport，所以不要说理论定义不严格
	2. 大部分微服务都会绑着一个分布式一致性算法实现比如说paxos或者raft，它本质上就是个分布式，或者分布式的延伸
2. Actor 大法好
	1. Actor 是 CSP的实现，虽然golang的gocoroutine也号称是CSP的的实现，但是那个垃圾，没有按照原始定义来做
	2. 原始定义是 C.A.R Hoare 给的，和Lamport一样都是图灵奖获得者，Lamport对CSP有明确表态，好，好，好。
3. FRP 大法好
	1. 耶鲁憋FRP憋了好几年，就为了解决建模的问题，FRP和Actor模型其实非常类似，只不过前者是基于时序事件，而且没有分布式概念，当时的动机似乎主要是为了玩音乐!！FRP这一块在haskell社区似乎搞了十几年，最近被前端抄抄抄了
	2. 本质上，大家都在做相同的事情。然而前端能够直接迅速的吸收学术界的东西，至少令前端有点计算机科学的样子，十年前他们只是调试IE6的。

4. 能解决的问题
	Actor和FRP能解决的问题其实都是副作用的问题，而副作用的问题主要就是IO的问题。
	
	比如说在prefork情况下，一个WsgiIO拖着对等数量的DBIO，跑，两个IO在同一个进程里。不好。为什么不好。我需要100个进程听Wsgi，只需要十个进程去听DBIO，怎么调？开线程？
	比如说在线程或者coroutine的情况下，一堆线程协程共享同一块内存。不好。为什么不好？锁起来没完没了，线程池没完没了，连接池没完没了。这池那池，这锁那锁。恩，可能监控比较容易，但monitoring是人家1972年就淘汰的概念.
	1965年，人家搞共享变量（全局变量）
	1968年，人家搞semaphore，全局信号
	1972年，人家搞monitors
	终于1978年搞了个CSP，没有副作用了，隔离了！none-causal language了！Lamport很开心，Hoare很开心，产生了Erlang这种完美实现到了现在。
	
	那么，微服务需要解决什么问题：
	
	1. 要小。
	2. 要可组合
	3. 要对等，完整，各自能跑，组合起来也能跑
	
	当然，你也可以说还有监控的问题，一致性的问题，发现的问题，但这些其实都是基于上面几点的扯淡的问题。

	这些bullshit,可能看起来是副作用的问题，建模的问题，monad的问题，分布式系统的问题，函数式变成的问题，响应事件的问题，但它们都是，本质上是前人已经解决了的问题。
	
	然后所谓微服务，就是2005年的时候，微软跳出来几个人重新发现了问题。然后我们来重新解决问题（大神们应该懒得动手了，心想，一群傻逼）
	
	八个卦，Actor modeling的初始论文是“A Universal Modular Actor Formalism for Artificial Intelligence". IJCAI.”，对的，他强行蹭了上一波人工智能的热点。现在看来，简直就是黑历史啊黑历史。
	
	Actor modeling 的所谓对等性是什么呢。就是我的每一个service，都是first class的。并不存在一个services io包括好几个其他IO的情况。这里的好处是什么呢？随便拆，随便组合，随便监控。随便写单元测试。完全不用考虑状态。
	
	然后来说pulsar的事儿
	
	Pulsar是一个Python的Actor的实现。其实在某种意义上来说Python不适合多线程只适合多进程可以是非常好的优势。但是大家普遍不会玩，最多完成coroutine那种样子，切个上下文而已，就不会搞了。具体的Python并发之类的，可以看CMGS之前的《Python网络编程乱弹琴》	https://www.douban.com/note/341479741/
	
	“
	接着我们有了pulsar这个库，直接照搬了erlang的Actor模型来了。actor虽然看上去有5个字符跟reactor一样，但这可是两种完全不同的概念。stackless python里面每一个task就可以看成是个actor。比起「coroutine」而言，actor的行为是通过外部message通过channel（mailbox）传入来改变的。在这个整整源码占了我20M SSD的源码里面，pulsar实现了你能想得到的一切，json rpc，websocket support，wsgi，socket server，process control等等，连特么route，orm，db_client，fake_redis都带上了……从无到有一个框架全给你搞定，长连接，实时计算，延迟后端计算，任务队列，4层以上多协议RPC，分分钟……
	
	”
	
	**警告**： 千万不要相信这个安利。Pulsar的文档写得....好吧，不黑，基本上是自动生成的。所以用Pulsar是要读它的代码和单元测试的——表示代码和测试都并不是我喜欢的抽象方式——mixin来mixin去的，但是作者还是非常nice的。celebi的router实现是用我的pwsgi实现的，pwsgi其实就是把一个wsgi包了一层，可以用pulsar来跑。这个东西会合并到pulsar的下一个版本里。大概两三个月后上线什么的。
	
	来说一下具体的例子
	
	actor模型，看代码pulsar/examples/snippets/actor1.py
	multi appliction可以看pulsar/tests/app/multi_app
	
	application的实现可以看pulsar的wsgiserver实现，或者celebi里的postgresArbiter的实现
	
	哦，还有一个imply
	
	如果我有n个服务，它们是用uwsgi其的，每个服务只有一个对称IO，它们之间用rpc通信。异步
	
	那么这是一个什么模型？这本质上是一个actor模型。
	
	
## 其实这里就写完了，下面的太长不要看，我写文档容易写偏，写着写着就水成paper了
	
	
	
	


## The problem is actually a Distributed System problem

**TL;DR：Microservices Architecture is Bullshit**

-----



Micro-Services was introducted by Peter Rodgers and Juval Löwy in 2005 [1,2,3]. The philosophy of it essentially equals to the Unix philosophy of "Do one thing and do it well". [4][5][6]:


* The services are small - fine-grained to perform a single function.

* The organization culture should embrace automation of testing and deployment. This eases the burden on management and operations and allows for different development teams to work on independently deployable units of code.[7]

* The culture and design principles should embrace failure and faults, similar to anti-fragile systems.

* Each service is elastic, resilient, composable, minimal, and complete.[6]

And as Leslie Lamport's defination of distributed which in given in 2000, the micro-services architecture should always be a distributed system. In the viewpoint, a network of interconnected computers is a distributed system, and a single computer can be also be viewed as a distributed system in which the central control unit, the menory unit, and the input-output channels are sparate process. *A system is distributed is the message transmision delay is not negligible compared to the time between events in a single process*.[9]

In the fact, Addressing to the granularity of services, the realworld usecase of microservices architecture is usually either a distributed system or based on a distributed such as some raft or paxos implementation like etcd[9], consul[10] and zookeeper[11].

Thus the "Unix Philosophy" of "Do one thing and do it well" is actually talking about the Philosophy of about the Distributed System archiecture", which is also descriping how "micro-services architecture" works.

## Communication Sequential Processes

**TL;DR: Two Turing Award laureates thinks CSP (Actor model) is good for distributed system, and it's really so fucking good**

-----


There is two kind of languages for modeling a complex distributed system: **Causal (or block-oriented) languages** and **none-causal (or object-oriented) language**.[12]

CPS is a typical None-Causal Language, which a modeling language which is abbreviation of Communication Sequential Processes, created by C.A.R Hoare, and still keeping update in nowadays(2015)[14]. It defined a process as this:

Let $x$ be an event and let $P$ be a process, Then $(x \rightarrow P)$ (proounced “$x$ then $p$”)

In 1983, when Lamport talk about CPS, he said: "It's a fine language, or more precisely, a fine set of communication constructs. Hoare deserved his Turing award...,We really know that CPS is the right way of doing things... "[14]


## Functional Reactive Programming

**TR;DR: We are doing so damn same things**


## Why Symmetric is importent
**TR;DR:**


## Reference


[1] Rodgers, Peter. "Service-Oriented Development on NetKernel- Patterns, Processes & Products to Reduce System Complexity Web Services Edge 2005 East: CS-3". CloudComputingExpo 2005. SYS-CON TV. Retrieved 3 July 2017.

[2] Löwy, Juval (October 2007). "Every Class a WCF Service". Channel9, ARCast.TV.

[3] Löwy, Juval (2007). Programming WCF Services 1st Edition. pp. 543–553.

[4] Lucas Krause. Microservices: Patterns and Applications. ASIN B00VJ3NP4A.

[5]Lucas Krause. "Philosophy of Microservices?".

[6]Jim Bugwadia. "Microservices: Five Architectural Constraints".

[7] Li, Richard. "Microservices Essentials for Executives: The Key to High Velocity Software 
Development". Datawire. Datawire, Inc. Retrieved 21 October 2016.


[8] Leslie Lamport, Times ,Clocks, and the Ordering of Events in a Distributed System


[9] A distributed, reliable key-value store for the most critical data of a distributed system. https://coreos.com/etcd/

[10] Service Discovery and Configuration Made Easy https://www.consul.io/

[11] Apache ZooKeeper is an effort to develop and maintain an open-source server which enables highly reliable distributed coordination. https://zookeeper.apache.org/

[12] [Andrew Kennedy. Programming Languages and Dimensions. PhdD thesis, University of Cambridge, Computer Laboratory, April 1996. Published as Technical Port No. 391.](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-391.pdf)

[13] C.A.R Hoare, Communicatiing Sequential Process, May 18, 2015.

[14] Leslie Lamport, 1983 Invited Address, Solved Problems, Unsolved Problems and Non-problems in Concurrency.


