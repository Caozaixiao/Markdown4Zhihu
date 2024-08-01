# 第1章 创建第一个Unreal C++游戏

本文为《Unreal Engine 5 Game Development with C++ Scripting》第1章 粗翻及学习笔记，原书请见https://www.oreilly.com/library/view/unreal-engine-5/9781804613931/，Github 源码请见https://github.com/PacktPublishing/Unreal-Engine-5-Game-Development-with-C-Scripting，有能力请支持正版。

[章节列表]()

虚幻引擎（UE）是Epic开发的最受欢迎的3D计算机图形游戏引擎之一，提供一套全面的工具和功能，以开发高质量、身临其境的游戏三维模拟。该引擎提供了直观的可视化脚本系统Blueprint和强大的C++适用于所有技能水平的开发人员的编程框架。这本书提供了一个简明的介绍C++编程，并演示了如何在UE中编写用于游戏开发的C++脚本。

在本章中，您将学习从头开始创建虚幻C++项目的基本技能或者将现有的虚幻蓝图项目转换为虚幻C++项目，这是在游戏开发中取得进步的基本技能。通过掌握这个过程，您将获得将你的游戏开发能力提升到一个新的水平所必需的基础。

本章将涵盖以下主题：

* 理解虚幻中的C++脚本
* 从样板创建您的C++射击程序项目
* 将已有蓝图项目转换为C++项目

# 技术要求
作为本书的读者，希望您具备常见的计算机操作技能。您还应该具备UE5编辑器的基本知识和经验，以及一些蓝图脚本编写的技能。

要继续学习本章，您应该已安装 Epic Games Hub 和 5.03 或更高版本的计算机上的引擎编辑器。如果您还没有这样做，请前往Epic官方网站（https://www.unrealengine.com/en-US） 注册账号并下载Epic游戏游戏启动器。

所需的最低开发环境如下： 

* 操作系统：Windows 10 
* 处理器：Intel 第 7 代或同等产品 
* 内存：16 GB RAM 
* GPU：GTX 1080（或 AMD 同等产品） 
* DirectX：DX12 
* 存储空间：25 GB 可用空间 
* 附注： 推荐8 GB显存

官方系统要求可以在这里找到：[https://docs.unrealengine.com/5.0/en-US/hardware-and-software-specifications-for-unreal-engine/](https://docs.unrealengine.com/5.0/en-US/hardware-and-software-specifications-for-unreal-engine/)。为了节省UE5编辑器中的游戏编辑时间，建议使用带有i9（或AMD的计算机等效）CPU、64 GB RAM 和 GeForce RTX 3060 显卡。

## 1.1 理解Unreal引擎中的C++脚本
**C++和蓝图的区别**

C++和Blueprint都是可以完成相同任务的脚本语言，但在某些情况下，其中一种可能比另一种更适合。它们之间的主要区别在于，C++是一种允许您编写通用的、基于文本的代码的编程语言，而Blueprint是一种用于UE的可视化脚本系统。

对于UE项目，游戏工作室通常同时使用C++和Blueprint来开发商业级游戏。

C++通常用于高级技术、复杂算法和大规模逻辑代码。如果你能用C++编写脚本，你将有更多的机会在专业团队中工作。

使用C++最重要的优点之一是性能。C++允许您编写低级操作代码。它还提供了对Blueprint无法访问的核心系统的控制。

此外，最终的C++代码最终将被优化并编译为机器友好的二进制本地代码。另一方面，蓝图脚本由中间层解释和执行，这意味着更多的执行时间。

C++代码和文件可以基于整个项目的机制进行良好的组织。在全局范围内很容易搜索、定位和访问代码块以进行编辑、维护和故障排除。同时，它也是更容易阅读和理解一大块实现复杂算法和逻辑的代码。

另一方面，蓝图是一个上下文敏感的脚本环境。蓝图图为相对独立。当一个图需要解决复杂的逻辑时，节点和连接线条形成了难以理解和维护的凌乱意大利面。

C++也有一些缺点。一个例子是，它可能会导致严重错误，从而导致整个系统崩溃。这通常是由开发人员的错误引起的。由于蓝图是一个受保护的层，所以它更安全，因此系统崩溃的可能性更小。总之，在C++和Blueprint之间的选择应该基于特定的开发需求和条件，并考虑每种方法的优缺点。

**什么时候使用C++**

C++和Blueprint都可以毫无问题地处理游戏开发过程。没有确切的规则来规定何时使用C++或蓝图。这主要取决于你的经验和不同游戏的实际需求。你根据自己对两个系统的熟悉程度去决定如何使用。

在你开始研究某件事之前，你可以问自己这样一个问题：“在哪里使用C++有意义，在哪里使用蓝图有意义？”我们建议你的答案基于以下方面和权衡：

* 性能
* 逻辑和算法复杂性
* 系统核心功能的可访问性
* 开发人员的经验

如果你想要更高的性能，处理高级的游戏逻辑和系统流程，并且你有能力编码和解决复杂的问题，你应该选择C++。

**C++编程和C++脚本的区别**

您可能会对C++编程和C++脚本之间的区别感到困惑。我们想澄清这两个术语的含义。

C++编程是指使用C++编程语言编写用于任何目的的代码；它不一定只针对UE项目。在本书中，C++脚本是C++的一种特定方言UE支持的编程语言。它利用了C++语法的强大功能与UE的应用程序编程接口（API）配合使用，允许开发人员创建和为游戏和开发环境的上下文扩展引擎的功能，例如作为对象、图形、音频和网络通信。

现在，我们对C++有了基本的了解，并了解了为什么以及何时将C++用于虚幻游戏开发，让我们通过创建一个示例项目来深入了解C++脚本。

## 1.2 从模板创建C++射击项目
现在，是时候自己动手做UE5 C++项目了。我们将根据第一人称模板从头开始创建一个新的C++项目。

第一人称模板是UE附带的默认游戏模板之一。如果要创建新项目，可以从“虚幻项目浏览器”窗口中选择此模板。我们的新MyShooter游戏将从模板游戏中获得所有功能，我们不必做任何额外的工作。

要开始使用C++脚本，我们首先需要安装一个IDE。在本书中，我们将使用MS Visual Studio 2022作为示例。

**安装Visual Studio 2022**

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/3Ei3rfOg4PfszwV7lYKM9vG3vtNZQHUfz0HM3_keRyE.png)

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/6q2J_Mfj6vM22--tVa4t7tO9tA5crdTrlYjYs8cUcWI.png)



