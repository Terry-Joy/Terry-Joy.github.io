---
title: 「LibreOJ Round #6」花火
tags:
- 算法竞赛
  - 线段树
    - 扫描线
---


## 「LibreOJ Round #6」花火
题意：$n\leq300000$的一个排列，每次能交换相邻两个数，并且有一次机会交换不相邻的两个数，可以不用这个机会。问使这个排列升序最少操作几次。

思路：
考虑没有不相邻的话，显然就是逆序对数，对于第二种操作，我们可以把$(i, h_i)$看成平面上的一个点，那么我们只有交换$i, j, i < j且h_i > h_j$的点，才会减少答案，我们把交换的两个点看成一个矩阵，贡献是$sum - 矩阵内点数加上 * 2 -1 + 1$，这个应该不难看出。此外，我们发现如果先做操作一，实质上对于任意操作二的贡献是不变的，不难理解，一次交换后把某点变到矩阵中的话，一定是多付出一次操作次数来换取一个矩阵内部点的增加，最后贡献不变。所以我们先考虑操作二再考虑操作一本质是一样的。

现在问题变成怎么选择一个数对，使得矩阵中的点数最多，暴力枚举点对+逆序对是$O(n^3logn)$的，显然无法通过本题，我们考虑其实对于一个矩阵来说，他左上角和右下角肯定是越往左上和越往右下越优秀，所以左上角和右下角保留的点一定是满足决策单调性的，分治套个数据结构可以做到$O(nlog^2n)$。

我们考虑另一种更优的方法，**现在我们想知道$O(n^2)$个矩形，一个矩形最多覆盖多少个点，扫描线有个常见问题是，多个矩形，问哪个点被覆盖最多**，我们希望矩阵覆盖更多的点，对于每个点，考虑他对矩阵的贡献，一个点$(i, h_i)$,设$l$为最小的$h_l > h_i$的数，$r$为最大的$h_r < h_i$的数，那么他对左端点在$[l, i - 1]$和右端点在$[i + 1, r]$的$(i, j)$交换数对有贡献，我们可以把$(i, j)$数对再看成另一个二维平面上的点，那么就变成多个矩形，问哪个点覆盖最多的问题，直接扫描线+线段树即可解决，注意一下进出边顺序即可，时间复杂度$O(nlogn)$

```cpp
#include <bits/stdc++.h>
#define eb emplace_back
#define ls p << 1
#define rs p << 1 | 1
#define lson p << 1, l, mid
#define rson p << 1 | 1, mid + 1, r
using namespace std;
using ll = long long;
const int maxn = 3e5 + 5;
struct Line {
    int l, r, op, y;
    Line(int m_l, int m_r, int m_op, int m_y) : l(m_l), r(m_r), op(m_op), y(m_y) { }
    bool operator<(const Line &x) const {
        if (y == x.y)
            return op > x.op;

        return y < x.y;
    }
};
struct BIT {
#define lowb(x) (x&(-x))
    vector<int> c;
    int N;
    void init(int n) {
        N = n;
        c.resize(n + 1);
    }
    void add(int x, int val) {
        for (int i = x; i <= N; i += lowb(i)) {
            c[i] += val;
        }
    }
    int ask(int x) {
        int ans = 0;

        for (int i = x; i; i -= lowb(i)) {
            ans += c[i];
        }

        return ans;
    }
} bit;
struct SegmentTree {
    int mx[maxn << 2], add[maxn << 2];
    void pushUp(int p) {
        mx[p] = max(mx[ls], mx[rs]);
    }
    void pushDown(int p) {
        mx[ls] += add[p];
        mx[rs] += add[p];
        add[ls] += add[p];
        add[rs] += add[p];
        add[p] = 0;
    }
    void update(int p, int l, int r, int L, int R, int val) {
        if (L <= l && r <= R) {
            mx[p] += val;
            add[p] += val;
            return;
        }

        if (add[p])
            pushDown(p);

        int mid = l + r >> 1;

        if (L <= mid)
            update(lson, L, R, val);

        if (R > mid)
            update(rson, L, R, val);

        pushUp(p);
    }
} tr;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n;
    cin >> n;
    vector<int> lmx(n + 1), rmn(n + 1), h(n + 1);

    for (int i = 1; i <= n; ++i) {
        cin >> h[i];
    }

    ll ans = 0;
    bit.init(n);

    for (int i = n; i; --i) {
        ans += bit.ask(h[i]);
        bit.add(h[i], 1);
    }

    lmx[1] = h[1];

    for (int i = 2; i <= n; ++i) {
        lmx[i] = max(lmx[i - 1], h[i]);
    }

    rmn[n] = h[n];

    for (int i = n - 1; i; --i) {
        rmn[i] = min(rmn[i + 1], h[i]);
    }

    vector<Line> line;

    for (int i = 1; i <= n; ++i) {
        int l = lower_bound(lmx.begin() + 1, lmx.end(), h[i]) - lmx.begin();
        int r = upper_bound(rmn.begin() + 1, rmn.end(), h[i]) - rmn.begin() - 1;

        if (l >= r || r <= i || l >= i)
            continue;

        //cout << l << " " << i - 1 << " " << r << endl;
        line.eb(l, i - 1, 1, i + 1);
        line.eb(l, i - 1, -1, r);
    }

    sort(line.begin(), line.end());
    int mx = 0;

    for (auto [l, r, op, y] : line) {
        mx = max(tr.mx[1], mx);
        tr.update(1, 1, n, l, r, op);
    }

    cout << ans - 2 * mx;
    return 0;
}
```
