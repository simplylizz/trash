#include <vector>
#include <unordered_map>
#include <iostream>
#include <limits>


#define MOD 1000000;


std::vector<std::vector<unsigned long> > matrix_mul(
    std::vector<std::vector<unsigned long> > const & m1,
    std::vector<std::vector<unsigned long> > const & m2
) {
    std::vector<std::vector<unsigned long> > result (2, std::vector<unsigned long> (2, 0));

    result[0][0] = (m1[0][0] * m2[0][0] + m1[0][1] * m2[1][0]) % MOD;
    result[0][1] = (m1[0][0] * m2[0][1] + m1[0][1] * m2[1][1]) % MOD;
    result[1][0] = (m1[1][0] * m2[0][0] + m1[1][1] * m2[1][0]) % MOD;
    result[1][1] = (m1[1][0] * m2[0][1] + m1[1][1] * m2[1][1]) % MOD;

    return result;
}


std::vector<std::vector<unsigned long> > matrix_pow(std::vector<std::vector<unsigned long> > const & m, int pow) {
    // std::cout << "calc p=" << pow << std::endl;
    if (pow == 1) {
        // std::cout << "return p=1" << std::endl;
        return m;
    } else if (pow == 2) {
        // std::cout << "return p=1" << std::endl;
        return matrix_mul(m, m);
    } else {
        std::vector<std::vector<unsigned long> > half_result = matrix_pow(m, pow >> 1);

        std::vector<std::vector<unsigned long> > result = matrix_mul(half_result, half_result);
        if (pow % 2 == 1) {
            result = matrix_mul(result, m);
        }

        return result;
    }
}


int solution(int n) {
    if (n < 0) {
        throw -1;
    } else if (n < 3) {
        return n > 0;
    }

    std::vector<std::vector<unsigned long> > matrix (2, std::vector<unsigned long> (2, 0));

    matrix[0][0] = 1;
    matrix[0][1] = 1;
    matrix[1][0] = 1;

    return matrix_pow(matrix, n)[0][1];
}


int main() {
    std::cout << "0. Expected 0, got " << solution(0) << std::endl;
    std::cout << "1. Expected 1, got " << solution(1) << std::endl;
    std::cout << "2. Expected 1, got " << solution(2) << std::endl;
    std::cout << "3. Expected 2, got " << solution(3) << std::endl;
    std::cout << "4. Expected 3, got " << solution(4) << std::endl;
    std::cout << "5. Expected 5, got " << solution(5) << std::endl;
    std::cout << "6. Expected 8, got " << solution(6) << std::endl;
    std::cout << "7. Expected 13, got " << solution(7) << std::endl;

    std::cout << "30. Expected 832040, got " << solution(30) << std::endl;
    std::cout << "31. Expected 346269, got " << solution(31) << std::endl;
    std::cout << "32. Expected 178309, got " << solution(32) << std::endl;
    std::cout << "33. Expected 524578, got " << solution(33) << std::endl;

    std::cout << "10000. Expected 366875 got " << solution(10000) << std::endl;

    std::cout << "???. Expected ??? got " << solution(100000000) << std::endl;
    

    return 0;
}
