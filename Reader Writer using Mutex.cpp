#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

mutex readmutex, writemutex;

int readerCount = 0;

void reader(int Id) {
    readmutex.lock();
    readerCount++;
    
    if (readerCount == 1) {
        writemutex.lock();
    }
    readmutex.unlock();

    cout << "Reader " << Id << " is reading" << endl;

    readmutex.lock();
    readerCount--;
    if (readerCount == 0) {
        writemutex.unlock();
    }
    readmutex.unlock();
}

void writer(int Id) {
    writemutex.lock();
    cout << "Writer " << Id << " is writing" << endl;
    writemutex.unlock();
}

int main() {
    thread r1(reader, 1);
    thread r2(reader, 2);
    thread r3(writer, 1);

    r1.join();
    r2.join();
    r3.join();
}
