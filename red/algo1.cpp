#include <stdio.h>
#include <stdlib.h>
#include <vector>

struct pair {
    size_t v;
    size_t u;
};

int main(int argc, char const* argv[]) {
    // read input data from stdin
    size_t n = 0;
    scanf("%zu", &n);
    // IDEA: we can pack matrix in ints
    // IDEA: we do not need whole matrix
    bool* data = (bool*)malloc(n * n * sizeof(bool));
    std::vector<pair> povezave;
    povezave.reserve(n * n / 2);
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            int t;
            scanf("%d", &t);
            data[i * n + j] = t;
            if (i <= j) povezave.emplace_back(pair {i, j});
        }
    }

    // prepare for output
    std::vector<pair> result;
    result.reserve(n * n / 2);

    for (auto povezava1 : povezave) {
        for (auto povezava2 : povezave) {
            // za vsako povezavo v rezultatu mora to veljati
            if (!data[povezava1.u * n + povezava2.u] && !data[povezava1.u * n + povezava2.v] && !data[povezava1.v * n + povezava2.u] && !data[povezava1.v * n + povezava2.v]) {
                //result.push_back();
            }
        }
    }

    // output result
    printf("%zu\n", result.size());
    for (pair car : result) {
        printf("%zu %zu\n", car.v, car.u);
    }

    free(data);
    return 0;
}
