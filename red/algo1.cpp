#include <stdio.h>
#include <stdlib.h>
#include <vector>

struct pair {
    size_t v;
    size_t u;
};

size_t n;
bool* data;
std::vector<pair> povezave;
std::vector<pair> najboljse;
std::vector<pair> trenutno;

bool jeValid(size_t x, size_t y) {
    for (auto [a, b] : trenutno) {
        if (data[x * n + a] || data[x * n + b] || data[y * n + a] || data[y * n + b]) {
            return false;
        }
    }
    return true;
}

void obhod(size_t idx) {
    if (trenutno.size() > najboljse.size()) {
        najboljse = trenutno;
    }

    if (trenutno.size() + povezave.size() - idx <= najboljse.size()) {
        return;
    }

    for (int i = idx; i < povezave.size(); i++) {
        auto [x, y] = povezave[i];
        if (jeValid(x, y)) {
            trenutno.emplace_back(pair {x, y});
            obhod(i + 1);
            trenutno.pop_back();
        }
    }
}

int main(int argc, char const* argv[]) {
    // read input data from stdin
    scanf("%zu", &n);
    // IDEA: we can pack matrix in ints
    // IDEA: we do not need whole matrix
    data = (bool*)malloc(n * n * sizeof(bool));
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            int t;
            scanf("%d", &t);
            data[i * n + j] = t;
        }
    }

    povezave.reserve(n * (n - 1) / 2);

    for (size_t i = 0; i < n; i++) {
        for (size_t j = i + 1; j < n; j++) {
            if (data[i * n + j]) {
                povezave.emplace_back(pair {i, j});
            }
        }
    }
    // IDEA: choose strategy by graph type
    obhod(0);

    printf("%zu\n", najboljse.size());
    for (auto [x, y] : najboljse)
        printf("%zu %zu\n", x + 1, y + 1);

    free(data);
    return 0;
}