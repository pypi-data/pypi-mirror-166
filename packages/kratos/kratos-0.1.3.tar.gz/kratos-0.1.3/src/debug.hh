#ifndef KRATOS_DEBUG_HH
#define KRATOS_DEBUG_HH

#include "stmt.hh"

namespace kratos {

std::vector<const Stmt *> extract_debug_break_points(Generator *top);
void remove_assertion(Generator *top);
void propagate_scope_variable(Generator *top);
std::unordered_map<Var *, std::unordered_set<Var *>> find_driver_signal(Generator *top);
// this is a pass for systems that don't fully integrate kratos as their backend but only
// want to partially use Kratos' debuggability
// it will fake a hierarchy
void mock_hierarchy(Generator *top, const std::string &top_name = "");

// for verilator
void insert_verilator_public(Generator *top);

void inject_assertion_fail(Generator *top);

class DebugDatabase {
public:
    DebugDatabase() = default;

    void set_break_points(Generator *top);
    void set_break_points(Generator *top, const std::string &ext);

    void set_variable_mapping(const std::map<Generator *, std::map<std::string, Var *>> &mapping);
    void set_variable_mapping(
        const std::map<Generator *, std::map<std::string, std::string>> &mapping);

    void save_database(const std::string &filename, bool override);
    void save_database(const std::string &filename) { save_database(filename, true); }

private:
    std::vector<const Stmt *> break_points_;
    std::map<const Stmt *, std::pair<std::string, uint32_t>> stmt_mapping_;
    std::unordered_map<const Generator *, std::map<std::string, std::string>> variable_mapping_;
    std::map<const Stmt *, std::map<std::string, std::pair<bool, std::string>>> stmt_context_;
    std::unordered_set<Generator *> generators_;

    Generator *top_ = nullptr;

    void compute_generators(Generator *top);
};

}  // namespace kratos
#endif  // KRATOS_DEBUG_HH
