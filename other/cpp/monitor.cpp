#include <iostream>
#include <thread>
#include <chrono>
#include <string>
#include <sstream>
#include <iomanip>
using namespace std;

#ifdef __linux__
#include <fstream>
#include <cstdlib>

struct cpuStats {
    unsigned long long user;
    unsigned long long nice;
    unsigned long long system;
    unsigned long long idle;
    unsigned long long iowait;
    unsigned long long irq;
    unsigned long long softirq;
    unsigned long long steal;
    unsigned long long guest;
    unsigned long long guest_nice;
};

struct memInfo {
    unsigned long long totalKb;
    unsigned long long availableKb;
};

unsigned long long sumStats(cpuStats data){
    return data.user + data.nice + data.system + data.idle +
    data.iowait + data.irq + data.softirq + data.steal +
    data.guest + data.guest_nice;
}
cpuStats getCpuUsage(){
    cpuStats stats;
    ifstream file("/proc/stat");
    if (!file.is_open()) {
        cerr << "Error: Could not open /proc/stat" << endl;
        exit(1);
    }
    string line;
    getline(file, line);
    istringstream iss(line);
    string cpu_label;
    iss >> cpu_label;
    iss >> stats.user >> stats.nice >> stats.system >> stats.idle >> stats.iowait >> stats.irq >> stats.softirq >> stats.steal >> stats.guest >> stats.guest_nice;
    return stats;
}

double calcCpu(cpuStats data1, cpuStats data2){
    unsigned long long data2_total = sumStats(data2);
    unsigned long long data2_idle = data2.idle + data2.iowait;

    unsigned long long data1_total = sumStats(data1);
    unsigned long long data1_idle = data1.idle + data1.iowait;

    unsigned long long total_delta = data2_total - data1_total;
    unsigned long long idle_delta =data2_idle - data1_idle;

    if (total_delta > 0){
        return (100.0 * (total_delta - idle_delta)/total_delta);
    }
    return 0.0;
}

double getCpuTemp(){
    ifstream file("/sys/class/hwmon/hwmon1/temp3_input");
    long long temp;
    if (!file.is_open()) {
        cerr << "Error: Could not open /proc/stat" << endl;
        exit(1);
    }
    file >> temp;
    file.close();
    return static_cast<double>(temp) / 1000.0;
}

memInfo getMemoryUsage(){
    memInfo data = {0, 0};
    ifstream file("/proc/meminfo");
    if (!file.is_open()) {
        cerr << "Error: Could not open /proc/meminfo" << endl;
        return data;
    }
    string line;
    while(getline(file, line)){
        stringstream ss(line);
        string key;
        unsigned long long value;
        string unit;
        ss >> key >> value;
        if (key == "MemTotal:"){
            data.totalKb = value;
        }
        else if (key == "MemAvailable:"){
            data.availableKb = value;
        }
        if (data.availableKb > 0 && data.totalKb > 0){
            break;
        }
    }
    file.close();
    return(data);
}

cpuStats cpuData1 = getCpuUsage();
cpuStats cpuData2;
memInfo ramInfo;

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

double calcCpu(host_cpu_load_info_data_t data1, host_cpu_load_info_data_t data2){
    long long data1_total = data1.cpu_ticks[CPU_STATE_USER] + data1.cpu_ticks[CPU_STATE_SYSTEM] + data1.cpu_ticks[CPU_STATE_IDLE];
    long long data1_idle = data1.cpu_ticks[CPU_STATE_IDLE];

    long long data2_total = data2.cpu_ticks[CPU_STATE_USER] + data2.cpu_ticks[CPU_STATE_SYSTEM] + data2.cpu_ticks[CPU_STATE_IDLE];
    long long data2_idle = data2.cpu_ticks[CPU_STATE_IDLE];

    long long total_delta = data2_total - data1_total;
    long long idle_delta = data2_idle - data1_idle;

    if (total_delta > 0){
        return (100.0 * (1-static_cast<double>(idle_delta)/total_delta));
    }
    return 0.0;

}

void getMemoryUsage(){

}

void calcMemory(){

}

host_cpu_load_info_data_t cpuData1 = getCpuUsage();
host_cpu_load_info_data_t cpuData2;


#endif

int main(){
    while (true){
        this_thread::sleep_for(chrono::seconds(1));
        cpuData2 = getCpuUsage();
        ramInfo = getMemoryUsage();
        double cpuUsage = calcCpu(cpuData1, cpuData2);
        double cpuTemp = getCpuTemp();
        cout << fixed << setprecision(2) 
        << "CPU usage: " << cpuUsage << "%" 
        << setprecision(1) << " (" << cpuTemp << "°)" 
        << setprecision(2) << "  |  Memory usage: " << (ramInfo.totalKb - ramInfo.availableKb)/1024.0/1024.0 << "gb (" << (ramInfo.totalKb - ramInfo.availableKb)/static_cast<double>(ramInfo.totalKb) * 100 << "%)" << endl;
        cpuData1 = cpuData2;
    }

    return 0;
}