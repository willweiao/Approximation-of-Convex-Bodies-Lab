这段脚本用 MATLAB + YALMIP + SeDuMi 实现了对**二维凸多边形**的 **John 椭球（最大体积内接椭球）** 的求解与可视化。

下面是逐步解释其核心原理和实现方式：

---

## 🧠 数学原理简述（John’s Theorem in 2D）

对于一个对称凸体 $C \subset \mathbb{R}^2$，其内接最大体积椭球（John ellipsoid）具有如下形式：

$$
E = \left\{ x \in \mathbb{R}^2 \ \middle| \ (x - a)^T P (x - a) \le 1 \right\}
$$

* $a$：椭球中心（向量）
* $P$：正定矩阵（形状控制）

**目标**：最大化椭球体积
由于二维椭球体积为 $\propto 1/\sqrt{\det P}$，所以最大体积 ⇔ 最小化 $\log\det(P)$

---

## 🧩 实现步骤详解（分段解读）

### ### Step 1：生成点集 & 求凸包

```matlab
points = rand(n_points, 2);
hull_idx = convhull(points(:,1), points(:,2));
```

* 在平面中生成随机点；
* 用 `convhull` 找出最小凸包点集，定义凸多边形 $C$。

---

### ### Step 2：定义椭球变量

```matlab
a = sdpvar(2,1);     % 椭球中心
P = sdpvar(2,2);     % 对称正定矩阵，定义椭球形状
```

* $a$ 是椭球中心；
* $P \succ 0$ 定义了椭球的方向和伸展程度。

---

### ### Step 3：约束构造（关键！）

```matlab
C{i} = [1, (v - a)'; (v - a), P] >= 0;
```

这表示：

> 对于凸体上的每个点 $v_i \in \partial C$，保证：

$$
(x - a)^T P (x - a) \le 1 \quad \text{（即椭球包含该点）}
$$

但为了使这个约束被 **SeDuMi 识别为 SDP**，使用了\*\*等价的线性矩阵不等式（LMI）\*\*形式：

$$
\begin{bmatrix}
1 & (v - a)^T \\
(v - a) & P
\end{bmatrix} \succeq 0
$$

这利用了 Schur 补性质，是标准的椭球包含点的 SDP 写法。

---

### ### Step 4：目标函数（最大体积）

```matlab
Objective = -logdet(P);
```

因为椭球体积 $\propto 1/\sqrt{\det(P)}$，所以最大体积 ⇔ 最小 $-\log\det(P)$，这使目标函数是 concave 的，适合 SDP 求解。

---

### ### Step 5：求解 SDP 问题

```matlab
sol = optimize([C{:}], Objective, opts);
```

* 使用 SeDuMi 或 SDPT3 对上述约束与目标进行优化；
* 解得的 $a, P$ 即为 John 椭球的参数。

---

### ### Step 6–7：提取解并绘图

```matlab
[U,D] = eig(inv(P_val));  % 将 P⁻¹ 对角化
ellip = U * sqrt(D) * circle + a_val;  % 椭圆变换
```

* 使用特征值分解 $P^{-1} = U D U^T$ 将单位圆映射为椭球；
* 最后绘出叠加在凸体上的红色椭球图形。

---

## ✅ 总结：这个脚本实现了什么？

| 项目   | 内容                              |
| ---- | ------------------------------- |
| 输入   | 一组二维点集（或凸多边形）                   |
| 输出   | 该凸体内的最大内接椭球                     |
| 优化形式 | 半正定规划（SDP）                      |
| 数学基础 | John’s Theorem, Schur 补, 椭球体积优化 |
| 求解工具 | YALMIP + SeDuMi/SDPT3           |
| 可视化  | 椭球轮廓叠加在凸体图上                     |

---

是否需要我也为这个方法写一个 3D 版本？或者帮你封装成函数形式方便调用？
