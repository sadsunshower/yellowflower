// Code by Nicc
// Re-implement fastdict with a hash table

#include <stdlib.h>
#include <string.h>

#include "fastdict.h"

Dict dict_create(int (*strhash) (char*, int))
{
    Dict d = malloc(sizeof(struct fastdict));
    d->size = DEFAULT_SIZE;
    d->strhash = strhash;

    d->table = malloc(sizeof(struct table_entry*) * d->size);
    for (int i = 0; i < d->size; i++) {
        d->table[i] = NULL;
    }

    return d;
}

int* dict_get(Dict d, char* key)
{
    int hash = d->strhash(key, d->size);

    struct table_entry* curr = d->table[hash];
    while (curr != NULL) {
        if (strcmp(curr->key, key) == 0) {
            return curr->value;
        }
        curr = curr->next;
    }

    return NULL;
}

void dict_put(Dict d, char* key, int* value)
{
    int hash = d->strhash(key, d->size);

    struct table_entry* curr = d->table[hash];
    if (curr == NULL) {
        struct table_entry* new = malloc(sizeof(struct table_entry));
        new->key = key;
        new->value = value;

        d->table[hash] = new;

        return;
    }

    struct table_entry* prev = NULL;
    while (curr != NULL) {
        if (strcmp(curr->key, key) == 0) {
            curr->value = value;
            return;
        }
        prev = curr;
        curr = curr->next;
    }

    struct table_entry* new = malloc(sizeof(struct table_entry));
    new->key = key;
    new->value = value;
    prev->next = new;
}