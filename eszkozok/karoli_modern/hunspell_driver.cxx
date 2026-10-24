// Minimal Hunspell driver: reads one word per line (UTF-8) from stdin,
// writes "word<TAB>1|0<TAB>suggestions(;-joined, only if --suggest and rejected)".
#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include "hunspell.hxx"

int main(int argc, char** argv) {
    if (argc < 3) { std::cerr << "usage: hs_check aff dic [--suggest]\n"; return 2; }
    bool sug = (argc > 3 && std::strcmp(argv[3], "--suggest") == 0);
    Hunspell h(argv[1], argv[2]);
    std::string w;
    while (std::getline(std::cin, w)) {
        if (!w.empty() && w.back() == '\r') w.pop_back();
        if (w.empty()) continue;
        bool ok = h.spell(w);
        std::cout << w << '\t' << (ok ? 1 : 0) << '\t';
        if (!ok && sug) {
            std::vector<std::string> s = h.suggest(w);
            for (size_t i = 0; i < s.size() && i < 3; ++i) { if (i) std::cout << ';'; std::cout << s[i]; }
        }
        std::cout << '\n';
    }
    return 0;
}
