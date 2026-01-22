#include <stdio.h>
#include <pthread.h>

// Thread function
void* thread_function(void* arg) {
    int num = *(int*)arg;
    printf("Thread is running. Number = %d\n", num);
    return NULL;
}

int main() {
    pthread_t thread;
    int value = 5;

    // Create thread
    pthread_create(&thread, NULL, thread_function, &value);

    // Wait for thread to finish
    pthread_join(thread, NULL);

    printf("Main thread finished.\n");
    return 0;
}
