#include <iostream>
#include <thread>
#include <chrono>
#include <string>
#include <sstream>
using namespace std;

#ifdef __linux__
#include <fstream>
#include <cstdlib>


#elif __APPLE__
#include <mach/mach_host.h>
#include <mach/host_info.h>
#include <mach/vm_statistics.h>


host_cpu_load_info_data_t getCpuUsage(){
    host_cpu_load_info_data_t cpu_info;
    mach_msg_type_number_t count = HOST_CPU_LOAD_INFO_COUNT;
    kern_return_t status = host_statistics(mach_host_self(), HOST_CPU_LOAD_INFO, (host_info_t)&cpu_info, &count);
    return cpu_info;
}

long long calcCpu(host_cpu_load_info_data_t data1, host_cpu_load_info_data_t data2){
    long long data1_total = data1.cpu_ticks[CPU_STATE_USER] + data1.cpu_ticks[CPU_STATE_SYSTEM] + data1.cpu_ticks[CPU_STATE_IDLE];
    long long data1_idle = data1.cpu_ticks[CPU_STATE_IDLE];

    long long data2_total = data2.cpu_ticks[CPU_STATE_USER] + data2.cpu_ticks[CPU_STATE_SYSTEM] + data2.cpu_ticks[CPU_STATE_IDLE];
    long long data2_idle = data2.cpu_ticks[CPU_STATE_IDLE];

    long long total_delta = data2_total - data1_total;
    long long idle_delta = data2_idle - data1_idle;

    if (total_delta > 0){
        return (100 * (1-static_cast<double>(idle_delta)/total_delta));
    }
    return 0.0;

}

void getMemoryUsage(){

}

void calcMemory(){

}

host_cpu_load_info_data_t data1 = getCpuUsage();
host_cpu_load_info_data_t data2;


#endif

int main(){
    while (true){
        this_thread::sleep_for(chrono::seconds(1));
        data2 = getCpuUsage();
        double cpuUsage = calcCpu(data1, data2);
        cout << cpuUsage << endl;
        data1 = data2;

    }
    return 0;
}