此外，请留意“安装详细信息”面板上属于“使用C++进行桌面开发”组的以下选项，并确保选中以下选项：

* C++ profiling tools
* C++ AddressSanitizer 
* Windows 10 SDK 
* IntelliCode 
* IDE support for Unreal Engine

接下来我们需要做的是确认我们已经安装了引擎源代码和UE5编辑器。我们之所以需要这样做，是因为当我们生成一个新项目时，引擎源代码可以集成到新项目中；在某些情况下，我们可能需要根据游戏的特定需求修改或自定义引擎。确保您的UE安装了源代码。

**确保您的UE已安装源代码**

在启动UE5编辑器之前，我们首先需要检查编辑器是否安装了Engine Source。通过进行此检查，我们确保UE5源代码与我们将要创建的C++项目集成在一起。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/QGNLbXZsDhxZLMt6gXjMHSdQQpdqw-l5hjL3Gae0mqc.png)

1. 单击向下箭头按钮，然后从下拉菜单中选择“选项”。
2. 确保已选中Engine Source选项。
3. 按下“应用”按钮：

UE是一个正在进行的开发产品，存在漏洞和缺陷，可能需要由用户修复。此外，专业开发人员有时会修改引擎源代码以适应他们的特定需求。一个例子是，当我们面临几何实例化（或实例化渲染）仅在游戏的开发构建中工作而不在发布构建中工作的问题时，我们的工程师随后修改了引擎的源代码，从而解决了这个问题。

**通过Epic Games Launcher启动UE5编辑器**

启动UE5编辑器非常简单。您只需单击5.03引擎上的Launch按钮即可启动编辑器（见图1.5）。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/r2gtuUuTPgO8xCMUuTQpftF8gKCec4sbNnX4MB3eK1c.png)

**创建MyShooter C++项目**

要创建项目，请执行以下步骤（请参见图1.6以供参考）：

1. 在“虚幻项目浏览器”窗口中，选择左侧的“游戏”选项卡。
2. 选择“第一人称”模板。
3. 选择C++按钮。
4. 选择项目位置（例如C:\\UEProjects），然后在“项目名称”字段中键入MyShooter。
5. 单击“创建”按钮。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/CYttpO9oAcurrA52NVYGc3UbnTXfFu9zhEgklDp2cvg.png)

创建的游戏项目还包括入门内容，其中包含可用于制作游戏原型的资产和资源。

引擎将进行一些初始化工作，然后在准备就绪时打开编辑器。如果您查看编辑器窗口左下角的项目树面板的MyShooter选项卡，你应该在与Content节点相同的层上看到C++类节点（见图1.7）。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/U4P8qjJfOHS7sT1SImObS_whjPLP2HGCnu8vn6pCxI0.png)

**将VS与UE5关联为默认源代码编辑器**

我们创建了C++项目，游戏的所有C++源代码都已经生成。要直接在UE5编辑器中打开源文件，我们需要将VS关联为引擎编辑器的默认IDE。

在UE5编辑器的主菜单上，选择**编辑-编辑器首选项** `Edit | Editor Preferences`以打开首选项窗口，然后在左侧面板上找到**常规|源代码**`General | Source Code`项目，最后从源代码编辑器下拉列表中选择Visual Studio 2022（见图1.8）。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/eO_37ur_MeVzHfLs5M4styGs_6h6HPzM2qDOiHymDjc.png)

