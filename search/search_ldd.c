// Code by Nicc
// Use a memoised version of Levenshtein-Damerau string metric to search the handbook

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define min3(_x, _y, _z) (((_x) < (_y) && (_x) < (_z)) ? (_x) : (((_y) < (_x) && (_y) < (_z)) ? (_y) : (_z)))
#define min(_x, _y) ((_x) < (_y) ? (_x) : (_y))
#define max(_x, _y) ((_x) > (_y) ? (_x) : (_y))

int levenshtein_damerau_memoised(char* s1, char* s2);
int levenshtein_damerau(char* s1, int l1, char* s2, int l2, int** memo);

int main(int argc, char** argv)
{
    FILE* tokenised = fopen("courses-tokenised.txt", "r");
    char line[1024];

    while (fgets(line, 1024, tokenised) != NULL) {
        double min_dist = 1.0;
        char* token = strtok(line, "|");
        char* name = token;

        token = strtok(NULL, "|");

        while (token != NULL) {
            for (int i = 1; i < argc; i++) {
                double d = levenshtein_damerau_memoised(token, argv[i]) / (max(strlen(argv[i]), strlen(token))*1.0);
                if (d < min_dist) {
                    min_dist = d;
                }
            }

            token = strtok(NULL, "|");
        }
        
        min_dist = floor(min_dist*100);

        if (min_dist <= 44) printf("%s|%.0lf\n", name, min_dist);
    }
}

int levenshtein_damerau_memoised(char* s1, char* s2)
{
    int l1 = strlen(s1);
    int l2 = strlen(s2);

    int** memo = malloc(sizeof(int*) * (l1 + 1));
    for (int i = 0; i < l1 + 1; i++) {
        memo[i] = malloc(sizeof(int) * (l2 + 1));
        for (int j = 0; j < l2 + 1; j++) {
            memo[i][j] = -1;
        }
    }

    return levenshtein_damerau(s1, l1, s2, l2, memo);
}

int levenshtein_damerau(char* s1, int l1, char* s2, int l2, int** memo)
{
    int cost = 0;

    if (l1 == 0) return l2;
    if (l2 == 0) return l1;

    if (s1[l1 - 1] == s2[l2 - 1]) {
        cost = 0;
    } else {
        cost = 1;
    }

    int d1 = memo[l1 - 1][l2];
    if (d1 == -1) {
        d1 = levenshtein_damerau(s1, l1 - 1, s2, l2, memo);
        memo[l1 - 1][l2] = d1;
    }

    int d2 = memo[l1][l2 - 1];
    if (d2 == -1) {
        d2 = levenshtein_damerau(s1, l1, s2, l2 - 1, memo);
        memo[l1][l2 - 1] = d2;
    }

    int d3 = memo[l1 - 1][l2 - 1];
    if (d3 == -1) {
        d3 = levenshtein_damerau(s1, l1 - 1, s2, l2 - 1, memo);
        memo[l1 - 1][l2 - 1] = d3;
    }

    int tmp = min3(d1 + 1, d2 + 1, d3 + cost);

    if (l1 > 1 && l2 > 1 && s1[l1 - 2] == s2[l2 - 1] && s1[l1 - 1] == s2[l2 - 2]) {
        int d4 = memo[l1 - 2][l2 - 2];
        if (d4 == -1) {
            d4 = levenshtein_damerau(s1, l1 - 2, s2, l2 - 2, memo);
            memo[l1 - 2][l2 - 2] = d4;
        }

        tmp = min(tmp, d4 + cost);
    }

    return tmp;
}