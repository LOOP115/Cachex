# Cachex

* [Cachex Rules](spec/cachex_rule.pdf)

## Part A

[**Searching**](simple_search)

* [Specification](spec/spec_a.pdf)
* [Report](report/report_a.pdf)

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
* [Report](report/report_b.pdf)

> Setup on Unix Machine
* <code> Host Name: dimefox.eng.unimelb.edu.au </code>
* <code> enable-python3 </code>
* <code> pcsp [files] [username]@username>@dimefox.eng.unimelb.edu.au:[remote directory path] </code>
* <code> python -m referee [board size] [red player] [blue player] -c -s [space MB] -t [time sec] </code>

### Progress Check List

> 校验 Rules
* Swap Rule (STEAL) ✔
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

> 生成所有可能的 Actions
* 第一回合利用 symmetry
* 第一回合不要下特别好的棋防止被偷 ✔
* 第二回合考虑 STEAL，如果我方偷棋后 Utility 更高则选择 STEAL ✔

> 实现 MiniMax
* α-β Pruning ✔
* 评估当前局面下是否值得这步棋 ✔
  * 如果我方下这步棋，我方会有多少收益 ✔
  * 如果对方下这步棋，我方会有多少收益 ✔
  * 如果我方下这步棋我方会赢，我方直接下这步棋 ✔
  * 如果对方下这步棋我方会输，我方下这步棋拦截 ✔
* 递归前先评估所有可以下的位置，排序后对评分前 50% 的位置进行 MiniMax ✔
* 每轮博弈都进行预先筛选 ❌

> 构造 Opponent
* Random ✔ ✌
* Greedy: Select most immediately promising action ✔ ✌
* Simple evaluation function ✔
* Same strategy ✔
* Human ✔ ✌

> Dimefox 测试
* 设置 Timer ✔
* Memory ✔

> 完成 Report
* Describe your approach: How does your game-playing program select actions throughout the game? ✔
  * What search algorithm have you chosen, and why? ✔
  * Have you made any modifications to an existing algorithm? ✔
  * What are the features of your evaluation function, and what are their strategic motivations? ✔
  * If you have applied machine learning, how does this fit into your overall approach? ❌
  * What learning methodology have you followed, and why? ❌
  * Note that it is not essential to use machine learning to design a strong player. ✔
* Performance evaluation: How effective is your game-playing program? ✔
  * How have you judged your program’s performance? ✔
  * Have you compared multiple programs based on different approaches, 
    and, if so, how have you selected which is the most effective? ✔
* Other aspects: Are there any other important creative or technical aspects of your work? ✔
  * algorithmic optimisations ✔
  * specialised data structures ✔
  * any other significant efficiency optimisations ✔
  * alternative or enhanced algorithms beyond those discussed in class ✔
  * any other significant ideas you have incorporated from your independent research ✔
* Supporting work: Have you completed any other work to assist you 
                   in the process of developing your game-playing program? ✔