**在VS中打开C++源代码（可选）**

如果您想在VS中打开并查看C++源代码，您可以在项目中找到源代码文件（例如，C++/MyShooter/MyShooterCharacter.cpp），然后双击它（见图1.9）。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/EPNIfssb_klr5UJ44LqX_jDPyn3gZi4p8DLT7FnEW8w.png)

系统将自动启动VS，VS编辑器将打开MyShooterCharacter.cpp文件（见图1.10）。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/GBvF6clYdK2Ift1D0OyFC6VMUZUs1Yh5oovpqsy67iw.png)

回到虚幻编辑器中，单击运行按钮开始游戏。在战场上玩游戏时，你可以控制你的角色，移动他们，并拿起他们面前的枪（见图1.11）。

我们已经学会了如何从头开始创建UE C++项目。然而，如果我们已经有了一个蓝图项目，并想将其转换为C++项目，该怎么办？UE允许开发人员通过向项目中添加一个新的C++类来实现这一点。让我们练习转换MyBPShooter蓝图项目。

## 1.3 将已有蓝图项目转换为C++项目
UE提供了一种将现有蓝图项目转换为C++项目的非常简单的方法。您所需要做的就是向项目中添加一个C++类，然后让UE负责转换并添加所需的项目文件：

1.首先，您必须在C:\\UEProjects下创建一个蓝图项目MyBPShooter（您可以选择不同的路径来创建新项目）。使用创建MyShooter C++项目部分中介绍的相同步骤，但选择BLUEPRINT而不是C++来创建MyBPShooter项目。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/kpW_B-fu0H03HdinCHKXmZn3maq2aO5YuWr_czTLAi8.png)

2.第二步，在UE5中打开新项目。注意项目树；它在这个阶段没有C++类节点。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/GmVkcJ1UFpr3FOOIvUVYZ4FTKRw5Rnd8GZAuV8PI0wM.png)

3.从编辑器的主菜单中选择Tools | New C++Class，然后在Add C++Class窗口（见图1.14）中，选择Character作为基类（一个包含公共属性的类以及由其派生类共享的方法）来创建MyShooterCharacter类。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/okN6F9Mkx_OyUhgxF9B829t8tS3PaszdN352kCPx-vQ.png)

单击“下一步”>按钮后，它将导航到“NAME YOUR NEW CHARACTER”窗口。

4.在“命名新角色”屏幕上，在“名称”字段中键入MyBPShooterCharacter。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/cHQ4CT3XG2UCrj_oyW_88LP4m56YXnbEAzd9oSPICbU.png)

请注意放置头文件和源文件的路径。它们看起来与MyShooter项目不同，因为C++节点还没有创建。现在别担心。转换工作完成后，系统将自动将文件移动到正确的位置。

5.单击“创建类”按钮后，您将看到一个进度条。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/1SgxUs-wfNtTKSUC9bzVeQRsXHtWOgLoidnxpdbaH_0.png)

等待弹出消息，该消息表示已添加C++类。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/PI_7tsQl_M_WLd31FtRtcvwBnNue5W1XR2zUuR00diw.png)

6.单击“确定”按钮。现在，您将看到消息对话框，询问您是否要编辑代码（见图1.18）。这里选No。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/N8X9Mt9Bd7ClLCvD13yL32hRkZ_G4COznc0-YsVZbAA.png)

7.关闭UE编辑器，然后重新打开**MyBPShooter**。当您看到一个对话框询问是否要重新生成项目时，请在此处回答“是”。

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/1TqIcC_1wr5esLwjeSsNikZKzM2WRB0rOTZ70t-J61M.png)

完成后，您将在项目树上找到新的C++类节点，并且MyShooterCharacter类已放置在MyBPShooter文件夹中：

![image](https://raw.githubusercontent.com/Caozaixiao/Markdown4Zhihu/master/Data/第1章 创建第一个Unreal C++游戏/o-feGY8ey0eaW6mBw-ZOSB4zSDQlw9zoCJGdeo5mgcM.png)

您可能已经注意到，与MyShooter项目相比，其他一些文件（如MyBPShooterGameMode）丢失了。这是因为蓝图版本已经存在，所以相应的C++版本不是自动生成的。只有在必要时，您才能选择手动将这些蓝图转换为C++类；否则，你只需要保留蓝图。

## 总结
在本章中，我们介绍了C++及其在职业游戏开发中的优势。然后，您练习创建新的MyShooter C++项目并转换MyBPShooter蓝图项目到C++项目。此外，您还使用VS和C++解决方案文件。

在下一章中，我们将首先介绍IDE用户界面的每个部分。然后，你会创建一个C++项目并练习编写一些简单的C++代码。一些代码编辑技巧将是在编辑代码时引入。

