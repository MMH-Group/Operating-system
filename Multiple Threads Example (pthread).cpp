#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 3

// Structure to pass data to threads
struct thread_data {
    int thread_id;
    int value;
};

// Thread function
void* thread_function(void* arg) {
    struct thread_data* data = (struct thread_data*)arg;
    printf("Thread %d running, value = %d\n",
           data->thread_id, data->value);
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    struct thread_data td[NUM_THREADS];

    // Create multiple threads
    for (int i = 0; i < NUM_THREADS; i++) {
        td[i].thread_id = i;
        td[i].value = (i + 1) * 10;
        pthread_create(&threads[i], NULL, thread_function, &td[i]);
    }

    // Wait for all threads to finish
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("All threads completed.\n");
    return 0;
}
