#include <iostream>
#include <vector>

int main() {
    const std::vector<int> numbers{1, 2, 4};
    int sum = 0;
    for (int number : numbers) {
        sum += number;
    }
    std::cout << "OK " << sum << '\n';
    return sum == 7 ? 0 : 1;
}
