#include <iostream> 
#include <vector>
#include <unordered_set>
#include <string>
#include <algorithm>
#include <sstream>


// Solution class
class Solution {
public:
    // sumtest function for sorted array
    bool sumtest(std::vector<int>& array, int testsum) {
        int left_ind    = 0; // index from the left end of the array
        int right_ind   = array.size() -1; // index from the right end of the array
        while(left_ind < right_ind){
            if(array[left_ind] + array[right_ind] == testsum)
                return true;
            else if(array[left_ind] + array[right_ind] > testsum)
                right_ind--;
            else
                left_ind++;
        }
		return false;
    }
    
    // sumtest function for unsorted array
    bool sumtest_nosort(std::vector<int>& array, int testsum) {
        std::unordered_set<int> set;
        int n = (int)array.size();
        for (int i = 0; i < n; i++) {
            int complement = testsum - array[i];
            // check if complement is in the set or not
            std::unordered_set<int>::const_iterator got = set.find(complement);
            if ( got == set.end() )
                set.insert(array[i]);
            else
                return true;
        }
        return false;
    }
};

void trimLeftTrailingSpaces(std::string &input) {
    input.erase(input.begin(), find_if(input.begin(), input.end(), [](int ch) {
        return !isspace(ch);
    }));
}

void trimRightTrailingSpaces(std::string &input) {
    input.erase(find_if(input.rbegin(), input.rend(), [](int ch) {
        return !isspace(ch);
    }).base(), input.end());
}

std::vector<int> stringToIntegerVector(std::string input) {
    std::vector<int> output;
    trimLeftTrailingSpaces(input);
    trimRightTrailingSpaces(input);
    input       = input.substr(1, input.length() - 2);
    std::stringstream ss;
    ss.str(input);
    std::string item;
    char delim  = ',';
    while (getline(ss, item, delim)) {
        output.push_back(stoi(item));
    }
    return output;
}


int main() {
    std::string line; // string contains input array or testsum
    bool issorted;
    bool dosorting  = false;
    // determine whether sorting is needed or not
    std::cout << "Is the array sorted or not? (Y/N)" << std::endl;
    getline(std::cin, line);
    std::transform(line.begin(), line.end(), line.begin(), ::tolower);
    if (line == "y" || line == "yes")
        issorted    = true;
    else if (line == "n" || line == "no"){
        issorted    = false;
        std::cout << "Do you need the array to be sorted? (Y/N)" << std::endl;
        getline(std::cin, line);
        std::transform(line.begin(), line.end(), line.begin(), ::tolower);
        if (line == "y" || line == "yes")
            dosorting   = true;
        else if (line == "n" || line == "no")
            dosorting   = false;
    }
    else
        return -1;
    
    while (true) {
        std::cout << "Input array (e.g. [1, 5, 7, 9]), type exit to exit" << std::endl;
        getline(std::cin, line);
        if  (line == "exit")
            break;
        std::vector<int> array   = stringToIntegerVector(line);
        // perform sorting based upon the value of dosorting
        if (dosorting){
            sort(array.begin(), array.end());
            std::cout << "Sorted array : "; 
            for (auto x : array) 
                std::cout << x << " ";
            std::cout << std::endl;
        }
        // input testsum
        std::cout << "Input integer as testsum" << std::endl;
        getline(std::cin, line);
        int testsum         = stoi(line);
        //return a boolean
        bool out;
        if (issorted || dosorting)
            out             = Solution().sumtest(array, testsum);
        else
            out             = Solution().sumtest_nosort(array, testsum);
        std::string output  = out ? "true" : "false";
        std::cout << "Answer: "<<output << std::endl;
    }
    return 0;
}