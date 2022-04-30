# Cachex

* [Cachex Rules](spec/cachex_rule.pdf)

## Part A

[**Searching**](simple_search)

* [Specification](spec/spec_a.pdf)
* [Report](simple_search/report/report.pdf)

####

> Setup on Unix Machine
* <code>Host Name: dimefox.eng.unimelb.edu.au</code>
* <code>enable-python3</code>
* <code>python -m search inputs/input.json</code>

####

> Reference
* https://stackoverflow.com/questions/5084801/manhattan-distance-between-tiles-in-a-hexagonal-grid
* https://www.redblobgames.com/pathfinding/a-star/implementation.html

## Part B

**Playing the Game**

* [Specification](spec/spec_b.pdf)

### Progress Check List

> 校验 Rules
* Swap Rule (STEAL)  后期实现，胜率 > 50% 的初始位置可以进行替换 ❓
* Starting with a hex in the center is illegal ✔
* Capture ✔
* Draw （交由 Referee 裁决）✔
    * 7 same game configurations
    * 343 turns

> Evaluation Function 要素
* 我方和敌方的棋子数 ❓
* 我方和敌方当前连续棋子的最大长度 ✔
* 我方和敌方当前距离胜利还需要几步 ✔
  * 寻找最优起始点 ✔
    * 优先选择存在更多棋子的同行（蓝）或同列（红）✔
    * 若没有棋子在边界，选择距离所有棋子最近的边界点 ✔
  * A* Search ✔
    * Heuristic function: Manhattan distance - 现存棋子数 ✔
    * 搜索过程中可能已经到达边界，记录最短步数 ✔

> 生成所有可能的 actions
* 第一回合利用 symmetry ❓
* 第一回合不要下特别好的棋防止被偷 ❓
* 第二回合考虑 STEAL

> 实现 MiniMax ✔

> 实现 α-β Pruning

> 构造 Opponent
* Human ✔
* Random ✔
* Basic Utility Function
* Same Strategy as Player

> 记录对战棋局, 生成训练数据

> 机器学习，优化模型

> 完成 Report

