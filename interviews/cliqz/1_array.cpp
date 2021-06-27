#include <vector>
#include <iostream>


int solution(std::vector<int> *v) {
    std::vector<int> & v_ref = *v;

    int jumps = 0;
    int current_index = 0;
    int previous_index = 0;
    while (true) {
        if (v_ref[current_index] == 0) {
            return -1;
        } else {
            ++jumps;

            previous_index = current_index;
            current_index += v_ref[current_index];

            if (current_index < 0 || current_index >= v_ref.size()) {
                return jumps;
            }

            v_ref[previous_index] = 0;
        }
    }
}


int main() {
    std::vector<int> v1;
    v1.push_back(1);
    std::cout << "Expected 1, got " << solution(&v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(1);
    std::cout << "Expected 2, got " << solution(&v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(1);
    v1.push_back(-1);
    v1.push_back(1);
    std::cout << "Expected -1, got " << solution(&v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(10);
    std::cout << "Expected 2, got " << solution(&v1) << std::endl;

    v1.clear();
    v1.push_back(1);
    v1.push_back(-10);
    std::cout << "Expected 2, got " << solution(&v1) << std::endl;

    return 0;
}