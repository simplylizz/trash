#include <vector>
#include <unordered_map>
#include <iostream>
#include <limits>


int solution(int k, std::vector<int> & v) {
    std::unordered_map<int, int> vmap (v.size());

    // std::cout << std::endl;

    for (auto const & it : v) {
        // std::cout << it << std::endl;
        ++vmap[it];
    }

    int pairs = 0;
    int compl_counter;
    long index;

    // std::cout << "########" << std::endl;
    // for (auto const & it : vmap) {
    //     std::cout << it.first << ": " << it.second << std::endl;
    // }

    // return -1;

    for (auto const & it : vmap) {
        // std::cout << "########" << std::endl;
        // std::cout << it.first << ": " << it.second << std::endl;
        index = k - (long)it.first;
        if (!(index > std::numeric_limits<int>::max() || index < std::numeric_limits<int>::lowest())) {
            if (vmap.count(k - it.first) != 0) {
                compl_counter = vmap[k - it.first];
                if (compl_counter > 0) {
                    // std::cout << "found pair for " << it.first << ": " << k - it.first << " inc pairs " << it.second << " * " <<  compl_counter << " = " << it.second * compl_counter << std::endl;
                    pairs += it.second * compl_counter;
                }
            }
        }
    }

    // std::cout << pairs << std::endl;

    return pairs;
}


int main() {
    std::vector<int> v1;

    v1.push_back(1);
    std::cout << "1. Expected 0, got " << solution(1, v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(2);
    std::cout << "2. Expected 2, got " << solution(3, v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(1);
    std::cout << "3. Expected 4, got " << solution(2, v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(2);
    v1.push_back(3);
    v1.push_back(4);
    std::cout << "4. Expected 0, got " << solution(99, v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(2);
    v1.push_back(3);
    v1.push_back(3);
    std::cout << "5. Expected 4, got " << solution(5, v1) << std::endl;

    v1.clear();
    v1.push_back(3);
    v1.push_back(3);
    v1.push_back(3);
    std::cout << "6. Expected 9, got " << solution(6, v1) << std::endl;

    v1.clear();
    v1.push_back(3);
    v1.push_back(3);
    v1.push_back(3);
    v1.push_back(0);
    std::cout << "7. Expected 6, got " << solution(3, v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(8);
    v1.push_back(-3);
    v1.push_back(0);
    v1.push_back(1);
    v1.push_back(3);
    v1.push_back(-2);
    v1.push_back(4);
    v1.push_back(5);

    std::cout << "8. Expected 7, got " << solution(6, v1) << std::endl;

    // int x1 = 1 << 31;
    // long x = x1 + (long)x1;
    // std::unordered_map<int, int> mmm;
    // mmm[x1] = 100500;

    // std::cout << "RRRRR: " << x1+1 << " /// " << ((1 << 31) + 1) << std::endl;

    return 0;
}
