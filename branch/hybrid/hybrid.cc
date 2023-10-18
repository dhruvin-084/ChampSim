#include <ooo_cpu.h>
#include "../tage/tage.h"
#include "../perceptron/perceptron.h"

#define HYBRID_TABLE_SIZE 8192

#define BIMODAL_PRIME 8191;

uint8_t bimodal_table[HYBRID_TABLE_SIZE];

// namespace
// {
// constexpr std::size_t GLOBAL_HISTORY_LENGTH = 13;
// constexpr std::size_t COUNTER_BITS = 2;
// constexpr std::size_t GS_HISTORY_TABLE_SIZE = 8192;

// std::map<O3_CPU*, std::bitset<GLOBAL_HISTORY_LENGTH>> branch_history_vector;
// std::map<O3_CPU*, std::array<champsim::msl::fwcounter<COUNTER_BITS>, GS_HISTORY_TABLE_SIZE>> gs_history_table;

// std::size_t gs_table_hash(uint64_t ip, std::bitset<GLOBAL_HISTORY_LENGTH> bh_vector)
// {
//   std::size_t hash = bh_vector.to_ullong();
//   hash ^= ip;
//   hash ^= ip >> GLOBAL_HISTORY_LENGTH;
//   hash ^= ip >> (GLOBAL_HISTORY_LENGTH * 2);

//   return hash % GS_HISTORY_TABLE_SIZE;
// }
// } // namespace
void O3_CPU::initialize_branch_predictor()
{
    tage_init();
    for(int i = 0; i < HYBRID_TABLE_SIZE; i++){
        bimodal_table[i] = 0;
    }
}

uint8_t O3_CPU::predict_branch(uint64_t ip)
{
    auto hash = ip % BIMODAL_PRIME;
    auto value = bimodal_table[hash];
    if(value < 2) return tage_predict(ip);
    else return  perceptron_predict(ip, this);


    // auto gs_hash = ::gs_table_hash(ip, ::branch_history_vector[this]);
    // auto value = ::gs_history_table[this][gs_hash];
    // uint8_t which_pred = value.value() >= (value.maximum / 2);

    // if(which_pred) return  perceptron_predict(ip, this); 
    // else return tage_predict(ip);
}

void O3_CPU::last_branch_result(uint64_t ip, uint64_t branch_target, uint8_t taken, uint8_t branch_type)
{
    auto hash = ip % BIMODAL_PRIME;
    if(taken == tage_predict(ip) && taken != perceptron_predict(ip, this)){
        bimodal_table[hash] -= bimodal_table[hash] == 0 ? 0 : 1;
    }else if(taken != tage_predict(ip) && taken == perceptron_predict(ip, this)){
        bimodal_table[hash] += bimodal_table[hash] == 3 ? 0 : 1;
    }

    // auto gs_hash = gs_table_hash(ip, ::branch_history_vector[this]);
    // if(taken == tage_predict(ip) && taken != perceptron_predict(ip, this)){
    //     ::gs_history_table[this][gs_hash] -= 1;
    // }else if(taken != tage_predict(ip) && taken == perceptron_predict(ip, this)){
    //     ::gs_history_table[this][gs_hash] += 1;
    // }

    // update branch history vector
    // ::branch_history_vector[this] <<= 1;
    // ::branch_history_vector[this][0] = taken;
    
    tage_train(ip, taken);
    perceptron_train(ip, branch_target, taken, branch_type, this);
}