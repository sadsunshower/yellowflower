// Code by Nicc
// Re-implement fastdict with a hash table

#define DEFAULT_SIZE 1024

struct table_entry {
    char* key;
    int* value;
    struct table_entry* next;
};

struct fastdict {
    struct table_entry** table;
    int size;
    int (*strhash) (char*, int);
};

typedef struct fastdict* Dict;

Dict dict_create(int (*strhash) (char*, int));
int* dict_get(Dict d, char* key);
void dict_put(Dict d, char* key, int* value);