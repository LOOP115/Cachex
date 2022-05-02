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
* 我方和敌方的棋子数 ✔
* 我方和敌方当前连续棋子的最大长度 ✔
* 我方和敌方当前距离胜利还需要几步 ✔
  * 寻找最优起始点 ✔
    * 优先选择存在更多棋子的同行（蓝）或同列（红）✔
    * 若没有棋子在边界，选择距离所有棋子最近的边界点 ✔
  * A* Search ✔
    * 搜索过程中可能已经到达边界，记录最短步数 ✔
    * 搜索过程中可能发现新的起点，可能缩短步数 ✔
    * Heuristic function: Manhattan distance - 现存棋子数 + x(红)/y(蓝)坐标值 ✔

> 生成所有可能的 actions
* 第一回合利用 symmetry ❓
* 第一回合不要下特别好的棋防止被偷 ❓
* 第二回合考虑 STEAL ❓

> 实现 MiniMax ✔
* α-β Pruning ✔
* 评估当前局面下是否值得这步棋 ✔
  * 如果我方下这步棋，我方会有多少收益 ✔
  * 如果对方下这步棋，我方会有多少收益 ✔
  * 如果我方下这步棋我方会赢，我方直接下这步棋 ✔
  * 如果对方下这步棋我方会输，我方下这步棋拦截 ✔
* 递归前先评估所有可以下的位置，排序后对评分前 50% 的位置进行 MiniMax ✔
* 每轮博弈都进行预先筛选 ❓

> 构造 Opponent
* Random ✔ ✌
* Greedy: Select most immediately promising action ✔ ✌
* Simple evaluation function ✔
* Same strategy ✔
* Human ✔ ✌

> 记录对战棋局, 生成训练数据

> Machine Learning

> 完成 Report

