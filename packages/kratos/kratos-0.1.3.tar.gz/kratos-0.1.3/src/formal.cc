#include "formal.hh"

#include "stmt.hh"

namespace kratos {

class AsyncVisitor : public IRVisitor {
public:
    void visit(Generator *gen) override {
        auto const stmt_count = gen->stmts_count();
        std::unordered_set<Port *> rst_ports;
        for (uint64_t i = 0; i < stmt_count; i++) {
            auto stmt = gen->get_stmt(i);
            if (stmt->type() != StatementType::Block) continue;
            auto stmt_blk = stmt->as<StmtBlock>();
            if (stmt_blk->block_type() != StatementBlockType::Sequential) continue;
            auto seq = stmt_blk->as<SequentialStmtBlock>();
            auto &conditions = seq->get_event_controls();
            conditions.erase(
                std::remove_if(conditions.begin(), conditions.end(),
                               [&rst_ports](const EventControl &e) -> bool {
                                   auto *var = e.var;
                                   if (var->type() != VarType::BaseCasted) {
                                       if (var->type() == VarType::PortIO) {
                                           auto port = var->as<Port>();
                                           if (port->port_type() == PortType::AsyncReset) {
                                               // need to remove this one
                                               rst_ports.emplace(port.get());
                                               return true;
                                           }
                                       }
                                   } else {
                                       auto casted = var->as<VarCasted>();
                                       if (casted->cast_type() == VarCastType::AsyncReset) {
                                           // need to remove this one
                                           return true;
                                       }
                                   }
                                   return false;
                               }),
                conditions.end());
        }

        for (auto const &var : rst_ports) {
            var->set_port_type(PortType::Reset);
        }
    }
};

void remove_async_reset(Generator *top) {
    AsyncVisitor visitor;
    visitor.visit_generator_root_p(top);
}
}  // namespace kratos