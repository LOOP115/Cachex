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

> 跑通下棋对战 ✔

> 校验 Rules
* Swap Rule (STEAL)  后期实现，胜率 > 50% 的初始位置可以进行替换
* Starting with a hex in the center is illegal ✔
* Capture ✔
* Draw （交由 Referee 裁决）✔
    * 7 same game configurations
    * 343 turns

> 实现 MiniMax

> 实现 α-β Pruning

> 构造 Opponent
* Random ✔
* Basic Utility Function
* Same Strategy as Player

> 记录对战棋局, 生成训练数据

> 优化 Evaluation Function

> 完成 Report

